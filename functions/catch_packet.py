# coding:utf-8
import json
import os


def writeCatchPacket(packet: dict, path: str):
    """ 将抓到的包保存到本地 """
    if not os.path.exists('data'):
        os.mkdir('data')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(packet, f)


def readCatchPacket(path: str) -> dict:
    """ 读取指定的数据包文件 """
    with open(path, encoding='utf-8') as f:
        packet = json.load(f)

    return packet
