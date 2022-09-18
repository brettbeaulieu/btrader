import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, QThread, QTimer, QThreadPool, QRunnable
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QHeaderView, QListWidget,
                             QListWidgetItem, QPushButton, QSizePolicy,
                             QSpacerItem, QStyle, QTableWidget,
                             QTableWidgetItem, QTabWidget, QVBoxLayout,
                             QWidget)

from . import const as c
from . import utils
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
        self.setStyleSheet("background-color:#121212;")

        # TODO: Add a cached header file, and customization.
        self.headers = c.DEFAULT_HEADERS

        # Start build header window
        self.headerWin = QWidget()

        self.minPolicy = QSizePolicy()
        self.minPolicy.setHorizontalPolicy(QSizePolicy.Minimum)
        self.minPolicy.setVerticalPolicy(QSizePolicy.Minimum)

        self.configButton = QPushButton(self.headerWin,text="Configure")
        self.headerSpacer = QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.autoRefresh = QCheckBox(self.headerWin,text="Auto-Refresh")
        self.refreshButton = QPushButton(self.headerWin,text="Refresh")
        self.headerWinLayout = QHBoxLayout()

        self.buildHeaderWindow()

        self.tabWidget = QTabWidget()
        self.tabWidget.setStyleSheet("::tab{background-color:#282828; color: white;}")
        self.buildMainWindow()

        # Start assemble layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.headerWin)
        self.layout.addWidget(self.tabWidget)
        self.setLayout(self.layout)
        
        self.threadpool = QThreadPool()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.refreshMainWindow)



    def buildHeaderWindow(self):

        self.headerWin.setStyleSheet("QWidget{background-color:#282828; color: white;}")

        self.configButton.setSizePolicy(self.minPolicy)
        self.autoRefresh.setSizePolicy(self.minPolicy)
        self.autoRefresh.stateChanged.connect(self.toggleAutoRefresh)
        self.refreshButton.setSizePolicy(self.minPolicy)
        self.refreshButton.clicked.connect(self.refreshMainWindow)

        self.headerWinLayout.addWidget(self.configButton)
        self.headerWinLayout.addItem(self.headerSpacer)
        self.headerWinLayout.addWidget(self.autoRefresh)
        self.headerWinLayout.addWidget(self.refreshButton)
        self.headerWin.setLayout(self.headerWinLayout)

    def buildMainWindow(self):

        self.perpUsdtTab = ScreenerTable(self.mAPI, self.client, self.headers, c.TYPES[0])
        self.tabWidget.addTab(self.perpUsdtTab,"USDT Margin Futures")

        self.perpUniTab = ScreenerTable(self.mAPI, self.client, self.headers, c.TYPES[1])

        self.tabWidget.addTab(self.perpUniTab,"Universal Margin Futures")

    def toggleAutoRefresh(self):
        if self.configButton.isChecked():
            self.timer.start()
        else:
            self.timer.stop()
        

    def refreshMainWindow(self):
        self.perpUsdtTab.updateTable()
        self.perpUniTab.updateTable()
