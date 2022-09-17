import json
import sys
from turtle import Screen

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QHeaderView,
                             QListWidget, QListWidgetItem, QPushButton,
                             QSizePolicy, QSpacerItem, QStyle, QTableView,
                             QTableWidgetItem, QTabWidget, QVBoxLayout,
                             QWidget)

from bitget.consts import CONTRACT_WS_URL
from bitget.mix.market_api import MarketApi
from bitget.ws.bitget_ws_client import BitgetWsClient, SubscribeReq
from screener import const as c
from screener.utils import *
from screener.screenerTable import ScreenerTable

class Screener(QWidget):
    def __init__(self, api_key, secret_key, passphrase, mAPI):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 720
        self.setWindowTitle("Bitget Screener")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color:#121212;")

        self.client = BitgetWsClient(CONTRACT_WS_URL, need_login=True)\
        .api_key(api_key) \
        .api_secret_key(secret_key) \
        .passphrase(passphrase) \
        .error_listener(self.handle) \
        .build()
        self.mAPI = mAPI
        #self.mAPI = MarketApi(api_key, secret_key, passphrase)
        self.contracts = {}
        
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
        # End build header window

        # Start build main window
        self.tabWidget = QTabWidget()
        self.tabWidget.setStyleSheet("::tab{background-color:#282828; color: white;}")
        self.buildMainWindow()
        # End build main window
        # Start assemble layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.headerWin)
        self.layout.addWidget(self.tabWidget)
        self.setLayout(self.layout)
        # End assemble layout
        self.show()
        

    def subscribeAllTickers(self):
        #--Subscribe to Channels--
        # -Get all symbols from REST API-
        symbols = getAllSymbols(self.mAPI,c.TYPES[0])
        channels = [SubscribeReq("mc", "ticker", x) for x in symbols]
        self.client.subscribe(channels,self.handleTicker)

    def buildHeaderWindow(self):

        self.headerWin.setStyleSheet("QWidget{background-color:#282828; color: white;}")

        self.configButton.setSizePolicy(self.minPolicy)
        self.autoRefresh.setSizePolicy(self.minPolicy)
        self.refreshButton.setSizePolicy(self.minPolicy)
        self.refreshButton.clicked.connect(self.updateTable)
        self.headerWinLayout.addWidget(self.configButton)
        self.headerWinLayout.addItem(self.headerSpacer)
        self.headerWinLayout.addWidget(self.autoRefresh)
        self.headerWinLayout.addWidget(self.refreshButton)
        self.headerWin.setLayout(self.headerWinLayout)

    def buildMainWindow(self):

        self.subscribeAllTickers()
        self.perpUsdtTab = self.buildTable(self.contracts)
        self.tabWidget.addTab(self.perpUsdtTab,"USDT Margin Futures")
        self.perpUniTab = self.buildTable(self.contracts)
        self.tabWidget.addTab(self.perpUniTab,"Universal Margin Futures")
    
    def buildTable(self, data, types=0): #TODO: Decide on implementation of passing types to tables
        table = QTableView() # TODO: Transition to QTableView
        model = ScreenerTable(data)
        table.setModel(model)
        self.tableStyleSheet(table)
        return table
    
    def tableStyleSheet(self,table):
        #table.setAlternatingRowColors(True)
        table.setFrameShape(QtWidgets.QFrame.NoFrame)
        table.setFrameShadow(QtWidgets.QFrame.Plain)

        # Horizontal Headers
        table.horizontalHeader().setFrameShape(QtWidgets.QFrame.NoFrame)
        table.horizontalHeader().setStyleSheet("::section{background-color:#3D3D3D; color: white;}")
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Vertical Headers
        table.verticalHeader().setFrameShape(QtWidgets.QFrame.NoFrame)
        table.verticalHeader().setStyleSheet("::section{background-color:#3D3D3D; color: white;}")

        table.setStyleSheet(
            "QWidget{background-color:#282828; color: white; alternate-background-color:#3D3D3D;}"
            + "QTableWidget QTableCornerButton::section { background-color: #3D3D3D; }"
        )
        table.setSortingEnabled(True)

    def updateTable(self):
        self.perpUsdtTab.update()

    def handle(self, message):
        pass

    def handleTicker(self, message): #TODO: Make tab selection more robust
        message = json.loads(message)["data"]
        message = list(message[0].values())
        self.perpUsdtTab.model().addData(message)

