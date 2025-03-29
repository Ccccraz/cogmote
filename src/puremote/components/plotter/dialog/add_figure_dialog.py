from typing import Callable
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

from puremote.config.config import config_store
from puremote.config.config import TrialDataConfig, FigureConfig
from puremote.common.logger import logger
from puremote.models.trail_data import trial_data_store


class AddFigureDialog(Dialog):
    """Dialog to select a figure to plot"""

    emit_accepted = Signal(FigureConfig, str)

    def __init__(self, parent=None):
        super().__init__(self.tr("Add figure"), "", parent)
        self._init_ui()

    def _init_ui(self):
        self.setTitleBarVisible(False)
        self.setFixedSize(640, 320)

        self.layout_input = QFormLayout()

        self.textLayout.addLayout(self.layout_input)

        self._init_plotter()

        self.yesButton.clicked.connect(self._emit_accepted)
        self.yesButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def _init_plotter(self):
        # Add Plot data source
        data = trial_data_store.data

        # Add data nickname
        label_nickname = BodyLabel(self.tr("data_nickname"))
        self.combobox_nickname = ComboBox()

        data_items = [i.nickname for i in data.values()]

        self.combobox_nickname.addItems(data_items)
        self.layout_input.addRow(label_nickname, self.combobox_nickname)

        # Add data address
        label_data = BodyLabel(self.tr("data_address"))
        self.combobox_address = ComboBox()

        data_items = [i for i in data.keys()]

        self.combobox_address.addItems(data_items)
        self.layout_input.addRow(label_data, self.combobox_address)

        # Add figure nickname
        label_figure_nickname = BodyLabel(self.tr("figure"))
        self.combobox_figure_nickname = EditableComboBox()
        self.layout_input.addRow(label_figure_nickname, self.combobox_figure_nickname)

        # Add x axis data
        labels_xaxis = BodyLabel(self.tr("x axis"))
        self.combo_box_xaxis = EditableComboBox()
        self.layout_input.addRow(labels_xaxis, self.combo_box_xaxis)

        # Add y axis data
        label_yaxis = BodyLabel(self.tr("y axis"))
        self.combo_box_yaxis = EditableComboBox()
        self.layout_input.addRow(label_yaxis, self.combo_box_yaxis)

        # Add figure type
        label_type = BodyLabel(self.tr("type"))
        self.combo_box_type = EditableComboBox()
        self.combo_box_type.addItems(["line", "scatter"])
        self.layout_input.addRow(label_type, self.combo_box_type)

        # Add data update logic
        self.combobox_nickname.currentTextChanged.connect(self._update_by_nickname)
        self.combobox_address.currentTextChanged.connect(self._update_by_address)
        self.combobox_figure_nickname.currentTextChanged.connect(self._update_by_figure)

        # Add initial data
        self._update_by_address(self.combobox_address.currentText())

    def _emit_accepted(self):
        """Emit accepted signal with selected data"""
        if self.trial:
            figure_nickname = self.combobox_figure_nickname.currentText()
            x_axis = self.combo_box_xaxis.currentText()
            y_axis = self.combo_box_yaxis.currentText()
            figure_type = self.combo_box_type.currentText()

            new_figure = FigureConfig(figure_nickname, x_axis, y_axis, figure_type)

            config_store.add_figure(self.trial.address, new_figure)

            self.emit_accepted.emit(
                new_figure,
                self.combobox_address.currentText(),
            )

    @Slot(str)
    def _update_by_nickname(self, nickname: str):
        self._update_trial_data(
            lambda trial: trial.nickname == nickname, "nickname", nickname
        )

    @Slot(str)
    def _update_by_address(self, address: str):
        self._update_trial_data(
            lambda trial: trial.address == address, "address", address
        )

    def _update_trial_data(
        self,
        condition: Callable[[TrialDataConfig], bool],
        condition_type: str,
        condition_value,
    ):
        self.combo_box_xaxis.clear()
        self.combo_box_yaxis.clear()
        self.combobox_figure_nickname.clear()

        self.trial = next(
            (trial for trial in config_store.config.trial_data if condition(trial)),
            None,
        )

        if not self.trial:
            return

        if condition_type == "nickname":
            self.combobox_address.setCurrentText(self.trial.address)
        elif condition_type == "address":
            self.combobox_nickname.setCurrentText(self.trial.nickname)

        self.combo_box_xaxis.addItems(trial_data_store.labels(self.trial.address))
        self.combo_box_yaxis.addItems(trial_data_store.labels(self.trial.address))

        if self.trial.figures:
            nickname = [figure.nickname for figure in self.trial.figures]
            self.combobox_figure_nickname.addItems(nickname)
        else:
            logger.warning(f"No figure found for {condition_type}: {condition_value}")

    def _update_by_figure(self, figure_name: str):
        if self.trial:
            figure = next(
                (i for i in self.trial.figures if i.nickname == figure_name),
                None,
            )

            if figure:
                self.combo_box_xaxis.setCurrentText(figure.x_axis)
                self.combo_box_yaxis.setCurrentText(figure.y_axis)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog = AddFigureDialog()
    dialog.show()

    sys.exit(app.exec())
