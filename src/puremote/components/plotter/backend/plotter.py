import numpy as np

from PySide6.QtCore import Slot, QModelIndex
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas  # type: ignore
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar  # type: ignore

from puremote.models.trail_data import TrialDataModel, trial_data_store
from puremote.config.config import FigureConfig


class Plotter(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)

    def initialize_plot(self, figure_config: FigureConfig, data_address: str):
        # Create a plotter
        self.figure_config = figure_config
        self.data_address = data_address

        self.xvalue = [
            item[self.figure_config.x_axis]
            for item in trial_data_store.data[self.data_address].data._data
        ]
        self.yvalue = [
            item[self.figure_config.y_axis]
            for item in trial_data_store.data[self.data_address].data._data
        ]

        if self.figure_config.figure_type == "line":
            (self.line,) = self.ax.plot(self.xvalue, self.yvalue)
            self.xdata = self.line.get_xdata()
            self.ydata = self.line.get_ydata()
            trial_data_store.data[self.data_address].data.rowsInserted.connect(
                self.update_line
            )

        elif self.figure_config.figure_type == "scatter":
            self.scat = self.ax.scatter(self.xvalue, self.yvalue)
            trial_data_store.data[self.data_address].data.rowsInserted.connect(
                self.update_line
            )
            

        self.ax.set_title(self.figure_config.nickname)
        self.ax.set_xlabel(self.figure_config.x_axis)
        self.ax.set_ylabel(self.figure_config.y_axis)

        self.raw_data = trial_data_store.data[self.data_address].data._data

    @Slot(QModelIndex, int, int)
    def update_line(self, parent: QModelIndex, first: int, last: int):
        # Update the plot if new data is added
        data = self.raw_data[first]

        self.xdata = np.append(self.xdata, data[self.figure_config.x_axis])
        self.ydata = np.append(self.ydata, data[self.figure_config.y_axis])

        self.line.set_data(self.xdata, self.ydata)

        self.ax.relim()
        self.ax.autoscale_view()

        self.line.figure.canvas.draw_idle()  # type: ignore

    @Slot(QModelIndex, int, int)
    def update_scatter(self, parent: QModelIndex, first: int, last: int):
        # Update the plot if new data is added
        data = self.raw_data[first]

        self.scat.set_offsets(np.c_[data[self.figure_config.x_axis], data[self.figure_config.y_axis]])
        self.ax.relim()
        self.ax.autoscale_view()

        self.scat.figure.canvas.draw_idle()  # type: ignore



if __name__ == "__main__":
    import sys
    import random
    from tqdm.rich import tqdm

    item_1 = {"x": 1, "y": 2}
    data = TrialDataModel(item_1)

    for _ in tqdm(range(1000)):
        data.insert_new_data({"x": random.random(), "y": random.random()})

        trial_data_store.add_data("test", data)

    app = QApplication(sys.argv)

    widget = Plotter()
    widget.initialize_plot("x", "y", "test")
    widget.show()

    sys.exit(app.exec())
