import sys

from PyQt5.QtWidgets import QApplication

from source.backend.adapters.bitget.bitget_spot_adapter import BitgetSpotAdapter
from source.frontend.screener.screenerGUI import Screener

if __name__ == "__main__":
    app = QApplication(sys.argv)
    adapter = BitgetSpotAdapter("", "", "")
    gui = Screener(adapter)  # pass the market api to the gui
    gui.show()  # show the gui
    sys.exit(app.exec_())  # execute the app
