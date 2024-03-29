import time

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from . import const as c
from .multithread.worker import Worker
from .widgets.screenerTable import ScreenerTable
from .widgets.sliderWidget import SliderWidget
from .widgets.customheaders import CustomHeaders
from ...backend.adapters.base import BaseAdapter


class Screener(QWidget):
    """QWidget displaying contracts available for screening"""

    # TODO: Add a cached header file, and header customization.
    def __init__(self, adapter: BaseAdapter):
        super().__init__()
        self.adapter = adapter
        self.headers = c.DEFAULT_HEADERS
        self.buildMainStyle()

        # Building Children
        self.buildTools()

        self.buildTabWidget()
        self.styleWidget()

        # Pack Children
        self.mainLayout = QVBoxLayout(self)
        self.pack_main_layout()
        self.setLayout(self.mainLayout)

        self.threadpool = QThreadPool()

    def buildMainStyle(self):
        self.setWindowTitle("Bitget Screener")
        self.setGeometry(0, 0, 1280, 720)
        self.setStyleSheet("background-color:#2a2a2a;")

    def styleWidget(self):
        self.tabWidget.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        self.tabWidget.setStyleSheet(
            "QTabWidget::pane {border-bottom: 0px;}\
            QTabBar::tab {background-color:#2a2a2a;\
            color:#FFFFFF;border-radius:5px;padding:5px;}\
            QTabBar::tab::selected{background-color:#414141;}"
        )
        font = QFont("Bahnschrift", 18)
        self.tabWidget.setFont(font)
        self.tabWidget.tabBar().setFont(font)

    def buildTools(self):
        # Configure Container
        self.toolsWidget = QWidget(self)
        self.toolsWidget.setStyleSheet(
            "QWidget{ background-color:#2a2a2a; \
            color: white; border-radius:10px;}"
        )

        # Configure Tools (Buttons, Sliders, etc.)
        self.configButton = QPushButton(self.toolsWidget, text="Configure")
        self.configButton.setStyleSheet("background-color:#414141;padding:50px;")
        self.configButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.configButton.clicked.connect(self.buildHeaderConfig)
        self.headerSpacer = QSpacerItem(
            1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.autoRefWidget = SliderWidget(self)

        # Create Refresh Button
        self.refreshButton = QPushButton(self.toolsWidget, text="Refresh")
        self.refreshButton.setStyleSheet("background-color:#414141;padding:50px;")
        self.refreshButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.refreshButton.clicked.connect(self.refresh)

        # Pack config button, spacer, and refresh tools
        self.toolsLayout = QHBoxLayout()
        self.toolsLayout.addWidget(self.configButton)
        self.toolsLayout.addItem(self.headerSpacer)
        self.toolsLayout.addWidget(self.autoRefWidget)
        self.toolsLayout.addWidget(self.refreshButton)
        self.toolsWidget.setLayout(self.toolsLayout)

    def buildTabWidget(self):
        self.tabWidget = QTabWidget(self)
        self.perpUsdtTab = self.buildTab(c.TYPES[0], "USDT Margin Futures")
        self.perpUniTab = self.buildTab(c.TYPES[1], "Universal Margin Futures")

    def buildTab(self, types: str, title: str):
        tab = ScreenerTable(self.adapter, self.headers)
        tab.verticalHeader().setDefaultAlignment(Qt.AlignHCenter)
        tab.verticalHeader().setDefaultSectionSize(50)
        # TODO: Round out tab styling
        tab.setSelectionBehavior(QAbstractItemView.SelectRows)
        tab.setStyleSheet(
            "QTableView{background:#2a2a2a;color:#FFFFFF; \
            selection-background-color:#8080ff;} \
            QHeaderView::section{background:#2a2a2a;color:#FFFFFF; \
                                 padding:5px;border-style: none;} \
            QTableCornerButton::section{background: #2a2a2a;}"
        )
        tab.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        tab.getData()
        tab.setSortingEnabled(True)
        tab.horizontalHeader().setMinimumSectionSize(100)
        self.tabWidget.addTab(tab, title)
        return tab

    def beginRefreshTask(self):
        # Pass the function to execute
        if self.autoRefWidget.button.isChecked():
            worker = Worker(self.refreshTask)
            worker.signals.finished.connect(worker.stop)
            self.threadpool.start(worker)

    def refreshTask(self):
        while self.autoRefWidget.button.isChecked():
            self.refresh()
            time.sleep(self.autoRefWidget.slider.value() / 10)

    def refresh(self):
        self.tabWidget.currentWidget().getData()
        self.tabWidget.currentWidget().update()

    def pack_main_layout(self):
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.toolsWidget)
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.setStretch(0, 1)
        self.mainLayout.setStretch(1, 7)

    def buildHeaderConfig(self):
        headers_copy = self.headers.copy()
        self.headerGUI = CustomHeaders(headers_copy)
        self.headerGUI.applyButton.clicked.connect(self.applyHeaders)

    def applyHeaders(self):
        # Find the headers that were removed and added
        removed = {
            x: c.ALL_HEADERS[x]
            for x in set(self.headers) - set(self.headerGUI.usedHeaders)
        }
        added = {
            x: c.ALL_HEADERS[x]
            for x in set(self.headerGUI.usedHeaders) - set(self.headers)
        }

        # Remove and add the columns to the table
        for key, val in removed.items():
            for idx in range(self.tabWidget.count()):
                columnIndex = self.tabWidget.widget(idx).model._headers.index(val)
                self.tabWidget.widget(idx).model.removeColumn(columnIndex)
        for key, val in added.items():
            for idx in range(self.tabWidget.count()):
                self.tabWidget.widget(idx).model.insertColumn(val)

        self.headers = self.headerGUI.usedHeaders
        for idx in range(self.tabWidget.count()):
            self.tabWidget.widget(idx).headers = self.headerGUI.usedHeaders
            self.tabWidget.widget(idx).getData()
        self.refresh()
        self.headerGUI.close()
