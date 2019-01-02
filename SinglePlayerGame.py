# -*- coding:utf-8 -*-
# @author: alex
# @time: 2018/12/30 8:40

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from my_games.DoublePlayerGame import Chessman
from my_games.DoublePlayerGame import WinLabel
from my_games.MyButton import MyButton
import sys
import random


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
        self.st_over = False
        self.history_chess = []
        # 白子得分
        self.machine_goal=[]

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

        self.focus_Point = Chessman(color='white', parent=self)
        self.focus_Point.pic = QPixmap('source/标识.png')
        self.focus_Point.setPixmap(self.focus_Point.pic)
        self.focus_Point.setFixedSize(self.focus_Point.pic.size())
        self.focus_Point.hide()

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
                n = self.history_chess.pop()
                m.close()
                n.close()

                self.focus_Point.hide()

                self.chess_map[m.map_point_x][m.map_point_y] = None
                self.chess_map[n.map_point_x][n.map_point_y] = None

                if self.color_flag == 1:
                    self.color_flag = 0
                #     self.player.pic = QPixmap('source/白手.png')
                # else:
                #     self.player.pic = QPixmap('source/黑手.png')
                # self.player.setPixmap(self.player.pic)
                # self.player.setFixedSize(self.player.pic.size())
                # self.player.move(700, 580)
                # self.player.show()
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
        # mychessman = QLabel(self)
        # mychessman.setPixmap(QPixmap('source/黑子.png'))
        # mychessman.move(a0.pos())
        # mychessman.show()

        if self.color_flag == 0:
            self.chessman = Chessman(color='black', parent=self)
            self.color_flag = 1
        else:
            self.chessman = Chessman(color='white', parent=self)
            self.color_flag = 0

        pos = self.reversePos(a0.pos())
        if self.st_over == True:
            return
        if pos == None:
            return
        pos_x = pos.x()
        pos_y = pos.y()
        self.chessman.move(pos_x, pos_y)
        self.chessman.map_point_x = (self.chessman.y - 50) // 30
        self.chessman.map_point_y = (self.chessman.x - 50) // 30
        #      此时:0是白色
        #      1是黑色
        if self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y] != None:
            if self.color_flag == 1:
                self.color_flag = 0
            else:
                self.color_flag = 1
            return
        self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y] = self.chessman
        # 显示标识
        self.focus_Point.move(pos_x, pos_y)
        self.focus_Point.show()
        self.focus_Point.raise_()

        self.chessman.show()

        # if self.color_flag == 1:
        #     self.player.pic = QPixmap('source/白手.png')
        # else:
        #     self.player.pic = QPixmap('source/黑手.png')
        # self.player.setPixmap(self.player.pic)
        # self.player.setFixedSize(self.player.pic.size())
        # self.player.move(700, 580)
        # self.player.show()

        self.history_chess.append(self.chessman)
        self.showWin()
        self.machinePlay()


        print(self.chessman.color)
        print(self.color_flag)
        self.showWin()

        print(self.chess_map)

    # 棋子坐标转换，棋子坐标判断
    # 如果返回None则不是一个有效位置，
    # 如果返回坐标，实际的坐标位置

    # def show

    def reversePos(self, pos):
        pos_x = pos.x()
        pos_y = pos.y()

        # 判断低级位置是否在棋盘内部，如果不是则返回None
        # 棋盘的左边界：x: 50-15=35
        # 棋盘的右边界：x: 50+18*30=590+15
        # 棋盘的上边界：y: 50-15=35
        # 棋盘的下边界：y: 590+15

        if pos_x <= 35 or pos_x >= 605 or pos_y <= 35 or pos_y >= 605:
            return None

        return pos

    def showWin(self):
        if self.whoIsWiner(self.chessman) == True:
            if self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y].color == 'white':
                self.win_lbl = WinLabel(color='white', parent=self)
                self.win_lbl.move(100, 100)
                print('白棋 胜利')
                self.win_lbl.show()
                self.st_over = True
            elif self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y].color == 'black':
                self.win_lbl = WinLabel(color='black', parent=self)
                self.win_lbl.move(100, 100)
                self.win_lbl.show()
                print('黑棋 胜利')
                self.st_over = True

    def whoIsWiner(self, chessman):
        x = chessman.map_point_x
        y = chessman.map_point_y

        # 横向
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x][y + 1].color, self.chess_map[x][y + 2].color,
                          self.chess_map[x][y + 3].color, self.chess_map[x][y + 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x][y + 1].color, self.chess_map[x][y + 2].color,
                          self.chess_map[x][y + 3].color, self.chess_map[x][y - 1].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x][y + 1].color, self.chess_map[x][y + 2].color,
                          self.chess_map[x][y - 1].color, self.chess_map[x][y - 2].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x][y + 1].color, self.chess_map[x][y - 1].color,
                          self.chess_map[x][y - 2].color, self.chess_map[x][y - 3].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x][y - 1].color, self.chess_map[x][y - 2].color,
                          self.chess_map[x][y - 3].color, self.chess_map[x][y - 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")

        # 竖向-----------------------------------------------------------------------------------------
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y].color, self.chess_map[x + 2][y].color,
                          self.chess_map[x + 3][y].color, self.chess_map[x + 4][y].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y].color, self.chess_map[x + 2][y].color,
                          self.chess_map[x + 3][y].color, self.chess_map[x - 1][y].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y].color, self.chess_map[x + 2][y].color,
                          self.chess_map[x - 1][y].color, self.chess_map[x - 2][y].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y].color, self.chess_map[x - 1][y].color,
                          self.chess_map[x - 2][y].color, self.chess_map[x - 3][y].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")

        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y].color, self.chess_map[x - 2][y].color,
                          self.chess_map[x - 3][y].color, self.chess_map[x - 4][y].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")

        # 斜降--------------------------------------------------------------------------------------------------------------
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y + 1].color, self.chess_map[x + 2][y + 2].color,
                          self.chess_map[x + 3][y + 3].color, self.chess_map[x + 4][y + 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y + 1].color, self.chess_map[x + 2][y + 2].color,
                          self.chess_map[x + 3][y + 3].color, self.chess_map[x - 1][y - 1].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y + 1].color, self.chess_map[x + 2][y + 2].color,
                          self.chess_map[x - 1][y - 1].color, self.chess_map[x - 2][y - 2].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y + 1].color, self.chess_map[x - 1][y - 1].color,
                          self.chess_map[x - 2][y - 2].color, self.chess_map[x - 3][y - 3].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")

        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y - 1].color, self.chess_map[x - 2][y - 2].color,
                          self.chess_map[x - 3][y - 3].color, self.chess_map[x - 4][y - 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")

        #  斜升-----------------------------------------------------------------------------------------------------------------------
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y + 1].color, self.chess_map[x - 2][y + 2].color,
                          self.chess_map[x - 3][y + 3].color, self.chess_map[x - 4][y + 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y + 1].color, self.chess_map[x - 2][y + 2].color,
                          self.chess_map[x - 3][y + 3].color, self.chess_map[x + 1][y - 1].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y + 1].color, self.chess_map[x - 2][y + 2].color,
                          self.chess_map[x + 1][y - 1].color, self.chess_map[x + 2][y - 2].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y + 1].color, self.chess_map[x + 1][y - 1].color,
                          self.chess_map[x + 2][y - 2].color, self.chess_map[x + 3][y - 3].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y - 1].color, self.chess_map[x + 2][y - 2].color,
                          self.chess_map[x + 3][y - 3].color, self.chess_map[x + 4][y - 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")

    def machinePlay(self):
        while True:
            if self.color_flag == 0:
                self.chessman = Chessman(color='black', parent=self)
                self.color_flag = 1
            else:
                self.chessman = Chessman(color='white', parent=self)
                self.color_flag = 0
            m_x = random.randint(50, 50 + 18 * 30 + 1)
            m_y = random.randint(50, 50 + 18 * 30 + 1)
            self.chessman.x, self.chessman.y = self.chessman.adjust_point(m_x, m_y)
            self.chessman.map_point_x = (self.chessman.y - 50) // 30
            self.chessman.map_point_y = (self.chessman.x - 50) // 30
            if self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y] == None:
                self.chessman.move(m_x, m_y)
                self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y] = self.color_flag
                self.chessman.show()
                # 显示标识
                self.focus_Point.move(m_x, m_y)
                self.focus_Point.show()
                self.focus_Point.raise_()

                self.history_chess.append(self.chessman)
                print(self.color_flag)
                return
            else:
                if self.color_flag == 1:
                    self.color_flag = 0
                else:
                    self.color_flag = 1


    # def goal_comput(self,chessman):
    #
    #
    #     x = chessman.map_point_x
    #     y = chessman.map_point_y
    #     # 横向
    #     try:
    #         list_chess = [self.chess_map[x][y], self.chess_map[x][y + 1], self.chess_map[x][y + 2],
    #                       self.chess_map[x][y + 3], self.chess_map[x][y + 4]]
    #         goal =list_chess.count(self.color_flag)
    #         self.machine_goal.append(goal)
    #     except Exception as e:
    #         print(e)
    #     try:
    #         list_chess = [self.chess_map[x][y], self.chess_map[x][y + 1], self.chess_map[x][y + 2],
    #                       self.chess_map[x][y + 3], self.chess_map[x][y - 1]]
    #         if len(set(list_chess)) == 1:
    #             return True
    #     except Exception:
    #         print("error")
    #     try:
    #         list_chess = [self.chess_map[x][y], self.chess_map[x][y + 1], self.chess_map[x][y + 2],
    #                       self.chess_map[x][y - 1], self.chess_map[x][y - 2]]
    #         goal = list_chess.count(self.color_flag)
    #         self.machine_goal.append(goal)
    #     except Exception as e:
    #         print(e)
    #     try:
    #         list_chess = [self.chess_map[x][y], self.chess_map[x][y + 1], self.chess_map[x][y - 1],
    #                       self.chess_map[x][y - 2], self.chess_map[x][y - 3]]
    #         goal = list_chess.count(self.color_flag)
    #         self.machine_goal.append(goal)
    #     except Exception as e:
    #         print(e)
    #     try:
    #         list_chess = [self.chess_map[x][y], self.chess_map[x][y - 1], self.chess_map[x][y - 2],
    #                       self.chess_map[x][y - 3], self.chess_map[x][y - 4]]
    #         goal = list_chess.count(self.color_flag)
    #         self.machine_goal.append(goal)
    #     except Exception as e:
    #         print(e)
    #
    #         # 竖向-----------------------------------------------------------------------------------------
    #         try:
    #             list_chess = [self.chess_map[x][y], self.chess_map[x + 1][y], self.chess_map[x + 2][y],
    #                           self.chess_map[x + 3][y], self.chess_map[x + 4][y]]
    #             goal = list_chess.count(self.color_flag)
    #             self.machine_goal.append(goal)
    #         except Exception as e:
    #             print(e)
    #         try:
    #             list_chess = [self.chess_map[x][y], self.chess_map[x + 1][y], self.chess_map[x + 2][y],
    #                           self.chess_map[x + 3][y], self.chess_map[x - 1][y]]
    #             goal = list_chess.count(self.color_flag)
    #             self.machine_goal.append(goal)
    #         except Exception as e:
    #             print(e)
    #         try:
    #             list_chess = [self.chess_map[x][y], self.chess_map[x + 1][y], self.chess_map[x + 2][y],
    #                           self.chess_map[x - 1][y], self.chess_map[x - 2][y]]
    #             goal = list_chess.count(self.color_flag)
    #             self.machine_goal.append(goal)
    #         except Exception as e:
    #             print(e)
    #         try:
    #             list_chess = [self.chess_map[x][y], self.chess_map[x + 1][y], self.chess_map[x - 1][y],
    #                           self.chess_map[x - 2][y], self.chess_map[x - 3][y]]
    #             goal = list_chess.count(self.color_flag)
    #             self.machine_goal.append(goal)
    #         except Exception as e:
    #             print(e)
    #
    #         try:
    #             list_chess = [self.chess_map[x][y], self.chess_map[x - 1][y], self.chess_map[x - 2][y],
    #                           self.chess_map[x - 3][y], self.chess_map[x - 4][y]]
    #             goal = list_chess.count(self.color_flag)
    #             self.machine_goal.append(goal)
    #         except Exception as e:
    #             print(e)
    #
    #             # 斜降--------------------------------------------------------------------------------------------------------------
    #             try:
    #                 list_chess = [self.chess_map[x][y], self.chess_map[x + 1][y + 1], self.chess_map[x + 2][y + 2],
    #                               self.chess_map[x + 3][y + 3], self.chess_map[x + 4][y + 4]]
    #                 goal = list_chess.count(self.color_flag)
    #                 self.machine_goal.append(goal)
    #             except Exception as e:
    #                 print(e)
    #             try:
    #                 list_chess = [self.chess_map[x][y], self.chess_map[x + 1][y + 1], self.chess_map[x + 2][y + 2],
    #                               self.chess_map[x + 3][y + 3], self.chess_map[x - 1][y - 1]]
    #                 goal = list_chess.count(self.color_flag)
    #                 self.machine_goal.append(goal)
    #             except Exception as e:
    #                 print(e)
    #             try:
    #                 list_chess = [self.chess_map[x][y], self.chess_map[x + 1][y + 1], self.chess_map[x + 2][y + 2],
    #                               self.chess_map[x - 1][y - 1], self.chess_map[x - 2][y - 2]]
    #                 goal = list_chess.count(self.color_flag)
    #                 self.machine_goal.append(goal)
    #             except Exception as e:
    #                 print(e)
    #             try:
    #                 list_chess = [self.chess_map[x][y], self.chess_map[x + 1][y + 1], self.chess_map[x - 1][y - 1],
    #                               self.chess_map[x - 2][y - 2], self.chess_map[x - 3][y - 3]]
    #                 goal = list_chess.count(self.color_flag)
    #                 self.machine_goal.append(goal)
    #             except Exception:
    #                 print(e)
    #
    #             try:
    #                 list_chess = [self.chess_map[x][y], self.chess_map[x - 1][y - 1], self.chess_map[x - 2][y - 2],
    #                               self.chess_map[x - 3][y - 3], self.chess_map[x - 4][y - 4]]
    #                 goal = list_chess.count(self.color_flag)
    #                 self.machine_goal.append(goal)
    #             except Exception as e:
    #                 print(e)









if __name__ == '__main__':
    import cgitb

    # 防止程序异常退出
    cgitb.enable(format='text')
    a = QApplication(sys.argv)
    m = SinglePlayerGame()
    m.show()
    sys.exit(a.exec_())
