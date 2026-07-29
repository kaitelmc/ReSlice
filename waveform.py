from PySide6.QtWidgets import (
    QWidget, QSizePolicy 
)

from PySide6.QtGui import(
    QPainter,
    QPen
)

from slicer import Slicer

import sounddevice as sd

class WaveformWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(200)
        self.setMaximumHeight(600)

        self.setSizePolicy(
        QSizePolicy.Expanding,
        QSizePolicy.Expanding
)
        self.data = None
        self.samplerate = None
        self.info = None
        self.number_of_slices = 4

        self.slicer = Slicer()

    def set_audio(self, data, samplerate, info):
        self.data = data
        self.samplerate = samplerate
        self.info = info

        self.slicer.number_of_slices = self.number_of_slices
        self.slicer.create_slices(self.width())
        self.slicer.create_sample_slices(
        self.width(),
        len(self.data)
    )

        self.update()

    def set_slice_count(self, slice_count_value):
        self.number_of_slices = slice_count_value
        self.slicer.number_of_slices = slice_count_value

        self.slicer.create_slices(self.width())

        if self.data is not None:
            self.slicer.create_sample_slices(
                self.width(),
                len(self.data)
                )
        self.update()

    def preview_slice(self, index):

        current_slice = self.slicer.sample_slices[index]

        start = current_slice[0]
        end = current_slice[1]

        slice_audio = self.data[start:end]

        sd.play(slice_audio, self.samplerate)

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.data is None:
            return
        
        #convert stereo to mono for display
        samples = (self.data[:, 0] + self.data[:, 1]) / 2

        peak = max(abs(samples))
        if peak > 0:
            samples = samples / peak

        width = self.width()
        height = self.height()

        centre = height // 2

        #waveform pen
        wave_pen = QPen()
        painter.setPen(wave_pen)
        samples_per_pixel = max(1, len(samples) // width)

        points = []

        for x in range(width):
            start = x * samples_per_pixel
            end = start + samples_per_pixel
            section = samples[start:end]

            if len(section) > 0:
                high = max(section)
                low = min(section)

                y_high = centre - int(high * centre)
                y_low = centre - int(low * centre)
                

                points.append((x, y_high, y_low))

        for point in points:
            painter.drawLine(
                point[0],
                point[1],
                point[0],
                point[2]
        )
            
        #draw centre line
        centre_pen=QPen()
        centre_pen.setColor("gray")
        painter.setPen(centre_pen)

        painter.drawLine(
            0,
            centre,
            width,
            centre
        )

        #draw slice markers
        for slice in self.slicer.visual_slices:
            x = slice[1]
            slice_pen=QPen()
            slice_pen.setColor("red")
            painter.setPen(slice_pen)

            painter.drawLine(
                 x,
                 0,  
                 x,
                 height
        )