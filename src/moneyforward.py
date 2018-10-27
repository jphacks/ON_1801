#! /usr/bin/env python
# -*- coding: utf-8 -*-

import doctest
import requests
import urllib.request

token = open("token.txt", "r").read()
text = token.replace('\n','')
url = 'https://invoice.moneyforward.com/api/v1/office.json'
headers = { 'SampleToken': text }

get = requests.get(url, headers=headers)

