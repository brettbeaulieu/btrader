from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QHBoxLayout, QSizePolicy, QSpacerItem,
                             QToolButton, QWidget)


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
        self.menuSpacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
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
        self.exitButton = QToolButton(self)
        self.minimizeButton = QToolButton(self)
        self.maximizeButton = QToolButton(self)

        # set auto raise
        self.exitButton.setAutoRaise(True)
        self.minimizeButton.setAutoRaise(True)
        self.maximizeButton.setAutoRaise(True)

        # set button size policies
        self.exitButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.minimizeButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.maximizeButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # set button icons
        self.buildIcons()

        # connect buttons to the corresponding parent widget functions
        self.minimizeButton.clicked.connect(self.p.showMinimized)
        self.maximizeButton.clicked.connect(self.p.maximize)

        self.exitButton.clicked.connect(self.p.close)

    def buildIcons(self):
        # gather images
        maxPic = QPixmap("icons\\fullScreen.png")
        minPic = QPixmap("icons\\minimize-sign.png")
        exitPic = QPixmap("icons\\close.png")

        # create QIcons
        maxIcon = QIcon(maxPic)
        minIcon = QIcon(minPic)
        exitIcon = QIcon(exitPic)

        # set icons
        self.maximizeButton.setIcon(maxIcon)
        self.minimizeButton.setIcon(minIcon)
        self.exitButton.setIcon(exitIcon)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.p.maximized:
            self.p.showNormal()
            self.p.maximized = False
            self.p.move(self.oldPos.x()-(self.p.width()/3), self.oldPos.y())
        delta = QPoint(event.globalPos() - self.oldPos)
        self.p.move(self.p.x() + delta.x(), self.p.y() + delta.y())
        self.oldPos = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        print("Mouse Double Click Event")
        self.p.maximize()
        