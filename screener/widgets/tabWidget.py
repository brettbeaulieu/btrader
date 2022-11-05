
from PyQt5.QtWidgets import QTabWidget

class ScreenerTabs(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        

