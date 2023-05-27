from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QCheckBox, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt


class SliderWidget(QWidget):
    def __init__(self, parent):
        self.p = parent
        super().__init__(parent)
        self.buildSlider()

    def buildSlider(self):
        # Slider Stuff

        self.sliderWidget = QWidget(self)
        self.slider = QSlider(Qt.Vertical, self.sliderWidget)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setRange(1,10)
        self.slider.valueChanged.connect(
            lambda: self.slider.setToolTip(str(self.slider.value()/10)+" secs")
            )
        # Slider Labels
        self.labels = QWidget(self.sliderWidget)
        self.endLabel = QLabel(self.labels, text="1 sec")
        self.startLabel = QLabel(self.labels, text="0.1 sec")

        # Slider Checkbox
        self.button = QCheckBox(self, text="Auto-Refresh")
        self.button.stateChanged.connect(self.p.beginRefreshTask)

        # Pack Slider Labels Widget
        self.labelsLayout = QVBoxLayout()
        self.labelsLayout.addWidget(self.endLabel, 1, Qt.AlignTop)
        self.labelsLayout.addWidget(self.startLabel, 1, Qt.AlignBottom)
        self.labelsLayout.setContentsMargins(0, 0, 0, 0)
        self.labels.setLayout(self.labelsLayout)

        # Pack Slider Widget
        self.sliderWidgetLayout = QHBoxLayout()
        self.sliderWidgetLayout.addWidget(self.slider)
        self.sliderWidgetLayout.addWidget(self.labels)
        self.sliderWidget.setLayout(self.sliderWidgetLayout)

        # Pack Auto Refresh Widget
        self.autoRefLayout = QVBoxLayout()
        self.autoRefLayout.addWidget(self.button, 1)
        self.autoRefLayout.addWidget(self.sliderWidget, 1, Qt.AlignCenter)
        self.setLayout(self.autoRefLayout)


