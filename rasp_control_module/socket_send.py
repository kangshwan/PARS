#! /usr/bin/python2
#-*-coding:utf-8-*-
import requests  
import json
url = "http://ec2-13-209-7-55.ap-northeast-2.compute.amazonaws.com:8080/dogfeed/main/"
url = "http://ec2-13-209-7-55.ap-northeast-2.compute.amazonaws.com:8080/dogfeed/ourdog/"
data = {'data':{'name':'뽀삐','weight':'100', 'time': "2020-06-18 18:00:00.000000"}}
headers = {'content-type': 'application/json'}
r=requests.post(url, data=json.dumps(data).encode('utf-8'), headers=headers)
print(r)

class Http():
	def __init__(self, url, name, weight, time):
		data = {'data':{'name':name, 'weight':weight, 'time': time}}
		headers = {'content-type': 'application/json'}
	def send_json(self):
		r=request.post(url, data=json.dumps(data).encode('utf-8'), headers=headers)
		return r
