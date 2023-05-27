import sys
from PyQt5.QtWidgets import QApplication
from source.screener.screenerGUI import Screener
from source.adapters.bitget.bitget_spot_adapter import BitgetSpotAdapter
from source.adapters.bitget.bitget_sdk.mix.market_api import MarketApi as MarketAPI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    adapter = BitgetSpotAdapter("","","")
    gui = Screener(adapter)  # pass the market api to the gui
    gui.show()  # show the gui
    sys.exit(app.exec_())  # execute the app
