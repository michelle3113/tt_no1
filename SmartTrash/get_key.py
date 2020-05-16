import requests

# client_id 为官网获取的AK， client_secret 为官网获取的SK
ak = 'Gfq2wb0ZOie8k503h0DGiHOs'
sk = 'FrYsQZDQD9mpWCRGKG7lxeTvVR0IRY6G'
host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ak}&client_secret={sk}'
response = requests.get(host)
if response:
    print(response.json())

request_url = "【接口地址】"


