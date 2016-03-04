#!/usr/local/bin/python3

from urllib.request import urlopen, Request

url = "http://www.google.com"
headers = {}
headers['User-Agent'] = "Googlebot"

request = Request(url, headers = headers)

res = urlopen(request)
print(res.read())
res.close()
