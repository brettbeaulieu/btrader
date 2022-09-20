import json

from bitget.ws.bitget_ws_client import SubscribeReq
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QHeaderView, QTableView
from .multithread.worker import Worker
from screener import const as c
from screener import utils as u
from screener.screenerModel import ScreenerModel


class ScreenerTable(QTableView):
    def __init__(self, mAPI, wsClient, headers=c.DEFAULT_HEADERS, types=c.TYPES[0]):
        super().__init__()
        self.mAPI = mAPI
        self.wsClient = wsClient
        self.headers = headers
        self.types = types

        self.font = QFont("Bahnschrift", 12)
        self.setFont(self.font)
        self.horizontalHeader().setFont(self.font)
        self.verticalHeader().setFont(self.font)
        self.setStyleSheet(
            "QTableView QTableCornerButton::section { background: #121212; }")
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setAlternatingRowColors(True)
        self.buildStyle()

        self.model = ScreenerModel(self.headers, self.wsClient)
        self.setModel(self.model)
        self.setShowGrid(False)
        self.threadPool = QThreadPool()

    def buildStyle(self):
        # Horizontal Headers
        self.horizontalHeader().setFrameShape(QFrame.NoFrame)
        self.horizontalHeader().setStyleSheet(
            "::section{background-color:#3D3D3D; color: white;}")
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Vertical Headers
        self.verticalHeader().setFrameShape(QFrame.NoFrame)
        self.verticalHeader().setStyleSheet(
            "::section{background-color:#3D3D3D; color: white;}")

        # Styling
        self.setStyleSheet(
            "QWidget{\
                background-color:#282828; color: white; \
                alternate-background-color:#3D3D3D;}\
             QTableWidget QTableCornerButton::section {\
                background-color: #3D3D3D; }" )

    def subscribeAllTickers(self):
        # --Subscribe to Channels--
        # -Get all symbols from REST API-
        symbols = u.getAllSymbols(self.mAPI, self.types)
        channels = [SubscribeReq("mc", "ticker", x) for x in symbols]
        self.wsClient.subscribe(channels, self.pushData)


    def pushData(self, message):
        message = list(json.loads(message)["data"][0].values())
        message.pop(8)
        message[1:] = [float(x) for x in message[1:]]
        self.model.addData(message)
