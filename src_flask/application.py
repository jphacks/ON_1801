import  sqlite3
from flask import Flask, request, jsonify, g
import logging
import cek
import os
import peewee as pe
import zaim
import datetime

db = pe.SqliteDatabase('my_database.db')


class BaseModel(pe.Model):
    class Meta:
        database = db

# データテーブルのモデル
class User(BaseModel):
    id = pe.IntegerField()

class ZaimAccesstoken(BaseModel):
    user = pe.ForeignKeyField(User, related_name='zaimaccesstokens')
    access = pe.CharField()


class Zaim(BaseModel):
    id = pe.IntegerField()
    user = pe.ForeignKeyField(User, related_name='zaims')
    money = pe.IntegerField()



application = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

clova = cek.Clova(
    application_id=os.environ['CLOVA_ID'],
    default_language="ja",
    debug_mode=True)


@application.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    logger.info('Lambda function invoked index()')
    return 'hello from Flask!'

# /clova に対してのPOSTリクエストを受け付けるサーバーを立てる
@application.route('/clova', methods=['POST'])
def my_service():
    body_dict = clova.route(body=request.data, header=request.headers)
    response = jsonify(body_dict)
    response.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return response

# 起動時の処理
@clova.handle.launch
def launch_request_handler(clova_request):
    welcome_japanese = cek.Message(message="はい何でしょう", language="ja")
    response = clova.response([welcome_japanese])
    return response

# WifeStatusIntentの発火箇所
@clova.handle.intent("StatusIntent")
def wife_status_handler(clova_request):
    VALUE = 100000

    money_msg = clova_request.slot_value('money_chan')
    response = clova.response("もう一回行ってください")
    if money_msg is not None:
        if money_msg == "差額":
            response = clova.response("差額は"+str(VALUE)+"です。")
            if VALUE > 10000:
                response = clova.response("使いすぎです。")
    return response


# 終了時
@clova.handle.end
def end_handler(clova_request):
    # Session ended, this handler can be used to clean up
    logger.info("Session ended.")

# 認識できなかった場合
@clova.handle.default
def default_handler(request):
    return clova.response("Sorry I don't understand! Could you please repeat?")

# zaimに問い合わせ

def request_zaim_setup():
    zapi = zaim.Api(consumer_key=os.environ['ZAIM_KEY'],
                consumer_secret=os.environ['ZAIM_SECRET'],
                access_token=os.environ['ACCESS_TOKEN_ZAIM'],
                access_token_secret=os.environ['ACCESS_TOKEN_ZAIM_SECRET'])
    return zapi

def request_zaim_money(zapi):
    d_today = datetime.date.today()
    today_moneys_json = zapi.money(mapping=1,
              start_date=d_today.strftime('%Y-%m-%d'),
              mode='payment',
              end_date=d_today.strftime('%Y-%m-%d')
    )
    return today_moneys_json
 
def today_sum():
    moneys = request_zaim_money(request_zaim_setup())
    summoney = 0
    for money in moneys['money']:
        summoney += money['amount']
    return summoney

                      


if __name__ == '__main__':
    application.run()
