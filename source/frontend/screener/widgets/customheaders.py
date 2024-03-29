from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QStyle,
)
from .. import const as c


class CustomHeaders(QWidget):
    """ Parameter:\n dict 'headers', a dictionary of string header labels keyed \
    by their api names. Examples specified in const.py """

    def __init__(self, headers):
        super().__init__()

        self.usedHeaders = headers
        self.unusedHeaders = {
            x: c.ALL_HEADERS[x] for x in set(c.ALL_HEADERS) - set(self.usedHeaders)
        }
        self.initialUsed = self.usedHeaders
        self.initialUnused = self.unusedHeaders

        # create used/unused headers lists
        self.mainLayout = QVBoxLayout()

        self.topWin = QWidget()
        self.topLayout = QHBoxLayout()
        self.topWin.setLayout(self.topLayout)

        self.used = QListWidget()
        self.unused = QListWidget()
        self.topLayout.addWidget(self.used)
        self.topLayout.addWidget(self.unused)

        for x in self.usedHeaders.values():
            self.used.addItem(QListWidgetItem(x))

        for x in self.unusedHeaders.values():
            self.unused.addItem(QListWidgetItem(x))

        # create buttons window
        self.toolsWin = QWidget()
        self.toolsLayout = QHBoxLayout(self.toolsWin)

        self.iconRight = self.style().standardIcon(QStyle.SP_ArrowRight)
        self.iconLeft = self.style().standardIcon(QStyle.SP_ArrowLeft)
        self.iconConfirm = self.style().standardIcon(QStyle.SP_DialogApplyButton)
        self.iconCancel = self.style().standardIcon(QStyle.SP_DialogCancelButton)

        self.unuseButton = QPushButton(self.iconRight, "Make Unused")
        self.useButton = QPushButton(self.iconLeft, "Make Used")
        self.applyButton = QPushButton(self.iconConfirm, "Apply Changes")
        self.discardButton = QPushButton(self.iconCancel, "Discard Changes")

        self.useButton.clicked.connect(self.makeUsed)
        self.unuseButton.clicked.connect(self.makeUnused)
        self.discardButton.clicked.connect(self.close)

        self.toolsWin.setLayout(self.toolsLayout)
        self.toolsLayout.addWidget(self.unuseButton)
        self.toolsLayout.addWidget(self.useButton)
        self.toolsLayout.addWidget(self.applyButton)
        self.toolsLayout.addWidget(self.discardButton)
        # final pack
        self.mainLayout.addWidget(self.topWin)
        self.mainLayout.addWidget(self.toolsWin)
        self.setLayout(self.mainLayout)

        # show ui
        self.show()

    def makeUsed(self):
        if self.unused.currentItem() is None:
            return
        newUsed = self.unused.takeItem(self.unused.currentRow())
        self.used.addItem(newUsed)

    def makeUnused(self):
        if self.used.currentItem() is None:
            return

        # Remove from used item list, add to unused item list
        newUnusedItem = self.used.takeItem(self.used.currentRow())
        self.unused.addItem(newUnusedItem)

        # Get key from value
        key_list = list(self.usedHeaders.keys())
        val_list = list(self.usedHeaders.values())
        solve = key_list[val_list.index(newUnusedItem.text())]
        # Remove from usedHeaders, add to unusedHeaders
        newUnusedData = self.usedHeaders.pop(solve)
        self.unusedHeaders[solve] = newUnusedData
