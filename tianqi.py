#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 导入requests包
import requests
import time
import json
import datetime

## 要发送的微信号，上面关注公众号得到的， 改成自己的
touser="owD_b6Q7lPExJuthVp_KO2-R6yk4"
## 消息模板ID， 改成自己的
# template_id="uc6Vw1wy2HS1IANwpqhvRHleRTpHG1Bp5lkOCD1xkX4"
template_id="AU_kAouzOOZX4UjYanoDKWzBRHTXIN1-mrPhFGa364w"
## 微信开发者的 appID， 改成自己的
wx_appid = "wx41b5362617d44312"
## 微信开发者的 appsecret， 改成自己的
wx_secret = "98cab0f6e6a1a7f0f488867b2576a594"
## 获取token的URL，不用改
wx_token_url = "https://api.weixin.qq.com/cgi-bin/token"


## 获取天气URL， 不用改
we_url = "https://devapi.qweather.com/v7/weather/3d"

caihongpi_url="https://apis.tianapi.com/caihongpi/index"

## 和风天气项目的key， 改成自己的
we_key ="26b8243b01a64a2ba34978634c68ac2b"
caihongpi_key ='59e6408c7212b9f2d1a23dd1cb20ecc3'
## 和风天气的地市代码，从这里查 https://github.com/qwd/LocationList/blob/master/POI-Air-Monitoring-Station-List-latest.csv， 
## 或者调用API查询， 文档参考：https://dev.qweather.com/docs/api/geoapi/
we_location = "101120206"

## 微信消息URL， 不用改
msg_url ="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token="

def send_msg():
    ourday="2022-03-15"
    # current_time = time.localtime()
    # # print(current_time)
    # alarm_time = (10, 0, 0) 
    # time_difference = time.mktime(alarm_time) - time.mktime(current_time) 
    # time.sleep(time_difference)
    our_date=datetime.datetime.strptime(ourday,"%Y-%m-%d")
    curr_datetime=datetime.datetime.now()
    minus_date=curr_datetime-our_date
    print(minus_date.days)

    # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
    my_params = {"grant_type":"client_credential","appid":wx_appid, "secret": wx_secret}
    ## 请求获取token
    res = requests.get(url=wx_token_url, params=my_params)
    print("微信token:",res.text)  # 返回请求结果

    if res.json()['access_token'] == "":
        return "微信Token失败"
    we_param = {"location":we_location,"key": we_key}
    ## 请求获取天气
    we_res = requests.get(url=we_url, params=we_param)
    print("天气返回:",we_res.text)
    if we_res.json()['code'] != '200':
        return "获取天气失败"
    caihongpi_param = {"location":we_location,"key": caihongpi_key}
    caihongpi_res = requests.get(url=caihongpi_url, params=caihongpi_param)
    print("彩虹屁返回:",caihongpi_res.text)
    caihong_data =  caihongpi_res.json()['result']
    print(caihong_data)
    
    we_data =  we_res.json()['daily'][0]
    print("天气返回:",we_data)
    ## 发送模板消息
    cur_time = time.time()
    msg_id = str(int(cur_time))
    ## 组装微信模版消息的数据
    send_json = {
            "touser":touser,
            "template_id":template_id,
            "url":"https://www.qweather.com/",
            "client_msg_id": msg_id,
            "data":{
                "aini": {
                    "value":"乖乖，我爱你哦",
                    "color":"#148526"
                },
                "fxDate": {
                    "value":we_data['fxDate'],
                    "color":"#173177"
                },
                "textDay":{
                    "value":we_data['textDay'],
                    "color":"#173177"
                },
                "textNight": {
                    "value":we_data['textNight'],
                    "color":"#173177"
                },
                "tempMax": {
                    "value":we_data['tempMax'],
                    "color":"#173177"
                },
                "tempMin":{
                    "value":we_data['tempMin'],
                    "color":"#173177"
                },
                "riqi":{
                    "value":minus_date.days,
                    "color":"#175866"
                },
                "caihong":{
                    "value":caihong_data['content'],
                    # "color":"#173177"
                    "color":"#175866"
                }
            }
        }
    ## 发送微信模版消息
    msg_res = requests.post(url=msg_url+res.json()['access_token'],data=json.JSONEncoder().encode(send_json))
    print("消息返回:",msg_res.text)
    if msg_res.json()['errcode'] == 0:
        return "发送成功"
    return "发送失败"
print(send_msg())
