import sys
from PyQt5.QtWidgets import QApplication
from screener.screenerGUI import Screener
from adapters.bitget_adapter.bitget.mix.market_api import MarketApi as MarketAPI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mAPI = MarketAPI("","","")  # no api keys needed for market data
    gui = Screener(mAPI)  # pass the market api to the gui
    gui.show()  # show the gui
    sys.exit(app.exec_())  # execute the app
