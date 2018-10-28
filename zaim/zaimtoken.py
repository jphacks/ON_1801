import urllib
import webbrowser

import requests
from requests_oauthlib import OAuth1


API_KEY = 'dummy_ApiKey'
SECRET_KEY = 'dummy_SecretKey'

request_url = 'https://api.zaim.net/v2/auth/request'
authorize_url = 'https://auth.zaim.net/users/auth'
access_token_url = 'https://api.zaim.net/v2/auth/access'
access_url = 'https://api.zaim.net/v2/auth/access'
callback_uri = 'oob'


def oauth_requests():
    # Get request token
    auth = OAuth1(API_KEY, SECRET_KEY, callback_uri=callback_uri)
    r = requests.post(request_url, auth=auth)
    request_token = dict(urllib.parse.parse_qsl(r.text))

    print(request_token)

    # Getting the User Authorization
    webbrowser.open('%s?oauth_token=%s&perms=delete' % (authorize_url, request_token['oauth_token']))  # ブラウザを開きOAuth認証確認画面を表示 ユーザーが許可するとPINコードが表示される

    oauth_verifier = input("Please input PIN code:")  # 上記PINコードを入力する
    auth = OAuth1(
        API_KEY,
        SECRET_KEY,
        request_token['oauth_token'],
        request_token['oauth_token_secret'],
        verifier=oauth_verifier)
    r = requests.post(access_token_url, auth=auth)

    access_token = dict(urllib.parse_qsl(r.text))
    return access_token

if __name__ == '__main__':
    print(oauth_requests()) 
