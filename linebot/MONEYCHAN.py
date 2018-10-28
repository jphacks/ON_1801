import re
import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)



line_bot_api = LineBotApi(os.environ['LineBotApi'])
handler = WebhookHandler(os.environ['WebHook'])




@app.route("/bot/callback", methods=['POST'])

def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



@handler.add(MessageEvent, message=TextMessage)


# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))


#追加

def text_message_handler(event):


    if re.match('.*残高.*',event.message.text):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('残っていないよ'))
    elif event.message.text in ['差額', '差', ]:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('-10000円！'))
    elif event.message.text in ['いくら', 'どのくらい', ]:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('5000円使ったよ'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('ちゃんと話して！'))


if __name__ == "__main__":
    app.run()
