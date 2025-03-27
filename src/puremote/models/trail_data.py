from dataclasses import dataclass
from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
)
from PySide6.QtGui import QFont
import json


class TrialDataModel(QAbstractTableModel):
    def __init__(self, data: str) -> None:
        super().__init__()
        self._data = [json.loads(data)] or []

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self._data) if self._data else 0

    def columnCount(
        self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()
    ) -> int:
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self._data[index.row()]
            keys = list(row.keys())
            return row[keys[index.column()]]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter

        if role == Qt.ItemDataRole.FontRole:
            return QFont(["Arial"], pointSize=10)

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return list(self._data[0].keys())[section]

        if role == Qt.ItemDataRole.FontRole:
            font = QFont(["Arial"], pointSize=13)
            font.setBold(True)
            return font

        return None

    def insert_new_data(self, row_data: str):
        position = len(self._data)
        self.beginInsertRows(QModelIndex(), position, position)
        self._data.append(json.loads(row_data))
        self.endInsertRows()


@dataclass
class TrialData:
    nickname: str
    address: str
    data: TrialDataModel


class TrialDataStore():
    def __init__(self) -> None:
        self._store: dict[str, TrialData] = {}

    def add_data(self, nickname: str, address: str, trial_data: TrialDataModel) -> None:
        data = TrialData(nickname, address, trial_data)
        self._store[address] = data

    @property
    def data(self):
        return self._store

trial_data_store = TrialDataStore()
