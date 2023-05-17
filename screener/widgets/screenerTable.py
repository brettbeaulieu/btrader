from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QHeaderView, QTableView

from .. import const as c
from ..widgets.screenerModel import ScreenerModel

"""_summary_
    ScreenerTable is a QTableView implementation that displays the results of API ticker
    requests.
"""


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

        self.model = ScreenerModel(list(self.headers.values()))
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
             QTableWidget::QTableCornerButton::section {\
                color: #3D3D3D; }"
        )

    def getData(self):
        # --Subscribe to Channels--
        # -Get all tickers from REST API-
        tickers = self.mAPI.tickers(self.types)["data"]
        # Iterate through returned tickers, push to data model.
        for ticker in tickers:
            # Filter out unwanted data, as defined by headers.
            filteredTicker = []
            for key in self.headers.keys():
                filteredTicker.append(ticker[key])
            # Convert all numeric values to floats.
            # If contract is not currently listed, some elements
            # will register as None, and will be changed to zero
            filteredTicker[1:] = [
                float(x) if x is not None else 0 for x in filteredTicker[1:]
            ]
            self.model.addData(filteredTicker)
