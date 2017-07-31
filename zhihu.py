#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
知乎模拟邮箱登录, 手动输入验证码, 验证码类型为点击图中所有倒立的文字
date: 20170731
'''
import requests
from PIL import Image
from matplotlib import pyplot
from bs4 import BeautifulSoup as BSoup
import time
import json
from io import BytesIO

# 信息预处理, 在 formdata 里填写密码和邮箱, 基本要发送的东西都在这里了
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
headers = {
    'Host': 'www.zhihu.com',
    'Origin': 'https://www.zhihu.com',
    'Referer': 'https://www.zhihu.com',
    'User-Agent': agent,
    'X-Requested-With': 'XMLHttpRequest',
    'X-Xsrftoken': ''
}
formdata = {
    '_xsrf': '',
    'password': '',  # 填写密码
    'captcha': '',
    'captcha_type': 'cn',
    'email': ''  # 填写邮箱
}
# 使用 requests.session 保存 cookie
session = requests.Session()

# 第一次访问知乎首页, header 只需要设置 user-agent
# 获取 _xsrf 和 X-Xsrftoken, 两个值是相同的, 一个用于 formdata, 一个用于header
response = session.get('https://www.zhihu.com/', headers={'User-Agent': agent})
soup = BSoup(response.text, 'html.parser')
xsrf = soup.select_one('input[name="_xsrf"]')['value']
formdata['_xsrf'] = xsrf
headers['X-Xsrftoken'] = xsrf

# 验证码处理, 没有验证码是不可能的, 验证码类型是选中图中所有倒立的文字, 参数类似于这样
# captcha:{"img_size":[200,44],"input_points":[[8.600006,11.600010000000001],[118.6,12.600010000000001]]}
# 验证码的 url 中参数 r 是时间值
t = str(int(time.time() * 1000))
captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login&lang=cn'
response = session.get(captcha_url, headers=headers)
captcha_gif = Image.open(BytesIO(response.content))

# 使用 matplotlib.pyplot 获得点击的位置
# https://matplotlib.org/2.0.2/api/pyplot_api.html?highlight=ginput#matplotlib.pyplot.ginput
pyplot.imshow(captcha_gif)
points = pyplot.ginput(2)
captcha = {'img_size': [200, 44], 'input_points': []}
for point in points:
    x, y = point
    x, y = round(x / 2, 2), round(y / 2, 2)
    captcha['input_points'].append([x, y])

formdata['captcha'] = json.dumps(captcha)

# 邮箱和密码
if not formdata['email']:
    formdata['email'] = input('输入你的邮箱: ')
    formdata['password'] = input('输入你的密码: ')

# 终于到这一步了, 所有的准备工作已经完成, 准备登录, 返回类型是json, 第一个值r是0就表示成功, 1是错误
response = session.post(
    'https://www.zhihu.com/login/email', data=formdata, headers=headers)

print(response.status_code)
print(response.text)

# 重新访问知乎首页, 验证是否真的已经登录
response = session.get('https://www.zhihu.com', headers=headers)
if '写文章' in response.text:
    print('登录成功')

if __name__ == '__main__':
    pass
