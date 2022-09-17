from collections import OrderedDict
from PyQt5 import QtWidgets
from . import const as c
from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStyle,
)
import PyQt5.QtCore as QtCore

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
        self.types = c.TYPES[0]

        self.lSelect = ""
        self.rSelect = ""

        self.headers = OrderedDict(c.DEFAULT_HEADERS)
        self.allHeaders = OrderedDict(c.CONTRACT_HEADERS | c.TICKER_HEADERS)
        self.unusedHeaders = OrderedDict({
            x: self.allHeaders[x] for x in set(self.allHeaders) - set(self.headers)
        })

        # Header Customization UI Elements
        self.headerWin = QWidget()
        self.headerWinLayout = QVBoxLayout()
        self.topHeaderWin = QWidget()
        self.topHeaderLayout = QHBoxLayout()
        self.usedList = QListWidget()
        self.unusedList = QListWidget()
        self.tempUsedHeaders = None
        self.tempUnusedHeaders = None

        # Create tool button widgets
        self.toolbarWidget = QWidget()
        self.toolsWin = QWidget()
        self.toolsLayout = QHBoxLayout(self.toolsWin)
        self.buttonLayout = QHBoxLayout(self.toolbarWidget)
        self.customize_button = QPushButton("Edit Headers")
        self.refresh_button = QPushButton("Refresh")

        # Build Table + Toolbar
        self.tableWidget = QTableWidget()
        self.table = self.buildTable()
        self.toolbar = self.buildToolbar()

        # Pack Table + Toolbar
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        # Show window
        self.show()

    # Create table of 'self.types' type contracts based on headers specified in field 'self.headers'
    def buildTable(self):

        # Table Stylesheet Customization
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Plain)

        self.tableWidget.horizontalHeader().setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.horizontalHeader().setStyleSheet(
            "::section{background-color:#3D3D3D; color: white;}"
        )
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableWidget.verticalHeader().setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.verticalHeader().setStyleSheet(
            "::section{background-color:#3D3D3D; color: white;}"
        )

        self.tableWidget.setStyleSheet(
            "QWidget{background-color:#282828; color: white; alternate-background-color:#3D3D3D;}"
            + "QTableWidget QTableCornerButton::section { background-color: #3D3D3D; }"
        )

        # update contracts list 
        self.getTableData()

        # Table Sorting
        self.tableWidget.setSortingEnabled(True)

        return self.tableWidget

    def getTableData(self):

        # Get list of contract dictionaries, union respective dictionaries
        contractsInfo = self.mAPI.contracts(self.types)["data"]
        tickersInfo = self.mAPI.tickers(self.types)["data"]
        for x in range(0, len(contractsInfo)):
            tickersInfo[x] = contractsInfo[x] | tickersInfo[x]

        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(self.headers.values())
        self.tableWidget.setRowCount(len(contractsInfo))

        # Filter out non-header items from combined tickersInfo
        # Append all header items to a respective tuple within the contracts list.
        contracts = []
        for contract in tickersInfo:
            tempContract = []
            for key, val in contract.items():
                if key in self.headers.keys():
                    tempContract.append( (key, val) )
            contracts.append(tempContract)

        # Pack all contracts into table
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
                    self.tableWidget.setItem(index1, index2, newItem)
                # If corresponding value does not exist for key, pack N/A.
                except IndexError:
                    self.tableWidget.setItem(index1, index2, QTableWidgetItem("N/A"))

    def buildToolbar(self):

        self.customize_button.clicked.connect(self.buildHeaderUI)
        self.refresh_button.clicked.connect(self.getTableData)

        self.buttonLayout.addWidget(self.customize_button)
        self.buttonLayout.addWidget(self.refresh_button)

        self.toolbarWidget.setLayout(self.buttonLayout)
        self.toolbarWidget.setStyleSheet("QWidget{background-color:#282828; color: white;}")
        self.toolbarWidget.setFixedHeight(50)

        return self.toolbarWidget

    def applyHeaderChanges(self):
        self.headers = self.tempUsedHeaders
        self.unusedHeaders = self.tempUnusedHeaders
        self.headerWin.close()
        self.getTableData()

    def getHeaderFromVal(self, headerVal):
        for x in self.allHeaders.keys():
            if headerVal == self.allHeaders.get(x):
                return {x: headerVal}

    def getKeyFromPair(self, dictPair):
        for x in dictPair.keys():
            return x

    # Header Helpers
    def makeUnused(self):
        row = self.usedList.currentRow()
        if isinstance(row, int):
            item = self.usedList.takeItem(row)
            headerVal = item.text()

            dictPair = self.getHeaderFromVal(headerVal)
            if dictPair not in self.tempUnusedHeaders.items():
                self.tempUnusedHeaders = self.tempUnusedHeaders | dictPair
                self.unusedList.addItem(item)
                del self.tempUsedHeaders[self.getKeyFromPair(dictPair)]
                self.tempUnusedHeaders = {
                    x: self.allHeaders[x]
                    for x in set(self.allHeaders) - set(self.tempUsedHeaders)
                }

    def makeUsed(self):
        row = self.unusedList.currentRow()
        if row > -1:
            item = self.unusedList.takeItem(row)
            headerVal = item.text()

            dictPair = self.getHeaderFromVal(headerVal)
            if dictPair not in self.headers.items():
                self.tempUsedHeaders = self.tempUsedHeaders | dictPair
                self.usedList.addItem(item)
                self.tempUnusedHeaders = {
                    x: self.allHeaders[x]
                    for x in set(self.allHeaders) - set(self.tempUsedHeaders)
                }
    # Headers
    def buildHeaderUI(self): 
        # Customize Header Window Stylesheet
        self.headerWin.setStyleSheet(
            "QWidget{background-color:#282828; color: white; alternate-background-color:#3D3D3D;}"
            + "QTableWidget QTableCornerButton::section { background-color: #3D3D3D; }"
        )

        # populate used headers list
        self.tempUsedHeaders = self.headers
        for x in self.tempUsedHeaders.values():
            tempItem = QListWidgetItem(x)
            self.usedList.addItem(tempItem)

        # populate unused headers list
        self.tempUnusedHeaders = self.unusedHeaders
        for x in self.tempUnusedHeaders.values():
            tempItem = QListWidgetItem(x)
            self.unusedList.addItem(tempItem)
        self.topHeaderLayout.addWidget(self.usedList)
        self.topHeaderLayout.addWidget(self.unusedList)
        self.topHeaderWin.setLayout(self.topHeaderLayout)

        # create tool buttons
        arrowRight = self.style().standardIcon(QStyle.SP_ArrowRight)
        self.makeUnusedButton = QPushButton(arrowRight, "Make Unused")
        self.makeUnusedButton.clicked.connect(self.makeUnused)
        self.toolsLayout.addWidget(self.makeUnusedButton)

        arrowLeft = self.style().standardIcon(QStyle.SP_ArrowLeft)
        self.makeUsedButton = QPushButton(arrowLeft, "Make Used")
        self.makeUsedButton.clicked.connect(self.makeUsed)
        self.toolsLayout.addWidget(self.makeUsedButton)

        confirm = self.style().standardIcon(QStyle.SP_DialogApplyButton)
        self.applyButton = QPushButton(confirm, "Apply Changes")
        self.applyButton.clicked.connect(self.applyHeaderChanges)
        self.toolsLayout.addWidget(self.applyButton)

        cancel = self.style().standardIcon(QStyle.SP_DialogCancelButton)
        self.discardButton = QPushButton(cancel, "Discard Changes")
        self.discardButton.clicked.connect(self.headerWin.close)
        self.toolsLayout.addWidget(self.discardButton)

        self.toolsWin.setLayout(self.toolsLayout)

        self.headerWinLayout.addWidget(self.topHeaderWin)
        self.headerWinLayout.addWidget(self.toolsWin)
        self.headerWin.setLayout(self.headerWinLayout)
        self.headerWin.show()
