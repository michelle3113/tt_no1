# encoding:utf-8
import urllib2

'''
easydl物体检测
'''

request_url = "【接口地址】"



params = "{\"image\":\"sfasq35sadvsvqwr5q...\"}"

access_token = '[调用鉴权接口获取的token]'
request_url = request_url + "?access_token=" + access_token
request = urllib2.Request(url=request_url, data=params)
request.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(request)
content = response.read()
if content:
    print(content)