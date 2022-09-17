from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPointF
from . import utils
from dateutil import parser

class TrackerGUI(QWidget):

    def __init__(self, csvpath):
        super().__init__()
        self.setWindowTitle("Portfolio Tracker")
        self.setGeometry(0,0,1280,720)
        self.build_chart(csvpath)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.chartview)
        self.layout.addWidget(self.tradeTable)
        self.setLayout(self.layout)
        self.show()


    def build_chart(self, csvpath):
        self.chart = QChart()

        self.build_line_portfolio(csvpath)
        
        self.xaxis = QDateTimeAxis(self)
        self.xaxis.setTickCount(10)
        self.xaxis.setFormat("MMM dd, yyyy")
        self.xaxis.setTitleText("Date")
        self.chart.addAxis(self.xaxis, Qt.AlignBottom)
        self.portfolio_series.attachAxis(self.xaxis)

        self.yaxis = QValueAxis(self)
        self.yaxis.setTickCount(11)
        self.yaxis.setLabelFormat("$%.2f")
        self.yaxis.setTitleText("Value")
        self.yaxis.setRange(0,100)
        self.chart.addAxis(self.yaxis, Qt.AlignLeft)
        self.portfolio_series.attachAxis(self.yaxis)
        

        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Portfolio")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)


        self.chartview = QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.Antialiasing)

    def build_line_portfolio(self, csvpath:str, feesOn:bool=True, startDate:str="", endDate:str=""):
        # temp stuffs
        self.csv = utils.convertCSV(csvpath)
        self.balance_series = utils.getBalanceSeries(self.csv,feesOn,startDate,endDate)
        
        self.portfolio_series = QLineSeries(self)
        for data in self.balance_series:
            epoch = parser.parse(data[0]).timestamp()*1000
            self.portfolio_series.append(epoch,data[1])

        self.chart.addSeries(self.portfolio_series)

    def build_trade_table(self, csvpath:str,feesOn:bool=True, startDate:str="", endDate:str=""):
