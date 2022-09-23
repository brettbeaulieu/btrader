import datetime
import operator

from PyQt5.QtGui import QColor
from PyQt5.QtCore import QModelIndex, Qt, QVariant, QAbstractTableModel, QModelIndex


class ScreenerModel(QAbstractTableModel):
    def __init__(self, headers):
        super().__init__()
        self._data = []
        self._headers = headers

    def addData(self, data):
        try:
            self.setData(data)
        except ValueError:
            row = len(self._data)
            self.beginInsertRows(QModelIndex(), row, row)
            self._data.append(data)
            self.endInsertRows()

    def setData(self, data):
        index = [x[0] for x in self._data].index(data[0])
        self._data[index] = data

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()):
        if (row >= 0) and (row < self.rowCount(0)):
            if (column >= 0) and (column < self.columnCount(0)):
                return self.createIndex(row, column, self._data[row][column])
        return QModelIndex()

    def data(self, index, role):
        # Text Alignment
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        # Generally percent column
        if index.column() == 6:
            # Text Coloration. Try Qt.BackgroundRole for background colors. :D
            if role == Qt.ForegroundRole:
                if self._data[index.row()][index.column()] > 0:
                    return QColor(100, 255, 100)
                elif self._data[index.row()][index.column()] < 0:
                    return QColor(255, 100, 100)
            if role == Qt.DisplayRole:
                temp = self._data[index.row()][index.column()]*100
                return (str(round(temp, 2))+"%")

        if role == Qt.DisplayRole:
            if self._headers[index.column()].find("Time") != -1:
                val = int(self._data[index.row()][index.column()])
                val2 = datetime.datetime.fromtimestamp(val / 1000)
                return val2.strftime("%m/%d %H:%M")
            return self._data[index.row()][index.column()]

    def setHeaderData(self, column, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            self._headers[column] = data
            return True
        return super().setHeaderData(column, orientation, data, role)

    def headerData(self, column, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[column]
        return super().headerData(column, orientation, role)

    def sort(self, col: int, order):
        """Sort table by given column number."""
        if len(self._data) > 0:
            self._data = sorted(self._data, key=operator.itemgetter(col))

            if order == Qt.DescendingOrder:
                self._data.reverse()
            self.layoutChanged.emit()
            # self.emit(SIGNAL("layoutAboutToBeChanged()"))
            # self.emit(SIGNAL("layoutChanged()"))

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)
