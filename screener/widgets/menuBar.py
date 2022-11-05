from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QSizePolicy,
                             QSpacerItem, QWidget)


class MenuBar(QWidget):
    def __init__(self, parent):
        self.p = parent
        super().__init__(parent)
        self.setStyleSheet("background-color: #414141;")
        self.buildMenuBar()

    def buildMenuBar(self):

        self.mainWidget = QWidget(self)

        # build minimize, maximize, and exit buttons
        self.buildButtons()

        # create menu bar layout
        self.menuSpacer = QSpacerItem(
            1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.menuBarLayout = QHBoxLayout(self.mainWidget)
        self.menuBarLayout.setContentsMargins(0, 0, 0, 0)
        self.menuBarLayout.addSpacerItem(self.menuSpacer)
        self.menuBarLayout.addWidget(self.minimizeButton)
        self.menuBarLayout.addWidget(self.maximizeButton)
        self.menuBarLayout.addWidget(self.exitButton)
        self.mainWidget.setLayout(self.menuBarLayout)

        # create main layout
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.mainWidget)
        self.setLayout(self.mainLayout)

    def buildButtons(self):
        # create buttons
        self.exitButton = QPushButton(self)
        self.minimizeButton = QPushButton(self)
        self.maximizeButton = QPushButton(self)

        # set button size
        self.exitButton.setFixedWidth(60)
        self.minimizeButton.setFixedWidth(60)
        self.maximizeButton.setFixedWidth(60)

        # set button stylesheets
        self.exitButton.setStyleSheet(
            "QPushButton { border:none; padding: 15px; } QPushButton:hover {background-color: red;}")
        self.minimizeButton.setStyleSheet(
            "QPushButton { border:none; padding: 15px; } QPushButton:hover {background-color: #545454;}")
        self.maximizeButton.setStyleSheet(
            "QPushButton { border:none; padding: 15px; } QPushButton:hover {background-color: #545454;}")

        # set button icons
        self.buildIcons()

        # connect buttons to the corresponding parent widget functions
        self.minimizeButton.clicked.connect(self.p.showMinimized)
        self.maximizeButton.clicked.connect(self.p.maximize)

        self.exitButton.clicked.connect(self.p.close)

    def buildIcons(self):
        # gather images
        maxPic = QPixmap("icons\\white\\fullScreen.png")
        minPic = QPixmap("icons\\white\\minimize-sign.png")
        exitPic = QPixmap("icons\\white\\close.png")

        # create QIcons
        maxIcon = QIcon(maxPic)
        minIcon = QIcon(minPic)
        exitIcon = QIcon(exitPic)

        # set icons
        self.maximizeButton.setIcon(maxIcon)
        self.minimizeButton.setIcon(minIcon)
        self.exitButton.setIcon(exitIcon)
        
        self.maximizeButton.setIconSize(QSize(10, 10))
        self.minimizeButton.setIconSize(QSize(10, 10))
        self.exitButton.setIconSize(QSize(10, 10))

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        # handling to prevent error calculating delta when oldPos is not defined
        if not hasattr(self, 'oldPos'):
            self.oldPos = event.globalPos()

        if self.p.maximized:
            self.p.showNormal()
            self.p.maximized = False
            self.p.move(int(self.oldPos.x()-(self.p.width()/3)),
                        self.oldPos.y())
        delta = QPoint(event.globalPos() - self.oldPos)

        self.p.move(self.p.x() + delta.x(), self.p.y() + delta.y())
        self.oldPos = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        self.p.maximize()
