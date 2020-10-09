class Push:
    def push(url, name, image):

        payload = {
            "type": "flex",
            "altText": "Flex Message",
            "contents": {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": image,
                    "size": "4xl",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                        "type": "uri",
                        "label": "Line",
                        "uri": url
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": name,
                            "size": "xl",
                            "color": "#000000",
                            "weight": "bold"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "神げー攻略サイト",
                                            "flex": 1,
                                            "size": "sm",
                                            "color": "#AAAAAA"
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "backgroundColor": "#98fb98"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "flex": 0,
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "spacer",
                            "size": "sm"
                        }
                    ],
                    "backgroundColor": "#98fb98"
                }
            }
        }
        return payload
