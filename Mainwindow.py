# -*- coding:utf-8 -*-
# @author: alex  
# @time: 2018/12/27 15:38

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from my_games.MyButton import MyButton
from my_games.DoublePlayerGame import DoublePlayerGame
from my_games.SinglePlayerGame import SinglePlayerGame
from my_games.NetConfig import *
import sys


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(760, 650)
        self.setWindowTitle('我的五子棋')
        self.setWindowIcon(QIcon('source/icon.ico'))

        p = QPalette(self.palette())  # 获得当前的调色板
        brush = QBrush(QImage('source/五子棋界面.png'))  # 画刷
        p.setBrush(QPalette.Background, brush)  # 设置调色板的背景色
        self.setPalette(p)  # 给窗口设置调色板
        self.move(300, 30)  # 窗口移动到中心

        self.btn1 = MyButton('source/人机对战_hover.png',
                             'source/人机对战_normal.png',
                             'source/人机对战_press.png', parent=self)
        self.btn1.move(270, 250)

        self.btn2 = MyButton('source/双人对战_hover.png',
                             'source/双人对战_normal.png',
                             'source/双人对战_press.png', parent=self)
        self.btn2.move(270, 350)

        self.btn3 = MyButton('source/联机对战_hover.png',
                             'source/联机对战_normal.png',
                             'source/联机对战_press.png', parent=self)
        self.btn3.move(270, 450)

        self.btn2.clicked.connect(self.startDoubleGame)
        self.btn1.clicked.connect(self.startSingleGame)
        self.btn3.clicked.connect(self.startNetGame)

    def startDoubleGame(self):
        #  构建双人对战游戏的界面
        self.double_player_game = DoublePlayerGame()
        self.double_player_game.backSignal.connect(self.showMain)
        self.double_player_game.startSignal.connect(self.startDoubleGame)
        self.double_player_game.show()
        self.close()

    def startSingleGame(self):
        self.single_player_game = SinglePlayerGame()
        self.single_player_game.backSignal.connect(self.showMain)
        self.single_player_game.startSignal.connect(self.startSingleGame)
        self.single_player_game.show()
        self.close()

    def startNetGame(self):

        self.netConfig = NetConfigWidget()
        self.netConfig.show()
        self.netConfig.exit_signal.connect(self.show)
        self.netConfig.config_signal.connect(self.recieveConfig)
        self.close()

    def recieveConfig(self, nettype, name, ip, port):
        print("net config", nettype, name, ip, port)

    def showMain(self):
        try:
            self.show()
            self.double_player_game.close()
        except Exception as e:
            print(e)
        try:
            self.show()
            self.single_player_game.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    import cgitb

    # 防止程序异常退出
    cgitb.enable(format='text')
    a = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    sys.exit(a.exec_())
