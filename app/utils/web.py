# -*- coding: utf-8 -*-
import requests
from urllib import parse

from app import current_config

"""
使用网络上其他 api 的工具函数
"""


def short_the_url(url: str):
    """使用短链服务"""
    parse.urlsplit(url)  # 解析失败会抛 error

    params = {
        'token': current_config.SHORT_URL_TOKEN,  # 美人提供的接口，这个是token
        'url': url,
    }
    result = requests.get(current_config.SHORT_URL_API, params=params)

    return result.json()["short_url"]


def char_zdict_url(chars: str):
    """查询汉典"""
    return short_the_url('http://m.zdic.net/s/?q=' + parse.quote(chars))


def talk(message: str, user_id, group_id=None, username=None):
    """图灵聊天服务"""
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": message
            }
        },
        "userInfo": {
            "apiKey": current_config.TURING_KEY,
            "userId": user_id,
            "groupId": group_id,
            "userIdName": username,
        }
    }

    resp = requests.post(url=current_config.TURING_API, json=data).json()

    # 分析返回值
    code = resp['intent']["code"]
    if code < 10000:  # 异常
        return "异常状况，即将崩坏。9 8 7..."

    codes_text_only = [  # 可以直接输出的 code
        10004,  # 聊天
        10008,  # 天气
        10009,  # 计算
        10010,  # 故事
        10011,  # 成语接龙
        10013,  # 百科
        10016,  # 快递查询
        10019,  # 日期
        10020,  # 翻译
        10022,  # 脑筋急转弯
        10030,  # 歇后语
        10031,  # 绕口令
        10032,  # 顺口溜
        10033,  # 邮编
        10034,  # 自定义语料库
        10041,  # 星座运势（包含多个）
    ]
    if code in codes_text_only:  # 可以直接输出
        return resp['results'][0]["values"]['text']

    return "暂不提供该功能"


