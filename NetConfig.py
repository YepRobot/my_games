# -*- coding:utf-8 -*-
# @author: alex  
# @time: 2019/1/2 16:43
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socket
import threading


class NetConfigWidget(QWidget):
    config_signal = pyqtSignal([str, str, str, str])  # 连接属性
    exit_signal = pyqtSignal()  # 退出信号

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("网络配置")

        self.name_label = QLabel('姓名', self)
        self.name_input = QLineEdit('玩家1', self)

        self.ip_label = QLabel('IP', self)
        self.ip_input = QLineEdit('127.0.0.1', self)

        self.port_label = QLabel('Port', self)
        self.port_input = QLineEdit('10086', self)

        self.client_button = QPushButton('连接主机', self)
        self.server_button = QPushButton('我是主机', self)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.name_label, 0, 0)
        grid_layout.addWidget(self.name_input, 0, 1)
        grid_layout.addWidget(self.ip_label, 1, 0)
        grid_layout.addWidget(self.ip_input, 1, 1)
        grid_layout.addWidget(self.port_label, 2, 0)
        grid_layout.addWidget(self.port_input, 2, 1)
        grid_layout.addWidget(self.client_button, 3, 0)
        grid_layout.addWidget(self.server_button, 3, 1)

        self.setLayout(grid_layout)  # 给窗口设置著布局

        self.client_button.clicked.connect(self.client_btn_slot)
        self.server_button.clicked.connect(self.server_btn_slot)

    def server_btn_slot(self):
        self.config_signal.emit('server', self.name_input.text(), self.ip_input.text(), self.port_input.text())

    def client_btn_slot(self):
        self.config_signal.emit('client', self.name_input.text(), self.ip_input.text(), self.port_input.text())

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.close()
        self.exit_signal.emit()


class NetClient(QObject):  # QObject是Qt中最基础的类

    msg_signal = pyqtSignal([str])

    def __init__(self,nettype, name, ip, port):
        super().__init__()
        self.nettype=nettype
        self.name = name
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def buildConnect(self):

        self.socket.connect((self.ip, int(self.port)))
        threading.Thread(target=self.recv).start()  # 启动线程接收数据

        pass

    def send(self, data):
        self.socket.send(data.encode())
        pass

    def recv(self):
        while True:
            try:
                data = self.socket.recv(4096).decode()
                self.msg_signal.emit(data)
            except:
                pass


class NetServer(QObject):
    msg_signal = pyqtSignal([str])

    def __init__(self,nettype, name, ip, port):
        super().__init__()
        self.nettype=nettype
        self.name = name
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cli_socket = None

    def buildConnect(self):
        self.socket.bind(('', int(self.port)))
        self.socket.listen(1)
        threading.Thread(target=self.__acceptConnect).start()

    def __acceptConnect(self):
        try:
            self.cli_socket, cli_addr = self.socket.accept()
        except:
            pass
        while True:
            try:

                data = self.cli_socket.recv(4096).decode()
                self.msg_signal.emit(data)
            except:
                pass

    def send(self, data):
        if self.cli_socket == None:
            return
        self.cli_socket.send(data.encode())


if __name__ == '__main__':
    import sys

    import cgitb

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    m = NetConfigWidget()
    m.show()
    sys.exit(app.exec_())
