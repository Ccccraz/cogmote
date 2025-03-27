import httpx
from httpx_sse import connect_sse

from loguru import logger

from PySide6.QtCore import QObject, Signal, Slot, QThread


class HttpListener(QObject):
    def __init__(self, address: str) -> None:
        super().__init__()
        self.url = address

    @Slot()
    def stop(self) -> None:
        self.is_running = False

    @Slot()
    def listen(self):
        self.is_running = True
        previous_id = 0

        logger.info(f"Listening on {self.url}")

        with httpx.Client() as client:
            while self.is_running:
                try:
                    response = client.get(self.url, timeout=None)

                    if response.status_code == httpx.codes.OK:
                        data: dict = response.text()
                        trial_id = data["trialID"]
                        if trial_id != previous_id:
                            previous_id = trial_id
                            yield data
                        QThread.msleep(1000)

                except httpx.ConnectError:
                    logger.error("Server not running")


class HttpListenerSse(QObject):
    received = Signal(str)
    finished = Signal()

    def __init__(self, address: str) -> None:
        super().__init__()
        self.url = address
        self.client = httpx.Client()

    @Slot()
    def stop(self) -> None:
        self.client.close()

    @Slot()
    def run(self):
        logger.info(f"Listening on {self.url}")

        try:
            with connect_sse(
                self.client, "GET", self.url, timeout=None
            ) as event_source:
                for sse in event_source.iter_sse():
                    self.received.emit(sse.data)
        except Exception as e:
            logger.error(f"Listener crashed: {str(e)}")
        finally:
            self.finished.emit()


if __name__ == "__main__":
    import sys
    from PySide6.QtCore import QThread
    from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow

    class MainWindow(QMainWindow):
        def __init__(self) -> None:
            super().__init__()
            self.setWindowTitle("Test")
            self.setup_thread()
            self.button = QPushButton("Test")
            self.button.clicked.connect(self.on_button_click)
            self.setCentralWidget(self.button)

        def setup_thread(self):
            self.test_thread = QThread()
            self.listener = HttpListenerSse("http://localhost:9012/data")
            self.listener.moveToThread(self.test_thread)

            self.test_thread.started.connect(self.listener.run)
            self.listener.finished.connect(self.test_thread.quit)
            self.listener.finished.connect(self.listener.deleteLater)
            self.test_thread.finished.connect(self.test_thread.deleteLater)
            self.listener.received.connect(self.on_received)

        @Slot(str)
        def on_received(self, data: str):
            print(data)

        @Slot()
        def on_button_click(self):
            self.test_thread.start()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
