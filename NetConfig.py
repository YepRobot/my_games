# -*- coding:utf-8 -*-
# @author: alex  
# @time: 2019/1/2 16:43


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class NetConfigWidget(QWidget):
    config_signal = pyqtSignal([str, str, str, str])

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

if __name__ == '__main__':
    import sys

    import cgitb

    cgitb.enable(format='text')
    app = QApplication(sys.argv)
    m = NetConfigWidget()
    m.show()
    sys.exit(app.exec_())
