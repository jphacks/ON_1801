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

line_bot_api = LineBotApi('+0V7hEjD589awEkFpf6SCDTA60ZJN51F6srJ7MTKbHHdBK16lS+TUUiSIyR9G49/L8hOrHlcK2q2fwwRnPNBfpWx3k+c8O8TPvHPMkIVLMFx1CnYApoBlMJ564D/M4whImS/v2KLEGtDvPligs7eiAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6f14db34b596943c2e6a8162b02e6d4e')


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
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
