import requests

#リクルートさんのAPIを使用
class Api_Key(object):
    def __init__(self):
        self.__param = 'key'

class Lineai(object):
    def talkapi(text):
        apikey = Api_Key()
        TALKAPI_KEY = apikey._Api_Key__param
        url = 'url'
        req = requests.post(url, {'apikey':TALKAPI_KEY,'query':text}, timeout=5)
        data = req.json()

        if data['status'] != 0:
            return data['message']

        msg = data['results'][0]['reply']
        return msg
