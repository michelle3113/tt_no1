# encoding:utf-8

import base64
import requests

request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/trashv2"
access_token = '24.5685fb55d448dae760a36d9aa57c4803.2592000.1592195411.282335-16678289'

with open('../tsne_vis/digits_tsne-generated.png', 'rb') as fp:
    img = base64.b64encode(fp.read())
params = {"image": img}

request_url = request_url + "?access_token=" + access_token
headers = {'Content-Type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
print(response.json())
