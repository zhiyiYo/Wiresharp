# coding: utf-8
from paho.mqtt.client import Client
from PyQt5.QtCore import QThread, pyqtSignal


class PublishThread(QThread):
    """ 发布消息 """

    publishStateChangedSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.client = Client()
        self.client.on_connect = self.on_connect

    def run(self):
        """ 发布消息 """
        self.client.connect(self.broker, 1883)
        self.client.loop_forever()

    def publish(self, broker: str, topic: str, message: str):
        """ 发布消息

        Parameters
        ----------
        broker : str
            代理服务器 IP 地址

        topic : str
            订阅主题

        message : str
            消息
        """
        self.topic = topic
        self.broker = broker
        self.message = message
        self.publishStateChangedSignal.emit('🙈 正在连接代理服务器...')
        self.start()

    def on_connect(self, client: Client, userdata, flags, rc, properties=None):
        """ mqtt连接回调函数 """
        status = ['连接成功', '协议版本错误', '客户端标识符无效',
                  '服务器不可用', '用户名或密码错误', '未授权']
        if rc != 0:
            self.publishStateChangedSignal.emit(status[rc])
            return
        # 发布信息并发送消息给主界面
        self.publishStateChangedSignal.emit('🙉 代理服务器连接成功！')
        client.publish(self.topic, self.message, 1)
        self.publishStateChangedSignal.emit('🙊 假数据包发送成功！')
        client.disconnect()
        self.publishStateChangedSignal.emit(
            f'🙊 已与代理服务器 {self.broker} 断开连接')
