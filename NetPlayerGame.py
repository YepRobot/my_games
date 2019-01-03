# -*- coding:utf-8 -*-
# @author: alex  
# @time: 2019/1/3 9:35
from my_games.DoublePlayerGame import DoublePlayerGame
import json
from PyQt5.QtCore import *
from my_games.DoublePlayerGame import *


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

    '''
    {
        "msg_type":"position",
        "x":"10",
        "y":"15",
        "color":"black"
    }
    
    '''

    def parseData(self, data):
        print('parseData' + data)
        msg = json.loads(data)
        print('msg:', msg)
        if msg['msg_type'] == "position":
            self.downChessman(QPoint(int(msg['x']), int(msg['y'])), msg['color'])

    def downChessman(self, point, color):

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

        if self.chessman.color == 0:
            self.chessman.color = 'black'
        else:
            self.chessman.color = 'white'

        self.chess_map[self.chessman.map_point_x][self.chessman.map_point_y] = self.chessman

        # 历史记录
        self.history_chess.append(self.chessman)

        # 改变落子颜色
        if self.color_flag == 0:
            self.color_flag = 1
        else:
            self.color_flag = 0
        # 判断输赢
