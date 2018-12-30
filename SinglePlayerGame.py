# -*- coding:utf-8 -*-
# @author: alex
# @time: 2018/12/30 8:40

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from my_games.MyButton import MyButton
import sys


class SinglePlayerGame(QWidget):

    # 信号量
    backSignal = pyqtSignal()  # 返回按钮
    startSignal = pyqtSignal()  # 开始按钮
    undoSignal = pyqtSignal()  # 悔棋按钮
    ggSignal = pyqtSignal()  # 认输按钮




