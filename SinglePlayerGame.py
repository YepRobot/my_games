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
    # 信号量
    backSignal = pyqtSignal()  # 返回按钮
    startSignal = pyqtSignal()  # 开始按钮
    undoSignal = pyqtSignal()  # 悔棋按钮
    ggSignal = pyqtSignal()  # 认输按钮

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(760, 650)
        self.setWindowTitle('人机对战')
        self.setWindowIcon(QIcon('source/icon.ico'))
        self.color_flag = 'black'

        self.chess_map = [[None] * 19 for _ in range(19)]
        self.st_over = True
        self.history_chess = []
        # 白子得分
        self.machine_goal = []

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
        try:
            self.win_lbl.close()
        except Exception as e:
            print(e)
        self.st_over = False
        self.history_chess.clear()
        for i in range(0, 19):
            for j in range(0, 19):
                m = self.chess_map[i][j]
                if m is not None:
                    m.close()
                    self.chess_map[i][j] = None
                    self.focus_Point.hide()
        self.color_flag = 'black'

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

                if self.color_flag == 'black':
                    self.color_flag = 'white'
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
        if self.st_over==True:
            return
        if self.color_flag == 'black':
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

        if self.color_flag == 'black':
            self.chessman = Chessman(color='black', parent=self)
            self.color_flag = 'white'
        else:
            self.chessman = Chessman(color='white', parent=self)
            self.color_flag = 'black'

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
            if self.color_flag == 'black':
                self.color_flag = 'white'
            else:
                self.color_flag = 'black'
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
        self.autoDown()
        self.showWin()

        print(self.chessman.color)
        print(self.color_flag)

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
                return
            elif self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y].color == 'black':
                self.win_lbl = WinLabel(color='black', parent=self)
                self.win_lbl.move(100, 100)
                self.win_lbl.show()
                print('黑棋 胜利')
                self.st_over = True
                return

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
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y + 1].color,
                          self.chess_map[x + 2][y + 2].color,
                          self.chess_map[x + 3][y + 3].color, self.chess_map[x + 4][y + 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y + 1].color,
                          self.chess_map[x + 2][y + 2].color,
                          self.chess_map[x + 3][y + 3].color, self.chess_map[x - 1][y - 1].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y + 1].color,
                          self.chess_map[x + 2][y + 2].color,
                          self.chess_map[x - 1][y - 1].color, self.chess_map[x - 2][y - 2].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y + 1].color,
                          self.chess_map[x - 1][y - 1].color,
                          self.chess_map[x - 2][y - 2].color, self.chess_map[x - 3][y - 3].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")

        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y - 1].color,
                          self.chess_map[x - 2][y - 2].color,
                          self.chess_map[x - 3][y - 3].color, self.chess_map[x - 4][y - 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")

        #  斜升-----------------------------------------------------------------------------------------------------------------------
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y + 1].color,
                          self.chess_map[x - 2][y + 2].color,
                          self.chess_map[x - 3][y + 3].color, self.chess_map[x - 4][y + 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y + 1].color,
                          self.chess_map[x - 2][y + 2].color,
                          self.chess_map[x - 3][y + 3].color, self.chess_map[x + 1][y - 1].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y + 1].color,
                          self.chess_map[x - 2][y + 2].color,
                          self.chess_map[x + 1][y - 1].color, self.chess_map[x + 2][y - 2].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x - 1][y + 1].color,
                          self.chess_map[x + 1][y - 1].color,
                          self.chess_map[x + 2][y - 2].color, self.chess_map[x + 3][y - 3].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")
        try:
            list_chess = [self.chess_map[x][y].color, self.chess_map[x + 1][y - 1].color,
                          self.chess_map[x + 2][y - 2].color,
                          self.chess_map[x + 3][y - 3].color, self.chess_map[x + 4][y - 4].color]
            if len(set(list_chess)) == 1:
                return True
        except Exception:
            print("error")

    def getPointScore(self, x, y, color):
        '''
        返回每个点的得分
        y:行坐标
        x:列坐标
        color：棋子颜色
        :return:
        '''
        # 分别计算点周围5子以内，空白、和同色的分数
        blank_score = 0
        color_score = 0

        # 记录每个方向的棋子分数
        blank_score_plus = [0, 0, 0, 0]  # 横向 纵向 正斜线 反斜线
        color_score_plus = [0, 0, 0, 0]

        # 横线
        # 右侧
        i = x  # 横坐标
        j = y  # 纵坐标
        while i < 19:
            if self.chess_map[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
                break
            elif self.chess_map[j][i].color == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
        # print('123123')
        # 左侧
        i = x  # 横坐标
        j = y  # 纵坐标
        while i >= 0:
            if self.chess_map[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
                break
            elif self.chess_map[j][i].color == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1

        # 竖线
        # 上方
        i = x  # 横坐标
        j = y  # 纵坐标
        while j >= 0:
            if self.chess_map[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
                break
            elif self.chess_map[j][i].color == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break
            if j <= y - 4:
                break
            j -= 1
        # 竖线
        # 下方
        i = x  # 横坐标
        j = y  # 纵坐标
        while j < 19:
            if self.chess_map[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
                break
            elif self.chess_map[j][i].color == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break

            if j >= y + 4:  # 最近五个点
                break
            j += 1
        # 正斜线
        # 右上
        i = x
        j = y
        while i < 19 and j >= 0:
            if self.chess_map[j][i] is None:
                blank_score += 1
                blank_score_plus[2] += 1
                break
            elif self.chess_map[j][i].color == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break

            if i >= x + 4:  # 最近五个点
                break
            i += 1
            j -= 1
        # 左下
        i = x
        j = y
        while j < 19 and i >= 0:
            if self.chess_map[j][i] is None:
                blank_score += 1
                blank_score_plus[2] += 1
                break
            elif self.chess_map[j][i].color == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break

            if j >= y + 4:  # 最近五个点
                break
            i -= 1
            j += 1
        # 反斜线
        # 左上
        i = x
        j = y
        while i >= 0 and j >= 0:
            if self.chess_map[j][i] is None:
                blank_score += 1
                blank_score_plus[3] += 1
                break
            elif self.chess_map[j][i].color == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1
            j -= 1
        # 右上
        i = x
        j = y
        while i < 19 and j < 19:
            if self.chess_map[j][i] is None:
                blank_score += 1
                blank_score_plus[3] += 1
                break
            elif self.chess_map[j][i].color == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
            j += 1

        for k in range(4):
            if color_score_plus[k] >= 5:
                return 100

        # color_score *= 5
        return max([x + y for x, y in zip(color_score_plus, blank_score_plus)])

    def getPoint(self):
        '''
        返回落子位置
        :return:
        '''
        # 简单实现：返回一个空白交点
        # for i in range(19):
        #     for j in range(19):
        #         if self.chess_map[i][j] == None:
        #             return QPoint(j, i)
        #
        #  没有找到合适的点
        white_score = [[0 for i in range(19)] for j in range(19)]
        black_score = [[0 for i in range(19)] for j in range(19)]

        for i in range(19):
            for j in range(19):
                if self.chess_map[i][j] != None:
                    continue
                # 模拟落子
                self.chess_map[i][j] = Chessman(color='white', parent=self)
                white_score[i][j] = self.getPointScore(j, i, 'white')
                self.chess_map[i][j].close()
                self.chess_map[i][j] = None
                self.chess_map[i][j] = Chessman(color='black', parent=self)
                black_score[i][j] = self.getPointScore(j, i, 'black')
                self.chess_map[i][j].close()
                self.chess_map[i][j] = None

        print('----------------')
        # 将二维坐标转换成以为进行计算
        r_white_score = []
        r_black_score = []
        for i in white_score:
            r_white_score.extend(i)
        for i in black_score:
            r_black_score.extend(i)

        # 找到分数最大值
        score = [max(x, y) for x, y in zip(r_white_score, r_black_score)]

        # 找到分数做大的下标
        chess_index = score.index(max(score))

        print(score, '\n', max(score))

        y = chess_index // 19
        x = chess_index % 19

        return QPoint(x, y)

    def autoDown(self):
        '''
        自动落子
        :return:
       '''
        if self.st_over==True:
            return
        point = self.getPoint()

        # 注意：x,y坐标对应
        chess_index = (point.y(), point.x())  # 棋子在棋盘中的下标
        pos = QPoint(50 + point.x() * 30, 50 + point.y() * 30)  # 棋子在棋盘中的坐标
        pos_x = pos.x()
        pos_y = pos.y()

        self.chessman = Chessman(color=self.color_flag, parent=self)
        # self.chessman.setIndex(chess_index[1], chess_index[0])
        self.chessman.move(pos_x, pos_y)
        self.chessman.show()  # 显示棋子

        # 显示标识
        self.focus_Point.move(pos_x, pos_y)
        self.focus_Point.show()
        self.focus_Point.raise_()

        self.chessman.map_point_x = chess_index[0]
        self.chessman.map_point_y = chess_index[1]
        print("zheshi" + str(self.chessman.map_point_x) + str(self.chessman.map_point_y))

        if self.chessman.color == 0:
            self.chessman.color = 'black'
        else:
            self.chessman.color = 'white'

        self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y] = self.chessman

        # 历史记录
        self.history_chess.append(self.chessman)

        # 改变落子颜色
        if self.color_flag == 'white':
            self.color_flag = 'black'
        else:
            self.color_flag = 'white'
        # 判断输赢

    def score(self, x, y, color):
        blank_score = [0, 0, 0, 0]
        chess_score = [0, 0, 0, 0]

        # 右方向
        for i in range(x, x + 5):
            if i >= 19:
                break
            if self.chess_map[i][y] is not None:
                if self.chess_map[i][y].color == color:
                    chess_score[0] += 1
                else:
                    break

            else:
                blank_score[0] += 1
                break

        # 左方向
        for i in range(x - 1, x - 5, -1):
            if i <= 0:
                break
            if self.chess_map[i][y] is not None:
                if self.chess_map[i][y].color == color:
                    chess_score[0] += 1
                else:
                    break
            else:
                blank_score[0] += 1
                break

        # 下方向
        for j in range(y, y + 5):
            if j >= 19:
                break
            if self.chess_map[x][j] is not None:
                if self.chess_map[x][j].color == color:
                    chess_score[0] += 1
                else:
                    break
            else:
                blank_score[0] += 1
                break

        # 上方向
        for i in range(y - 1, y - 5, -1):
            if i <= 0:
                break
            if self.chess_map[x][j] is not None:
                if self.chess_map[x][j].color == color:
                    chess_score[1] += 1
                else:
                    break
            else:
                blank_score[1] += 1
                break

        # 右下
        for i in range(x, x + 5):
            if i >= 19 or j >= 19:
                break
            if self.chess_map[i][j] is not None:
                if self.chess_map[i][j].color == color:
                    chess_score[2] += 1
                else:
                    break

            else:
                blank_score[2] += 1
                break

            j += 1

        # 左上
        for i in range(x - 1, x - 5, -1):
            if i <= 0 or j <= 0:
                break
            if self.chess_map[i][j] is not None:
                if self.chess_map[i][j].color == color:
                    chess_score[2] += 1
                else:
                    break
            else:
                blank_score[2] += 1
                break

            j -= 1

        # 左下
        for i in range(x, x - 5, -1):
            if i <= 0 or j >= 19:
                break
            if self.chess_map[i][j] is not None:
                if self.chess_map[i][j].color == color:
                    chess_score[3] += 1
                else:
                    break

            else:
                blank_score[3] += 1
                break
            j += 1

        # 右上
        for i in range(x + 1, x + 5):
            if i >= 19 or j <= 0:
                break
            if self.chess_map[i][j] is not None:
                if self.chess_map[i][j].color == color:
                    chess_score[3] += 1
                else:
                    break

            else:
                blank_score[3] += 1
                break
            j -= 1

        for score in chess_score:
            if score > 4:
                return 100
        for i in range(0, len(blank_score)):
            if blank_score[i] == 0:
                blank_score[i] -= 20

        result = [a + b for a, b in zip(chess_score, blank_score)]
        return max(result)


if __name__ == '__main__':
    import cgitb

    # 防止程序异常退出
    cgitb.enable(format='text')
    a = QApplication(sys.argv)
    m = SinglePlayerGame()
    m.show()
    sys.exit(a.exec_())
