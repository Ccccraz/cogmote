from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QFormLayout,
)

from qfluentwidgets import (
    EditableComboBox,
    BodyLabel,
    ComboBox,
    Dialog,
)

from puremote.config.config import config_store, TrialDataConfig


class AddTrialDataDialog(Dialog):
    emit_accept = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(self.tr("Add trial data"), "", parent)
        self.__init_ui()

    def __init_ui(self):
        self.setTitleBarVisible(False)
        self.setFixedSize(640, 320)

        self.layout_sub = QFormLayout()
        self.textLayout.addLayout(self.layout_sub)

        # Create input component
        self._init_status_server()

        self.yesButton.clicked.connect(self._emit_accept)
        self.yesButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def _init_status_server(self) -> None:
        """
        Create input component
        """
        trial_config: list[TrialDataConfig] = config_store.config.trial_data

        # Create Nickname input component
        label_nickname = BodyLabel(self.tr("Nickname : "))
        self.combobox_nickname = EditableComboBox()
        self.combobox_nickname.setPlaceholderText(self.tr("Input a nickname"))

        item_list = [i.nickname for i in trial_config]
        self.combobox_nickname.addItems(item_list)

        self.layout_sub.addRow(label_nickname, self.combobox_nickname)

        # Create Address input component
        label_address = BodyLabel(self.tr("Server : "))
        self.combobox_address = EditableComboBox()
        self.combobox_address.setPlaceholderText(self.tr("Input server address"))

        item_list = [i.address for i in trial_config]
        self.combobox_address.addItems(item_list)

        # Add input component to layout
        self.layout_sub.addRow(label_address, self.combobox_address)

        # Create Listen Mode input component
        label_mode = BodyLabel(self.tr("Server type: "))
        self.combobox_mode = ComboBox()
        item_list = ["sse", "polling"]
        self.combobox_mode.addItems(item_list)
        self.layout_sub.addRow(label_mode, self.combobox_mode)

        # Connect signal
        self.combobox_nickname.textActivated.connect(self._update_by_nickname)
        self.combobox_address.textActivated.connect(self._update_by_address)

    @Slot(str)
    def _update_by_nickname(self, nickname: str):
        self.combobox_address.setCurrentText(
            config_store.trial_data_nickname[nickname].address
        )
        self.combobox_mode.setCurrentText(
            config_store.trial_data_nickname[nickname].mode
        )

    @Slot(str)
    def _update_by_address(self, address: str):
        self.combobox_nickname.setCurrentText(
            config_store.trial_data_address[address].nickname
        )
        self.combobox_mode.setCurrentText(config_store.trial_data_address[address].mode)

    def _emit_accept(self) -> None:
        nickname = self.combobox_nickname.currentText()
        address = self.combobox_address.currentText()
        mode = self.combobox_mode.currentText()

        new_config = TrialDataConfig(nickname, address, mode)

        config_store.add_trial_data(new_config)

        self.emit_accept.emit(nickname, address, mode)
