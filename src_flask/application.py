import  sqlite3
from flask import Flask, request, jsonify, g
import logging
import cek
import os
import peewee as pe
import zaim
from datetime  import datetime, date,timedelta

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
    welcome_japanese = cek.Message(message="金なら残っていないぞ", language="ja")
    response = clova.response([welcome_japanese])
    return response

# WifeStatusIntentの発火箇所
@clova.handle.intent("StatusIntent")
def wife_status_handler(clova_request):
    VALUE = (yesterday_sum() - today_sum())
    print(VALUE)

    money_msg = clova_request.slot_value('money_chan')
    response = clova.response("もう一回言ってね")
    print(money_msg)
    if money_msg is not None:
        if money_msg == "差額":
            response = clova.response("先月との差額は"+str(VALUE)+"円だよ")
            if VALUE < 0:
                response = clova.response("先月との差額はマイナス"+str(VALUE)+"円だよ！使いすぎです。")
        elif money_msg == "残高":
            response = clova.response("残っていないよ")
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

def request_zaim_money_day(zapi,calc_days=0):
    d_day = datetime.today()
    if calc_days !=0 :
        if calc_days < 0 :
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
    return calc_money_sum(request_zaim_money_day(request_zaim_setup(),-1))

if __name__ == '__main__':
    application.run()
