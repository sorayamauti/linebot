# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

# import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReplyButton, MessageAction, QuickReply,
    # TemplateSendMessage,ButtonsTemplate,URIAction,
    ImageSendMessage,FlexSendMessage,StickerMessage,
    StickerSendMessage,
)
from pymongo import MongoClient
from push import Push
from lineai import Lineai
# from richmenu import RichMenu, RichMenuManager
# import json
# import requests
# import os
from linesticker import Sticker

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = 'secret'
channel_access_token = 'token'
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler =  WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#テキスト応答
@handler.add(MessageEvent, message=(TextMessage))
def handle_message(event):
    bool = True
    #データベースに接続
    client = MongoClient('mongodb://root:password@mongodb:27017/')
    db = client.pazudora_db
    collection = db.kouryaku_fe
    collectionimg = db.kouryakuimages_fe
    return_text = ""
    push = Push

    for record in collection.find(filter={'name': event.message.text}):
        for image in collectionimg.find(filter={'name': {'$regex': event.message.text}}):
            payload = push.push(record["url"],record["name"],image["url"]  )
            container_obj = FlexSendMessage.new_from_json_dict(payload)
            line_bot_api.reply_message(event.reply_token, messages=container_obj)
            bool = False

    #ラインパズドラ情報応答
    #神げー攻略サイトさんを参照
    if event.message.text == "パズドラ":
        pazulist = ["最強リーダー", "最強サブ", "無課金最強",
                    "ガチャ", "コラボ", "リセマラ",
                    "ダンジョン攻略", "モンスター", "パーティ"]
        #データベースを作っておく
        items = [QuickReplyButton(action=MessageAction(label=f"{list}", text=f"{list}")) for list in pazulist]
        messages = TextSendMessage(text="なにがしりたい？", quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)

    # その他テキスト自動応答
    elif bool == True:
        push_text = event.message.text
        msg = Lineai.talkapi(push_text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))

#スタンプ応答
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    PackageIDlist = ['11537','11538','11539']
    #スタンプに対しておうむ返し。デフォルトであるスタンプのみ返す
    if (event.message.package_id in PackageIDlist) == True:
        line_bot_api.reply_message(event.reply_token,
            StickerSendMessage(package_id=event.message.package_id,sticker_id=event.message.sticker_id))
    else:
         # デフォルトに無いスタンプに、デフォルトスタンプを返す(ランダム)
        st = Sticker.stickersend()
        event.message.package_id = st[0]
        event.message.sticker_id = st[1]
        line_bot_api.reply_message(event.reply_token,
            StickerSendMessage(package_id=event.message.package_id,sticker_id=event.message.sticker_id))

if __name__ == "__main__":

    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8080, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port, host='0.0.0.0')