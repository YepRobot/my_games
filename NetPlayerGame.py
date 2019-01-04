# -*- coding:utf-8 -*-
# @author: alex  
# @time: 2019/1/3 9:35
import sys

from my_games.DoublePlayerGame import DoublePlayerGame
import json
from PyQt5.QtCore import *
from my_games.DoublePlayerGame import *
from PyQt5.QtMultimedia import QSound


class NetPlayerGame(DoublePlayerGame):
    def __init__(self, net_object, parent=None):
        super().__init__(parent=parent)
        self.net_object = net_object
        self.net_object.buildConnect()  # 建立网络连接
        self.net_object.msg_signal.connect(self.parseData)
        self.setWindowTitle("联机对战")
        # if net_object.nettype == 'client':
        #     self.local_color = "white"
        # elif net_object.nettype == "server":
        #     self.local_color = "black"
        self.color_flag = 'black'
        self.local_color = None
        self.st_over = True

        self.press = MyButton('source/催促按钮_hover.png',
                              'source/催促按钮_normal.png',
                              'source/催促按钮_press.png', parent=self)
        self.press.move(650, 500)
        self.press.clicked.connect(self.cuicu)

    def cuicu(self):

        QSound.play("source/cuicu.wav")
        msg = {}
        msg['msg_type'] = 'cuicu'
        self.net_object.send(json.dumps(msg))

    def goBack(self):
        self.backSignal.emit()
        self.close()
        self.net_object.socket.close()

    def goStart(self):
        msg = {}
        msg['msg_type'] = 'restart'
        self.net_object.send(json.dumps(msg))

    '''
    {
        "msg_type":"position",
        "x":"10",
        "y":"15",
        "color":"black"
    }
    
    '''

    def goGG(self):
        if self.st_over == True:
            QMessageBox.information(self, '五子棋-消息提示', '游戏未开始')
            return
        if self.local_color == 'black':
            print("黑棋认输，白棋胜")
            self.win_lbl = WinLabel(color='white', parent=self)
            self.win_lbl.move(100, 100)
            self.win_lbl.show()
            self.focus_Point.hide()
            self.st_over = True
        elif self.local_color == 'white':
            print("白棋认输 黑棋胜")
            self.win_lbl = WinLabel(color='black', parent=self)
            self.win_lbl.move(100, 100)
            self.win_lbl.show()
            self.focus_Point.hide()
            self.st_over = True

        msg = {}
        msg['msg_type'] = 'goGG'
        self.net_object.send(json.dumps(msg))

    def parseData(self, data):
        print('parseData' + data)
        try:
            msg = json.loads(data)
        except Exception as e:
            print(e)
            return
        print('msg:', msg)
        if msg['msg_type'] == "position":
            self.downChessman(QPoint(int(msg['x']), int(msg['y'])), msg['color'])
        elif msg['msg_type'] == "restart":
            result = QMessageBox.information(self, '五子棋-消息提示', '对方请求开始游戏', QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self.restartGame()
                self.local_color = 'white'
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'restart'
                msg['action_result'] = 'yes'
                self.net_object.send(json.dumps(msg))
            else:
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'restart'
                msg['action_result'] = 'no'
                self.net_object.send(json.dumps(msg))
        elif msg['msg_type'] == "response":
            if msg['action_type'] == "restart":
                if msg['action_result'] == 'yes':
                    self.restartGame()
                    self.local_color = 'black'
                else:
                    QMessageBox.information(None, '五子-消息提示', '对方拒绝开始游戏')
            elif msg['action_type'] == 'goUndo':
                if msg['action_result'] == 'yes':
                    self.goUndoGame()
                else:
                    QMessageBox.information((self, '五子棋-消息提示', '对方拒绝悔棋'))
        elif msg['msg_type'] == "goUndo":
            result = QMessageBox.information(self, '五子棋-消息提示', '对方请求悔棋', QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self.goUndoGame()
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'goUndo'
                msg['action_result'] = 'yes'
                self.net_object.send(json.dumps(msg))
        elif msg['msg_type'] == "goGG":
            self.win_lbl = WinLabel(color=self.local_color, parent=self)
            self.win_lbl.move(100, 100)
            self.win_lbl.show()
            self.st_over = True
            return
        elif msg['msg_type'] == 'cuicu':
            QSound.play('source/cuicu.wav')

    def goUndo(self):

        if self.st_over == True:
            QMessageBox.warning(self, '五子-消息棋提示', '游戏未开始，不能悔棋')
            return
        if self.local_color != self.color_flag:
            QMessageBox.warning(self, '五子-消息棋提示', '不是你的回合，不能悔棋')
            return
        msg = {}
        msg['msg_type'] = "goUndo"
        self.net_object.send(json.dumps(msg))

    def goUndoGame(self):
        try:
            if self.st_over != True:

                print('悔棋')
                m = self.history_chess.pop()
                m.close()
                n = self.history_chess.pop()
                n.close()
                self.focus_Point.hide()
                self.chess_map[m.map_point_x][m.map_point_y] = None
                self.chess_map[n.map_point_x][n.map_point_y] = None

                if self.color_flag == 'white':
                    self.player.pic = QPixmap('source/白手.png')
                else:
                    self.player.pic = QPixmap('source/黑手.png')
                self.player.setPixmap(self.player.pic)
                self.player.setFixedSize(self.player.pic.size())
                self.player.move(700, 580)
                self.player.show()
        except Exception as e:
            print(e)

    def restartGame(self):
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

    def downChessman(self, point, color):
        if self.color_flag == 'black':
            self.player.pic = QPixmap('source/白手.png')
        else:
            self.player.pic = QPixmap('source/黑手.png')
        self.player.setPixmap(self.player.pic)
        self.player.setFixedSize(self.player.pic.size())
        self.player.move(700, 580)
        self.player.show()

        chess_index = (point.y(), point.x())  # 棋子在棋盘中的下标
        pos = QPoint(50 + point.x() * 30, 50 + point.y() * 30)  # 棋子在棋盘中的坐标
        pos_x = pos.x()
        pos_y = pos.y()

        self.chessman = Chessman(color=color, parent=self)
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

        # if self.chessman.color == 'white':
        #     self.chessman.color = 'black'
        # else:
        #     self.chessman.color = 'white'

        self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y] = self.chessman
        # if self.chessman.color == 'black':
        #     self.player.pic = QPixmap('source/白手.png')
        # else:
        #     self.player.pic = QPixmap('source/黑手.png')
        #
        # self.player.setPixmap(self.player.pic)
        # self.player.setFixedSize(self.player.pic.size())
        # self.player.move(700, 580)
        # self.player.show()
        print(self.color_flag)
        # 历史记录
        self.history_chess.append(self.chessman)

        # 改变落子颜色
        if self.color_flag == 'white':
            self.color_flag = 'black'
        else:
            self.color_flag = 'white'
        # 判断输赢
        self.showWin()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        # if self.color_flag == 'black':
        #     self.player.pic = QPixmap('source/白手.png')
        # else:
        #     self.player.pic = QPixmap('source/黑手.png')
        if self.local_color is not self.color_flag:
            return
        # self.player.setPixmap(self.player.pic)
        # self.player.setFixedSize(self.player.pic.size())
        # self.player.move(700, 580)
        # self.player.show()

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
            elif self.color_flag == 'white':
                self.color_flag = 'black'
            return
        self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y] = self.chessman
        self.chessman.show()
        if self.color_flag == 'white':
            self.player.pic = QPixmap('source/白手.png')
        else:
            self.player.pic = QPixmap('source/黑手.png')
        self.player.setPixmap(self.player.pic)
        self.player.setFixedSize(self.player.pic.size())
        self.player.move(700, 580)
        self.player.show()

        print(self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y].color)

        # 显示标识
        self.focus_Point.move(pos_x, pos_y)
        self.focus_Point.show()
        self.focus_Point.raise_()

        self.history_chess.append(self.chessman)
        print(self.chessman.color)
        self.showWin()

        msg = {}
        msg["msg_type"] = "position"
        msg["y"] = self.chessman.map_point_x
        msg["x"] = self.chessman.map_point_y
        msg["color"] = self.chessman.color
        self.net_object.send(json.dumps(msg))

# if __name__ == '__main__':
# import cgitb
#
# cgitb.enable('text')
# q = QApplication(sys.argv)
# result = QMessageBox.information(None, '五子棋', '请开始游戏', QMessageBox.Cancel | QMessageBox.Close | QMessageBox.Ok)
# if result == QMessageBox.Ok:
#     print("我点击的是Ok")
# elif result == QMessageBox.Cancel:
#     print("我点击的是Cancel")
# elif result == QMessageBox.Close:
#     print("我点击的是Close")
#     sys.exit(q.exec_())
