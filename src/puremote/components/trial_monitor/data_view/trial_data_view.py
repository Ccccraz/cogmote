import sys

from puremote.shared.web_requests.http_listener import HttpListener, HttpListenerSse
from puremote.models.trail_data import TrialDataModel, trial_data_store

from PySide6.QtCore import Signal, QThread, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication

from qfluentwidgets import TableWidget, TableView


class TrialDataView(QWidget):
    received = Signal()

    def __init__(self, parnet) -> None:
        super().__init__(parent=parnet)
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)

        self.table = TableWidget()
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().font().setPointSize(16)

        self.table.setRowCount(10)
        self.table.setColumnCount(10)
        self.layout_main.addWidget(self.table)

    def init_listener(self, address: str, option: str) -> None:
        self.address = address
        self.listener_thread = QThread(self)

        if option == "sse":
            self.listener = HttpListenerSse(address)
        elif option == "polling":
            self.listener = HttpListener(address)

        self.listener.moveToThread(self.listener_thread)

        self.listener_thread.started.connect(self.listener.run)
        self.listener_thread.finished.connect(self.listener_thread.deleteLater)

        self.listener.finished.connect(self.listener_thread.quit)
        self.listener.finished.connect(self.listener.deleteLater)
        self.listener.received.connect(self._update_view)

        self._is_init = False
        self.listener_thread.start()

    @Slot(str)
    def _update_view(self, data) -> None:
        if self._is_init is not True:
            self.layout_main.removeWidget(self.table)
            self.table.deleteLater()

            self.data_model = TrialDataModel(data)
            trial_data_store.add_data("Tmp", self.address, self.data_model)
            self.table = TableView()
            self.table.setBorderVisible(True)
            self.table.setBorderRadius(8)
            self.table.verticalHeader().setVisible(False)
            self.table.setModel(self.data_model)
            self.layout_main.addWidget(self.table)
            self._is_init = True
        else:
            self.data_model.insert_new_data(data)
            self.table.resizeColumnsToContents()
            self.table.scrollToBottom()

    def stop(self) -> None:
        if self.listener is not None:
            self.listener.stop()


if __name__ == "__main__":
    from PySide6.QtWidgets import QMainWindow

    app = QApplication(sys.argv)

    class MainWindow(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("Trial Data View")
            self.resize(800, 600)
            self.setCentralWidget(TrialDataView())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
