import time
import traceback
import sys
from PyQt5.QtCore import QRunnable, QThreadPool, QTimer, pyqtSignal
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QPushButton, QSizePolicy,
                             QSpacerItem, QTabWidget, QVBoxLayout, QWidget)
from . import const as c
from .screenerTable import ScreenerTable

# Main Window
class Screener(QWidget):
    """QWidget displaying contracts available for screening"""

    def __init__(self, mAPI, client):
        super().__init__()
        self.mAPI = mAPI
        self.client = client

        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 720
        
        self.setWindowTitle("Bitget Screener")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color:#282828;")

        # TODO: Add a cached header file, and customization.
        self.headers = c.DEFAULT_HEADERS

        # Start build header window
        self.headerWin = QWidget(self)

        self.minPolicy = QSizePolicy()
        self.minPolicy.setHorizontalPolicy(QSizePolicy.Minimum)
        self.minPolicy.setVerticalPolicy(QSizePolicy.Minimum)

        self.configButton = QPushButton(self.headerWin, text="Configure")
        self.headerSpacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.autoRefreshButton = QCheckBox(self.headerWin, text="Auto-Refresh")
        self.refreshButton = QPushButton(self.headerWin, text="Refresh")
        self.headerWinLayout = QHBoxLayout()

        self.tabWidget = QTabWidget()
        self.buildTabWidget()
        self.buildHeaderWindow()
        # Start assemble layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.headerWin)
        self.layout.addWidget(self.tabWidget)
        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.threadedRefresh)
        self.threadpool = QThreadPool()


    

    def buildTabWidget(self):
        self.tabWidget.setStyleSheet("::tab{background-color:#282828; color: white;}")
        self.perpUsdtTab = self.buildTab(c.TYPES[0], "USDT Margin Futures")
        self.perpUniTab = self.buildTab(c.TYPES[1], "Universal Margin Futures")
        
    def buildTab(self, types:str, title:str):
        tab = ScreenerTable(self.mAPI,self.client, self.headers, types)
        while True:
            if len(tab.contracts) > 0:
                self.tabWidget.addTab(tab,title)
                break
        return tab
                

    def toggleAutoRefresh(self):
        if self.autoRefreshButton.isChecked():
            self.timer.start(100)
        else:
            self.timer.stop()
        
    def threadedRefresh(self):
        x = Worker(self.refresh)
        self.threadpool.start(x)
        
    def refresh(self):
        self.perpUsdtTab.updateTable()
        self.perpUniTab.updateTable()

    def manualRefresh(self):
        self.refresh()
        print("Refreshed.")

