import json
import sys
from turtle import Screen


from bitget.ws.bitget_ws_client import SubscribeReq
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QHeaderView,
                             QListWidget, QListWidgetItem, QPushButton,
                             QSizePolicy, QSpacerItem, QStyle, QTableView,
                             QTableWidgetItem, QTabWidget, QVBoxLayout,
                             QWidget)

from screener import const as c
from screener.screenerModel import ScreenerModel
from screener import utils as u


class ScreenerTable(QTableView):
    def __init__(self, mAPI, wsClient, headers=c.DEFAULT_HEADERS, types=c.TYPES[0]):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 720
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color:#121212;")
        self.showGrid()
        self.client = wsClient
        self.mAPI = mAPI
        self.headers = headers
        self.types = types
        self.contracts = {}

        # table.setAlternatingRowColors(True)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Plain)

        # Horizontal Headers
        self.horizontalHeader().setFrameShape(QtWidgets.QFrame.NoFrame)
        self.horizontalHeader().setStyleSheet(
            "::section{background-color:#3D3D3D; color: white;}")
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Vertical Headers
        self.verticalHeader().setFrameShape(QtWidgets.QFrame.NoFrame)
        self.verticalHeader().setStyleSheet(
            "::section{background-color:#3D3D3D; color: white;}")

        self.setStyleSheet(
            "QWidget{background-color:#282828; color: white; alternate-background-color:#3D3D3D;}"
            + "QTableWidget QTableCornerButton::section { background-color: #3D3D3D; }"
        )

        self.subscribeAllTickers()
        self.model = ScreenerModel(self.contracts, self.headers)

        self.setModel(self.model)
        self.setSortingEnabled(True)

    def subscribeAllTickers(self):
        # --Subscribe to Channels--
        # -Get all symbols from REST API-
        symbols = u.getAllSymbols(self.mAPI, self.types)
        channels = [SubscribeReq("mc", "ticker", x) for x in symbols]
        self.client.subscribe(channels, self.handleTicker)

    def updateTable(self):
        self.update()
    
    def handle(self, message):
        pass

    def handleTicker(self, message):  # TODO: Make tab selection more robust
        message = json.loads(message)["data"]
        message = list(message[0].values())
        self.model.addData(message)
