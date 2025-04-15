import datetime
from pathlib import Path
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

from furl import furl
from qfluentwidgets import StateToolTip
from puremote.common.logger import logger

import subprocess


class WebRTCBackend(QWidget):
    def __init__(
        self,
        address,
        record: bool = False,
        target_floder: str = "",
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.address = furl(address)
        self.address /= "whep"

        self.need_record = record
        self.target_floder = target_floder

        self.playing = False
        self.recording = False

        self.layout_main = QVBoxLayout()
        self.browser = QWebEngineView()

        self.browser.setUrl(QUrl(address))

        self.layout_main.addWidget(self.browser)
        self.setLayout(self.layout_main)

        if self.need_record:
            self.record(target_floder)

    def record(self, target_floder: str) -> None:
        target_file_new = (
            Path(target_floder)
            / f"{datetime.datetime.now().strftime(r'%Y%m%d_%H%M%S')}.mkv"
        )

        print(self.address)
        print(target_file_new.absolute())

        command = [
            "gst-launch-1.0.exe",
            "-e",
            "whepsrc",
            f"whep-endpoint={self.address}",
            "use-link-headers=true",
            'video-caps="application/x-rtp,media=video,encoding-name=H264,payload=127,clock-rate=90000"',
            'audio-caps="application/x-rtp,media=audio,encoding-name=PCMU,payload=0,clock-rate=8000"',
            "!",
            "rtph264depay",
            "!",
            "h264parse",
            "!",
            "matroskamux!",
            "filesink",
            f"location={target_file_new.as_posix()}",
        ]

        self.process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        self.recording = True

        self.stateTooltip = StateToolTip(
            self.tr("Recording"), str(target_file_new), self.window()
        )

        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()

    def stop_play(self) -> None:
        pass

    def stop_record(self) -> None:
        if self.recording:
            logger.info("stoping record")
            assert self.stateTooltip is not None
            self.stateTooltip.setContent(self.tr("Stoping record"))
            self.stateTooltip.setState(True)
            self.stateTooltip = None
            self.process.terminate()
            self.recording = False
        try:
            self.process.wait(5)
        except subprocess.TimeoutExpired:
            self.process.kill()


if __name__ == "__main__":
    app = QApplication([])

    window = WebRTCBackend("http://localhost:8889/mystream")
    window.show()
    window.record(r"C:\Users\ccccr\repo")

    app.exec()
