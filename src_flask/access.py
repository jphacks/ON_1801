# coding: utf-8
 
import urllib
import webbrowser

import requests
from requests.auth import OAuth1
import oauth2 as oauth
 
request_token_url = 'https://api.zaim.net/v2/auth/request'
access_token_url = 'https://api.zaim.net/v2/auth/access'
authenticate_url = 'https://auth.zaim.net/users/auth'
callback_uri = 'https://www.zaim.net/'
callback_url = 'https://www.zaim.net/'
# callback_uri = 'oob'
consumer_key = '5a16dc78b738134b766719315527fd7b639ac87f'
consumer_secret = '9b53494758fb485c09e0587d4694c49ac1ad6e7f'
 


def get_request_token():
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    client = oauth.Client(consumer)
 
    # get the request_token
    resp, content = client.request('%s?&oauth_callback=%s' % (request_token_url, callback_url))
    request_token = dict(parse_qsl(content))
    if 'oauth_token_secret' in request_token:
        print ('OAuth Token Secret: %s' % request_token['oauth_token_secret'])
        print ('OAuth Token : %s' % request_token['oauth_token'])
    else:
        print ('not secret')
        return
    return request_token['oauth_token']
 
def parse_qsl(url):
    param = {}
    for i in url.split(b'&'):
        _p = i.split(b'=')
        param.update({_p[0]: _p[1]})
    return param
 
def get_access_token(oauth_token, oauth_verifier):
    customer = oauth.Consumer(key=consumer_key, secret=consumenr_secret)
    token = oauth.Token(oauth_token, oauth_verifier)
 
    client = oauth.Client(consumer, token)
    resp, content = client.request(access_token_url, "POST", body="oauth_verifier={0}".format(oauth_verifier))
    return content
 
# main
## request tokenを取得
request_token = get_request_token()
 
## request_tokenを認証URLにつけて認証URLを生成する
authorize_url = '%s?oauth_token=%s' % (authenticate_url, request_token)
print ('Authorize url: %s' % authorize_url)



# def oauth_requests():
#     # Get request token
#     auth = OAuth1(consumer_key, consumer_secret, callback_uri=callback_uri)
#     r = requests.post(request_token_url, auth=auth)
#     request_token = dict(urlparse.parse_qsl(r.text))
# 
#     webbrowser.open('%s?oauth_token=%s&perms=delete' % (authenticate_url, request_token_url['oauth_token']))  # ブラウザを開きOAuth認証確認画面を表示 ユーザーが許可するとPINコードが表示される
# 
#     auth = OAuth1(
#         consumer_key,
#         consumer_secret,
#         request_token['oauth_token'],
#         request_token['oauth_token_secret'])
#     r = requests.post(access_token_url, auth=auth)
# 
#     access_token = dict(urlparse.parse_qsl(r.text))
#     return access_token
# 
# # if __name__ == '__main__':
# #print (oauth_requests())
#         
