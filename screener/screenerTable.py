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
    def __init__(self, mAPI, headers=c.DEFAULT_HEADERS, types=c.TYPES[0]):
        super().__init__()
        self.mAPI = mAPI
        self.headers = headers
        self.types = types

        self.font = QFont("Bahnschrift", 12)
        self.setFont(self.font)
        self.horizontalHeader().setFont(self.font)
        self.verticalHeader().setFont(self.font)
        self.setStyleSheet(
            "QTableView QTableCornerButton::section { background: #121212; }"
        )
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.buildStyle()

        self.model = ScreenerModel(self.headers)
        self.setModel(self.model)
        self.setShowGrid(False)
        self.threadPool = QThreadPool()

    def buildStyle(self):
        # Horizontal Headers
        self.horizontalHeader().setFrameShape(QFrame.NoFrame)
        self.horizontalHeader().setStyleSheet(
            "::section{background-color:#3D3D3D; color: white;}"
        )
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Vertical Headers
        self.verticalHeader().setFrameShape(QFrame.NoFrame)
        self.verticalHeader().setStyleSheet(
            "::section{background-color:#3D3D3D; color: white;}"
        )

        # Styling
        self.setStyleSheet(
            "QWidget{\
                background-color:#282828; color: white; \
                alternate-background-color:#3D3D3D;}\
             QTableWidget QTableCornerButton::section {\
                background-color: #3D3D3D; }"
        )

    def getData(self):
        # --Subscribe to Channels--
        # -Get all tickers from REST API-
        tickers = self.mAPI.tickers(self.types)["data"]
        
        # Iterate through returned tickers, push to data model.
        for ticker in tickers:
            ticker["symbol"] = ticker["symbol"].split("_")[0]
            ticker = list(ticker.values())
            # Convert all numeric values to floats.
            # If contract is not currently listed, some elements 
            # will register as None, and will be changed to zero
            ticker[1:] = [float(x) if x is not None else 0 for x in ticker[1:]]
            ticker.pop(6)
            self.model.addData(ticker)
        
