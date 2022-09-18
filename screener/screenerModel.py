from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QModelIndex


class ScreenerModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headers):
        super(ScreenerModel, self).__init__()
        self._data = data
        self._headers = headers
        
    def addData(self, data):
        self._data[data[0]] = data

    def data(self, index, role):
        if len(self._data)==0:
            return ""
        row = list(self._data.keys())[index.row()]
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[row][index.column()]

    def setHeaderData(self, section, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self._headers[section] = data
                return True
            except:
                return False
        return super().setHeaderData(section, orientation, data, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self._headers[section]
            except:
                pass
        return super().headerData(section, orientation, role)

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if len(self._data) > 0:
            val1 = list(self._data.keys())[0]
            return len(self._data[val1])
        return 0