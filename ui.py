#import from packages
from PySide6.QtWidgets import (
    QWidget, 
    QPushButton, 
    QLabel, 
    QVBoxLayout,
    QFileDialog,
    QSpinBox
    )

from PySide6.QtGui import QFont

from audio import load_audio

from export import Exporter

import os

from waveform import WaveformWidget

RESLICE_LOGO = """
██████╗ ███████╗███████╗██╗     ██╗ ██████╗███████╗
██╔══██╗██╔════╝██╔════╝██║     ██║██╔════╝██╔════╝
██████╔╝█████╗  ███████╗██║     ██║██║     █████╗
██╔══██╗██╔══╝  ╚════██║██║     ██║██║     ██╔══╝
██║  ██║███████╗███████║███████╗██║╚██████╗███████╗
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝╚══════╝  
 SIMPLESLICER // DEVELOPED BY KAITELMC // ver0.1   
"""
class MainWindow(QWidget):
    def __init__(self):
        super(). __init__()
        self.setWindowTitle("ReSlice v0.1")
        self.setFixedSize(800,600)

        layout = QVBoxLayout()

        self.logo_label = QLabel(RESLICE_LOGO)

        self.load_button = QPushButton("Load WAV")
        self.export_button = QPushButton("Export")

        self.slice_selector = QSpinBox()
        self.slices_label = QLabel("Slices")
        self.slice_selector.setMinimum(4)
        self.slice_selector.setMaximum(32)
        self.slice_selector.setValue(4)

        self.logo_label.setStyleSheet("""
    QLabel {
        font-family: Consolas;
        font-size: 8pt;
        color: white;
    }
""")


        self.file_label = QLabel("File: None")
        self.sample_rate_label = QLabel("Sample Rate: --")
        self.length_label = QLabel("Length: --")
        self.channels_label = QLabel("Channels: --")

        self.exporter = Exporter()
        self.filename = None
        self.data = None
        self.samplerate = None
        self.info = None

        self.waveform = WaveformWidget()

        layout.addWidget(self.logo_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.sample_rate_label)
        layout.addWidget(self.length_label)
        layout.addWidget(self.channels_label)
        layout.addWidget(self.waveform)
        layout.addWidget(self.slice_selector)
        layout.addWidget(self.slices_label)
        layout.addWidget(self.export_button)


        self.setLayout(layout)
        self.load_button.clicked.connect(self.load_wav)
        self.export_button.clicked.connect(self.export_slices)
        self.slice_selector.valueChanged.connect(self.set_slice_count)

    def set_slice_count(self, slice_count_value):
        self.waveform.set_slice_count(slice_count_value)


    def load_wav(self):
        self.filename, _ = QFileDialog.getOpenFileName(
        self,
        "Open WAV File",
        "",
        "Wave Files (*.wav)"
    )

        if self.filename:
            self.data, self.samplerate, self.info = load_audio(self.filename)
            self.waveform.set_audio(
                self.data,
                self.samplerate,
                self.info
                )

            self.file_label.setText(f"File: {os.path.basename(self.filename)}")
            self.sample_rate_label.setText(f"Sample Rate: {self.info.samplerate} Hz")
            self.length_label.setText(f"Length: {self.info.duration:.2f} seconds")
            self.channels_label.setText(f"Channels: {self.info.channels}")

    def export_slices(self):

        if self.waveform.data is None:
            return

        folder = QFileDialog.getExistingDirectory(
            
        self,
        "Select Export Folder"
    )

        if folder:

            self.exporter.export_slices(
            self.waveform.data,
            self.waveform.samplerate,
            self.waveform.slicer.sample_slices,
            folder
        )


            

















