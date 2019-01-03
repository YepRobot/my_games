# -*- coding:utf-8 -*-
# @author: alex  
# @time: 2019/1/3 9:35
from my_games.DoublePlayerGame import DoublePlayerGame


class NetPlayerGame(DoublePlayerGame):
    def __init__(self, net_object, parent=None):
        super().__init__(parent=parent)
        self.net_object = net_object
        self.net_object.buildConnect()  # 建立网络连接
        self.net_object.msg_signal.connect(self.parseData)

    def goBack(self):
        self.backSignal.emit()
        self.close()
        self.net_object.socket.close()

    def parseData(self, data):
        print(data)
