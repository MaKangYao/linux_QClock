#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt, QTime, QPoint
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QPen

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()
        self.dragPos = QPoint()  # 用于记录拖动位置

    def initUI(self):
        # 设置窗口标志：无边框、置顶、工具窗口（不显示在任务栏）
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        # 透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(300, 120)  # 窗口大小

        # 时间标签
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 48, QFont.Bold))
        self.label.setStyleSheet("color: #00FFCC;")  # 青绿色，可自定

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # 每秒更新一次
        self.updateTime()       # 立即显示

    def updateTime(self):
        current = QTime.currentTime()
        time_text = current.toString("hh:mm:ss")
        # 如果想显示日期，取消下面两行的注释，并适当调高窗口高度
        # date_text = QDate.currentDate().toString("yyyy-MM-dd")
        # self.label.setText(f"{time_text}\n{date_text}")
        self.label.setText(time_text)

    def paintEvent(self, event):
        # 绘制半透明圆角背景
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 0, 0, 180)))  # 黑色半透明
        painter.setPen(QPen(QColor(255, 255, 255, 80))) # 弱边框
        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.drawRoundedRect(rect, 15, 15)
        super().paintEvent(event)

    # ---- 窗口拖动 ----
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)

    # ---- 右键菜单 ----
    def showContextMenu(self, pos):
        menu = QMenu()
        quit_action = menu.addAction("退出")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == quit_action:
            self.close()  # 触发 closeEvent

    # ---- 关键：关闭窗口时彻底退出程序 ----
    def closeEvent(self, event):
        QApplication.quit()  # 结束应用程序

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
