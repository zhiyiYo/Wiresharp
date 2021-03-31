# coding:utf-8
import os
import json
import socket


def getUserInfo():
    """ 读取用户信息 """
    if not os.path.exists('app\\config'):
        os.mkdir('app\\config')
    try:
        with open('app\\config\\user_info.json', encoding='utf-8') as f:
            userInfo = json.load(f)
    except:
        userInfo = {
            "userName": socket.gethostname(),
            "personalSignature": "うそじゃないよ",
            "headPortraitPath": r"app\resource\Image\head_portrait\硝子.jpg"
        }

    return userInfo


def writeUserInfo(userInfo: dict):
    """ 将用户信息写入到json文件中 """
    if not os.path.exists('app\\config'):
        os.mkdir('app\\config')
    with open('app\\config\\user_info.json', 'w', encoding='utf-8') as f:
        json.dump(userInfo, f)
