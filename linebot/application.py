import re
import os
import zaim
from datetime  import datetime, date,timedelta
import logging

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



application = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



line_bot_api = LineBotApi(os.environ['LineBotApi'])
handler = WebhookHandler(os.environ['WebHook'])

@application.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    logger.info('Lambda function invoked index()')
    return 'hello from Flask!'

@application.route("/bot/callback", methods=['POST'])

def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    application.logger.info("Request body: " + body)

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

    VALUE = (yesterday_sum() - today_sum())


    if re.match('.*残高.*',event.message.text):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('残っていないよ'))
    elif re.match('.*差額.*',event.message.text):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('先月との差額は'+str(VALUE)+'円だよ'))
    elif re.match('.*今日.*いくら.*',event.message.text):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('5000円使ったよ'))
    elif re.match('gitub',event.message.text,re.IGNORECASE):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('https://github.com/jphacks/ON_1801'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('ちゃんと話して！'))


#zaimに問い合わせ

def request_zaim_setup():
    zapi = zaim.Api(consumer_key=os.environ['ZAIM_KEY'],
                    consumer_secret=os.environ['ZAIM_SECRET'],
                    access_token=os.environ['ACCESS_TOKEN_ZAIM'],
                    access_token_secret=os.environ['ACCESS_TOKEN_ZAIM_SECRET'])
    return zapi


def request_zaim_money_day(zapi, calc_days=0):
    d_day = datetime.today()
    if calc_days != 0:
        if calc_days < 0:
            calc_days *= -1
        d_day = d_day - timedelta(days=calc_days)
    print(d_day.strftime('%Y-%m-%d'))
    day_moneys_json = zapi.money(mapping=1,
                                 start_date=d_day.strftime('%Y-%m-%d'),
                                 mode='payment',
                                 end_date=d_day.strftime('%Y-%m-%d')
                                 )
    return day_moneys_json


def today_sum():
    return calc_money_sum(request_zaim_money_day(request_zaim_setup()))


def calc_money_sum(moneys):
    summoney = 0
    for money in moneys['money']:
        summoney += money['amount']
    return summoney


def yesterday_sum():
    return calc_money_sum(request_zaim_money_day(request_zaim_setup(), -1))


if __name__ == "__main__":
    application.run()
