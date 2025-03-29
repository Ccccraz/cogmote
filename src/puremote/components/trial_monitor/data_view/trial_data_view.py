import sys

from puremote.shared.web_requests.http_listener import HttpListener, HttpListenerSse
from puremote.models.trail_data import TrialDataModel, trial_data_store

from PySide6.QtCore import Signal, QThread, Slot, QObject
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication

from qfluentwidgets import TableView


class TrialDataView(QWidget):
    received = Signal()

    def __init__(self, parnet) -> None:
        super().__init__(parent=parnet)

        # Init Trial data view basic layout
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)

    def init_listening(self, nickname: str, address: str, mode: str) -> None:
        self.init_listening_thread(nickname, address, mode)
        self.init_data_process_thread()
        self.start_thread()

    def init_listening_thread(self, nickname: str, address: str, mode: str) -> None:
        # attributes of data source
        self.nickname = nickname
        self.address = address

        # Init listening thread
        self.listener_thread = QThread(self)

        ## Select listener mode
        if mode == "sse":
            self.listener = HttpListenerSse(address)
        elif mode == "polling":
            self.listener = HttpListener(address)

        self.listener.moveToThread(self.listener_thread)

    def init_data_process_thread(self) -> None:
        self.data_processor = DataProcess()

        self.data_process_thread = QThread(self)
        self.data_processor.moveToThread(self.data_process_thread)

    def start_thread(self) -> None:
        # TODO: Multi threading support for polling mode
        # start listener when thread started
        self.listener_thread.started.connect(self.listener.run)  # type: ignore

        # send data to trial data view
        self.listener.received.connect(self._init_trialview)  # type: ignore
        self.data_processor.finished.connect(self._handle_process_finished)

        # start listening thread
        self.listener_thread.start()
        self.data_process_thread.start()

        # attributes for first time update
        self._is_init = False

    @Slot(str)
    def _init_trialview(self, data) -> None:
        if self._is_init is not True:
            self.data_model = TrialDataModel(data)
            trial_data_store.add_data(self.nickname, self.address, self.data_model)

            self.table = TableView()

            self.table.setBorderVisible(True)
            self.table.setBorderRadius(8)
            self.table.verticalHeader().setVisible(False)
            self.table.setModel(self.data_model)
            self.layout_main.addWidget(self.table)

            self.data_processor.data = self.data_model
            self.table.resizeColumnToContents(0)

            self._is_init = True
        else:
            self.data_processor.update(data)

    @Slot()
    def _handle_process_finished(self) -> None:
        self.table.scrollToBottom()

    def stop(self) -> None:
        print("Stop listening")
        if self.listener is not None:
            self.listener.stop()

            self.listener_thread.quit()
            self.listener_thread.wait()
            self.listener.deleteLater()
            self.listener_thread.deleteLater()
            
            self.data_process_thread.quit()
            self.data_process_thread.wait()
            self.data_processor.deleteLater()
            self.data_process_thread.deleteLater()

            self.layout_main.removeWidget(self.table)
            self.table.deleteLater()
            trial_data_store.remove_data(self.address)
            self.data_model.deleteLater()

    def closeEvent(self, event: QCloseEvent):
        print("Close Event")
        self.stop()
        return super().closeEvent(event)


class DataProcess(QObject):
    finished = Signal()

    def __init__(self, parnet=None) -> None:
        super().__init__(parent=parnet)
        self.data: TrialDataModel | None = None

    @Slot(str)
    def update(self, data: str) -> None:
        assert self.data is not None
        self.data.insert_new_data(data)
        self.finished.emit()


if __name__ == "__main__":
    from PySide6.QtWidgets import QMainWindow

    app = QApplication(sys.argv)

    class MainWindow(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("Trial Data View")
            self.resize(800, 600)
            self.setCentralWidget(TrialDataView(self))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
