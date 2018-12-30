# -*- coding:utf-8 -*-
# @author: alex
# @time: 2018/12/30 8:40

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *

from my_games.DoublePlayerGame import WinLabel
from my_games.MyButton import MyButton
import sys









class SinglePlayerGame(QWidget):

    # 按钮信号量
    backSignal = pyqtSignal()  # 返回按钮
    startSignal = pyqtSignal()  # 开始按钮
    undoSignal = pyqtSignal()  # 悔棋按钮
    ggSignal = pyqtSignal()  # 认输按钮

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(760, 650)
        self.setWindowTitle('人机对战')
        self.setWindowIcon(QIcon('source/icon.ico'))
        self.color_flag = 0

        self.chess_map = [[None] * 19 for _ in range(19)]
        self.st_over=False
        self.history_chess=[]

        self.player = QLabel(self)
        self.player.pic = QPixmap('source/黑手.png')
        self.player.setPixmap(self.player.pic)
        self.player.setFixedSize(self.player.pic.size())
        self.player.move(700, 580)
        self.player.show()

        #  绘制背景图

        p = QPalette(self.palette())  # 获得当前的调色板
        brush = QBrush(QImage('source/游戏界面.png'))  # 画刷
        p.setBrush(QPalette.Background, brush)  # 设置调色板的背景色

        self.setPalette(p)  # 给窗口设置调色板
        self.move(300, 30)  # 窗口移动到中心

        self.return_to_main = MyButton('source/返回按钮_hover.png',
                                       'source/返回按钮_normal.png',
                                       'source/返回按钮_press.png', parent=self)
        self.return_to_main.move(650, 50)

        self.start_game = MyButton('source/开始按钮_hover.png',
                                   'source/开始按钮_normal.png',
                                   'source/开始按钮_press.png', parent=self)
        self.start_game.move(650, 200)

        self.undo_play = MyButton('source/悔棋按钮_hover.png',
                                  'source/悔棋按钮_normal.png',
                                  'source/悔棋按钮_press.png', parent=self)
        self.undo_play.move(650, 300)

        self.gg = MyButton('source/认输按钮_hover.png',
                           'source/认输按钮_normal.png',
                           'source/认输按钮_press.png', parent=self)
        self.gg.move(650, 400)

        self.return_to_main.clicked.connect(self.goBack)

        # 绑定开始按钮信号和槽函数
        self.start_game.clicked.connect(self.goStart)
        self.undo_play.clicked.connect(self.goUndo)
        self.gg.clicked.connect(self.goGG)

    def goBack(self):
        self.backSignal.emit()

    def goStart(self):
        self.startSignal.emit()
        self.close()

    def goUndo(self):
        try:
            if self.st_over != True:

                print('悔棋')
                m = self.history_chess.pop()
                m.close()
                self.chess_map[m.map_point_x][m.map_point_y] = None
                if self.color_flag == 1:
                    self.color_flag = 0
                else:
                    self.color_flag = 1
                if self.color_flag == 1:
                    self.player.pic = QPixmap('source/白手.png')
                else:
                    self.player.pic = QPixmap('source/黑手.png')
                self.player.setPixmap(self.player.pic)
                self.player.setFixedSize(self.player.pic.size())
                self.player.move(700, 580)
                self.player.show()
        except Exception as e:
            print(e)

    def goGG(self):
        if self.color_flag == 0:
            print("黑棋认输，白棋胜")
            self.win_lbl = WinLabel(color='white', parent=self)
            self.win_lbl.move(100, 100)
            self.win_lbl.show()
            self.st_over = True
        else:
            print("白棋认输 黑棋胜")
            self.win_lbl = WinLabel(color='black', parent=self)
            self.win_lbl.move(100, 100)
            self.win_lbl.show()
            self.st_over = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        print(a0.pos())
        print('x:', a0.x())
        print('y', a0.y())



if __name__ == '__main__':
    import cgitb

    # 防止程序异常退出
    cgitb.enable(format='text')
    a = QApplication(sys.argv)
    m = SinglePlayerGame()
    m.show()
    sys.exit(a.exec_())


