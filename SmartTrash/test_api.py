# encoding:utf-8

import base64
import requests
import json

request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/garbage_sorting_new"
access_token = '24.95db6c6271434c2daa1653f9af027fee.2592000.1594530371.282335-17789337'
# request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/garbage_sort3"
# access_token = '24.543b730347d1e9f4ddca0809d0812763.2592000.1594365870.282335-20181039'

with open('ttt.jpg', 'rb') as fp:
    img = base64.b64encode(fp.read())
params = {"image": img.decode()}

request_url = request_url + "?access_token=" + access_token
headers = {'Content-Type': 'application/json'}
response = requests.post(request_url, data=json.dumps(params), headers=headers)
print(response.json())
