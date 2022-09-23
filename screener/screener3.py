import time

from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QAbstractItemView, QCheckBox, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QSpacerItem,
                             QTabWidget, QVBoxLayout, QWidget)

from .const import DEFAULT_HEADERS, TYPES
from .multithread.worker import Worker
from .screenerTable import ScreenerTable


class Screener(QWidget):
    """QWidget displaying contracts available for screening"""

    def __init__(self, mAPI):
        super().__init__()
        self.mAPI = mAPI
        self.headers = DEFAULT_HEADERS
        # TODO: Add a cached header file, and customization.

        # Building Children
        self.buildMainStyle()
        self.buildToolsUi()
        self.buildTabWidget()
        self.buildTabWidgetStyle()

        # Pack Children
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.toolsWidget)
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.setStretch(0, 1)
        self.mainLayout.setStretch(1, 7)
        self.setLayout(self.mainLayout)

        self.threadpool = QThreadPool()

    def buildMainStyle(self):
        self.setWindowTitle("Bitget Screener")
        self.setGeometry(0, 0, 1280, 720)
        self.setStyleSheet("background-color:#121212;")

    def buildTabWidgetStyle(self):
        self.tabWidget.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        self.tabWidget.setStyleSheet(
            "QTabWidget::pane {border-bottom: 0px;}\
            QTabBar::tab {background-color:#2a2a2a;\
            color:#FFFFFF;}"
        )
        font = QFont("Bahnschrift", 12)
        self.tabWidget.setFont(font)
        self.tabWidget.tabBar().setFont(font)

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
        self.autoRefreshWidget = QWidget(self.toolsWidget)

        # Slider Stuff
        self.sliderWidget = QWidget(self.autoRefreshWidget)
        self.autoRefreshSlider = QSlider(Qt.Vertical, self.sliderWidget)
        self.autoRefreshSlider.setTickPosition(QSlider.TicksBelow)
        self.autoRefreshSlider.setTickInterval(1)
        self.autoRefreshSlider.setRange(1,10)
        self.autoRefreshSlider.valueChanged.connect(
            lambda: self.autoRefreshSlider.setToolTip(str(self.autoRefreshSlider.value()/10)+" secs")
            )
        # Slider Labels
        self.sliderLabels = QWidget(self.sliderWidget)
        self.sliderEndLabel = QLabel(self.sliderLabels, text="1 sec")
        self.sliderStartLabel = QLabel(self.sliderLabels, text="0.1 sec")

        # Slider Checkbox
        self.autoRefreshButton = QCheckBox(self.autoRefreshWidget, text="Auto-Refresh")
        self.autoRefreshButton.stateChanged.connect(self.beginRefreshTask)

        # Pack Slider Labels Widget
        self.sliderLabelsLayout = QVBoxLayout()
        self.sliderLabelsLayout.addWidget(self.sliderEndLabel, 1, Qt.AlignTop)
        self.sliderLabelsLayout.addWidget(self.sliderStartLabel, 1, Qt.AlignBottom)
        self.sliderLabelsLayout.setContentsMargins(0, 0, 0, 0)
        self.sliderLabels.setLayout(self.sliderLabelsLayout)

        # Pack Slider Widget
        self.sliderWidgetLayout = QHBoxLayout()
        self.sliderWidgetLayout.addWidget(self.autoRefreshSlider)
        self.sliderWidgetLayout.addWidget(self.sliderLabels)
        self.sliderWidget.setLayout(self.sliderWidgetLayout)

        # Pack Auto Refresh Widget
        self.autoRefreshLayout = QVBoxLayout()
        self.autoRefreshLayout.addWidget(self.autoRefreshButton, 1)
        self.autoRefreshLayout.addWidget(self.sliderWidget, 1, Qt.AlignCenter)
        self.autoRefreshWidget.setLayout(self.autoRefreshLayout)

        self.refreshButton = QPushButton(self.toolsWidget, text="Refresh")
        self.refreshButton.setStyleSheet("background-color:#414141;padding:50px;")
        self.refreshButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.refreshButton.clicked.connect(self.refresh)

        # Pack container
        self.toolsLayout = QHBoxLayout()
        self.toolsLayout.addWidget(self.configButton)
        self.toolsLayout.addItem(self.headerSpacer)
        self.toolsLayout.addWidget(self.autoRefreshWidget)
        self.toolsLayout.addWidget(self.refreshButton)
        self.toolsWidget.setLayout(self.toolsLayout)

    def buildTabWidget(self):
        self.tabWidget = QTabWidget(self)

        self.perpUsdtTab = self.buildTab(TYPES[0], "USDT Margin Futures")
        self.perpUniTab = self.buildTab(TYPES[1], "Universal Margin Futures")

    def buildTab(self, types: str, title: str):
        tab = ScreenerTable(self.mAPI, self.headers, types)
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
        if self.autoRefreshButton.isChecked():
            worker = Worker(self.refreshTask)
            worker.signals.finished.connect(worker.stop)
            self.threadpool.start(worker)

    def refreshTask(self):
        while self.autoRefreshButton.isChecked():
            self.refresh()
            time.sleep(self.autoRefreshSlider.value()/10)

    def refresh(self):
        self.tabWidget.currentWidget().getData()
        self.tabWidget.currentWidget().update()
