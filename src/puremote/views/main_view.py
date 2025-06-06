from PySide6.QtCore import QSize
from qfluentwidgets import FluentWindow, SplashScreen, setTheme, Theme, FluentIcon
from puremote.config.config import APP_NAME
from puremote.views.experiments_view.experiments_view import ExperimentsInterface


class MainWindow(FluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWindow()

        setTheme(Theme.DARK)

        self.experiments_interface = ExperimentsInterface(self)
        self.initNavigation()

        self.splashScreen.finish()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowTitle(APP_NAME)
        self.setMicaEffectEnabled(False)

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))

        self.show()

    def initNavigation(self):
        """Init sidebar navigation"""
        self.addSubInterface(
            self.experiments_interface,
            FluentIcon.CAMERA,
            "Monitor",
            isTransparent=True,
        )
