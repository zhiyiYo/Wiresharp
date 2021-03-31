# coding:utf-8
import json
import os


def writeCatchPacket(packet: dict, path: str):
    """ 将抓到的包保存到本地 """
    if not os.path.exists('app\\data'):
        os.mkdir('app\\data')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(packet, f)


def readCatchPacket(path: str) -> dict:
    """ 读取指定的数据包文件 """
    # 文件不存在时返回None
    if not os.path.exists(path):
        return None

    with open(path, encoding='utf-8') as f:
        packet = json.load(f)
    return packet
