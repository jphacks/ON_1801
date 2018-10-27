from venv import logger

from flask import Flask, request, jsonify
import cek
import os

app = Flask(__name__)

clova = cek.Clova(
    application_id=os.environ['CLOVA_ID']
    default_language="ja",
    debug_mode=True)

# /clova に対してのPOSTリクエストを受け付けるサーバーを立てる
@app.route('/clova', methods=['POST'])
def my_service():
    body_dict = clova.route(body=request.data, header=request.headers)
    response = jsonify(body_dict)
    response.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return response

# 起動時の処理
@clova.handle.launch
def launch_request_handler(clova_request):
    welcome_japanese = cek.Message(message="調子どうだい？", language="ja")
    response = clova.response([welcome_japanese])
    return response

# WifeStatusIntentの発火箇所
@clova.handle.intent("money_chan")
def wife_status_handler(clova_request):
    #message_japanese = cek.Message(message="奥さんの気分はいい感じです", language="ja")
    money_msg = clova_request.slot_value('money_chan')
    response
    if money_msg is not None:
        if money_msg == "差額"
            response = clova.response('差額は500円です)
             
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