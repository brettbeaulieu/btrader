import time
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThreadPool, QTimer
from PyQt5.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .const import DEFAULT_HEADERS, TYPES
from .multithread.worker import Worker
from .screenerTable import ScreenerTable


class Screener(QWidget):
    """QWidget displaying contracts available for screening"""

    def __init__(self, mAPI, client):
        super().__init__()
        self.mAPI = mAPI
        self.client = client
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 720
        self.setWindowTitle("Bitget Screener")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color:#121212;")

        # TODO: Add a cached header file, and customization.
        self.headers = DEFAULT_HEADERS

        # Build Tools Container
        self.buildToolsUi()

        self.screenerWidget = QTabWidget(self)
        self.buildTabWidget()
        self.screenerWidget.setStyleSheet("QTabWidget::pane {border-bottom: 0px;}\
                                           QTabBar::tab {background-color:#2a2a2a;\
                                           color:#FFFFFF;}")
        
        self.font = QFont("Bahnschrift", 12)
        self.screenerWidget.setFont(self.font)
        self.screenerWidget.tabBar().setFont(self.font)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.toolsWidget)
        self.mainLayout.addWidget(self.screenerWidget)
        self.mainLayout.setStretch(0, 1)
        self.mainLayout.setStretch(1, 7)
        self.setLayout(self.mainLayout)
        self.threadpool = QThreadPool()

    def buildToolsUi(self):

        # Configure Container
        self.toolsWidget = QWidget(self)
        self.toolsWidget.setStyleSheet(
            "QWidget{ background-color:#2a2a2a; \
            color: white; border-radius:10px;}"
        )

        # Configure Tools (Buttons/Interactives)
        self.configButton = QPushButton(self.toolsWidget, text="Configure")
        self.configButton.setStyleSheet("background-color:#414141;padding:50px;")
        self.configButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.headerSpacer = QSpacerItem(
            1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        self.autoRefreshButton = QCheckBox(self.toolsWidget, text="Auto-Refresh")
        self.autoRefreshButton.stateChanged.connect(self.beginRefreshTask)
        self.refreshButton = QPushButton(self.toolsWidget, text="Refresh")
        self.refreshButton.setStyleSheet("background-color:#414141;padding:50px;")
        self.refreshButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.refreshButton.clicked.connect(self.refresh)

        # Pack container
        self.toolsLayout = QHBoxLayout()
        self.toolsLayout.addWidget(self.configButton)
        self.toolsLayout.addItem(self.headerSpacer)
        self.toolsLayout.addWidget(self.autoRefreshButton)
        self.toolsLayout.addWidget(self.refreshButton)
        self.toolsWidget.setLayout(self.toolsLayout)

    def buildTabWidget(self):
        self.screenerWidget.setStyleSheet(
            "::tab{background-color:#2a2a2a;\
            color: white;}"
        )
        self.perpUsdtTab = self.buildTab(TYPES[0], "USDT Margin Futures")
        self.perpUniTab = self.buildTab(TYPES[1], "Universal Margin Futures")

    def buildTab(self, types: str, title: str):
        tab = ScreenerTable(self.mAPI, self.client, self.headers, types)
        # TODO: Round out tab styling
        tab.setStyleSheet( "QTableView{alternate-background-color:#242424; background: #2a2a2a; color: #FFFFFF;}\
                            QTableView QTableCornerButton::section { background: #2a2a2a; alternate-background-color:#a0a0a0; }")
        tab.subscribeAllTickers()
        tab.setSortingEnabled(True)
        self.screenerWidget.addTab(tab, title)
        return tab

    def beginRefreshTask(self):
        # Pass the function to execute
        if self.autoRefreshButton.isChecked():
            worker = Worker(self.refreshTask)
            worker.signals.finished.connect(lambda: print("Done!"))
            self.threadpool.start(worker)

    def refreshTask(self):
        while self.autoRefreshButton.isChecked():
            time.sleep(1)
            self.refresh()

    def refresh(self):
        self.perpUsdtTab.update()
        self.perpUniTab.update()
