
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QHeaderView,
                             QListWidget, QListWidgetItem, QPushButton,
                             QSizePolicy, QSpacerItem, QStyle, QTableWidget,
                             QTableWidgetItem, QTabWidget, QVBoxLayout,
                             QWidget)

from . import const as c
from . import utils


# Main Window
class Screener(QWidget):
    """QWidget displaying contracts available for screening"""

    def __init__(self, mAPI):
        super().__init__()
        self.mAPI = mAPI

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

    def buildHeaderWindow(self):

        self.headerWin.setStyleSheet("QWidget{background-color:#282828; color: white;}")

        self.configButton.setSizePolicy(self.minPolicy)
        self.autoRefresh.setSizePolicy(self.minPolicy)
        self.refreshButton.setSizePolicy(self.minPolicy)
        self.refreshButton.clicked.connect(self.refreshMainWindow)

        self.headerWinLayout.addWidget(self.configButton)
        self.headerWinLayout.addItem(self.headerSpacer)
        self.headerWinLayout.addWidget(self.autoRefresh)
        self.headerWinLayout.addWidget(self.refreshButton)
        self.headerWin.setLayout(self.headerWinLayout)

    def buildMainWindow(self):

        self.perpUsdtTab = QTableWidget()
        self.tableStyleSheet(self.perpUsdtTab)
        self.buildTab(c.TYPES[0],self.perpUsdtTab)
        self.tabWidget.addTab(self.perpUsdtTab,"USDT Margin Futures")

        self.perpUniTab = QTableWidget()
        self.tableStyleSheet(self.perpUniTab)
        self.buildTab(c.TYPES[1],self.perpUniTab)
        self.tabWidget.addTab(self.perpUniTab,"Universal Margin Futures")

    #TODO: Make refresh function more robust
    def refreshMainWindow(self):
        data1 = self.getTableData(c.TYPES[0])
        data2 = self.getTableData(c.TYPES[1])
        self.packTableData(data1,self.perpUsdtTab)
        self.packTableData(data2,self.perpUniTab)

    def buildTab(self, types, tab):
        data = self.getTableData(types)
        tab.setColumnCount(len(self.headers))
        tab.setHorizontalHeaderLabels(self.headers.values())
        tab.setRowCount(len(data))
        self.packTableData(data, tab)

    def tableStyleSheet(self,table):
        table.setAlternatingRowColors(True)
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

    def getTableData(self, types):
        # Get list of contract dictionaries, union respective dictionaries
        contracts = utils.getAllInfo(self.mAPI,types)
        contractsFinal = []
        for contract in contracts:
            tempContract = []
            for key, val in contract.items():
                if key in self.headers: # may need to change to self.headers.keys(), linter change
                    tempContract.append((key, val))
            contractsFinal.append(tempContract)
        return contractsFinal

    def packTableData(self, contracts, widget):
        for index1 in range(0, len(contracts)):
            keys = list(self.headers.keys())
            for index2 in range(0, len(keys)):
                # Attempt to pack each value matching self.header keys into the table
                try:
                    newItem = QTableWidgetItem()
                    # Split symbol from type (e.g. BTCUSDT_UMCBL -> BTCUSDT)
                    if contracts[index1][index2][0] == "symbol":
                        newItem.setData(QtCore.Qt.DisplayRole, contracts[index1][index2][1].split("_")[0])
                    else:
                        newItem.setData(QtCore.Qt.DisplayRole, contracts[index1][index2][1])
                    widget.setItem(index1, index2, newItem)
                # If corresponding value does not exist for key, pack N/A.
                except IndexError:
                    widget.setItem(index1, index2, QTableWidgetItem("N/A"))