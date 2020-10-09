import random

#https://developers.line.biz/media/messaging-api/sticker_list.pdf
#LINE Developer スタンプリストを参照
class Sticker(object):
    def stickersend():
        ra = random.randint(0, 2)
        send = []
        PackageIDlist = [('11537','520027'),('11538','51626'),('11539','521141')]
        if ra == 0:
                id = random.randint(34, 73)
                send.append(PackageIDlist[ra][0])
                send.append(PackageIDlist[ra][1] + str(id))
        if ra == 1:
                id = random.randint(494, 533)
                send.append(PackageIDlist[ra][0])
                send.append(PackageIDlist[ra][1] + str(id))
        if ra == 2:
                id = random.randint(10, 49)
                send.append(PackageIDlist[ra][0])
                send.append(PackageIDlist[ra][1] + str(id))
        return send
