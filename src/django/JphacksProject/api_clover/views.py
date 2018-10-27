from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from cek import (Clova, SpeechBuilder, ResponseBuilder,)
line_bot_api = LineBotApi(
    'アクセストークン(ロングターム)'
)

clova = Clova(application_id='Extension ID', default_language='ja')

@clova.handle.launch
def launch_request_handler(clova_request):
    return clova.response('お金管理ちゃんを起動します。')

@clova.handle.default
def dafault_handler(clova_request):
    return clova.response('もう一回行ってね')

@clova.handle.intent('money_chan')
def money_chan_handler(clova_request):
    money_chan = clova_request.slot_value('money_chan')
    if money_chan is not None:
        if money_chan == '差額':
            response = clova.response('差額は¥5000です')

        elif money_chan == 'いくら':
            response = clova.response('foo!!')

        elif money_chan == '残り':
            response = clova.response('hoge')

        else:
            response = clova.response('わけわからないよ')
    else:
        response = clova.response('もう一度お願いします')

    return response
if __name__ == '__main__':
    pass



