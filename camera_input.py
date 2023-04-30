import folium
import cv2
from PyQt5 import QtWebEngineWidgets
import io
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

"""
To be implemented.
"""

class realTimeVideo(QObject):

    finished = pyqtSignal()

    def __init__(self, ui):
        super(realTimeVideo, self).__init__()
        self.ui = ui

    def run(self):
        WIDTH,HEIGHT=651,701

        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret == True:
                frame = cv2.flip(frame, 180)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (WIDTH, HEIGHT))

                image = QImage(
                    frame,
                    frame.shape[1],
                    frame.shape[0],
                    frame.strides[0],
                    QImage.Format_RGB888,
                )
                self.ui.setPixmap(QPixmap.fromImage(image))
            else:
                break
            cv2.destroyAllWindows()


class CameraI:
    def __init__(self, ui) -> None:
        self.ui = ui

        # Live Camera Version 
        # https://stackoverflow.com/questions/72265287/pyqt5-i-want-to-show-camera-view-to-label
        # https://realpython.com/python-pyqt-qthread/
        self.thread = QThread()
        self.realTimeVideo = realTimeVideo(self.ui.MainCamera)
        self.realTimeVideo.moveToThread(self.thread)
        self.thread.started.connect(self.realTimeVideo.run)
        self.realTimeVideo.finished.connect(self.thread.quit)
        self.realTimeVideo.finished.connect(self.realTimeVideo.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

        # Gif version
        """
        self.ui.movie = QMovie("/home/rhip/Downloads/test.gif")
        self.ui.MainCamera.setMovie(self.ui.movie)
        self.ui.movie.start()
        """

        self.ui.movie2 = QMovie(
            "/home/rhip/ros2_ws/src/metu_gui_v2/assets/ezgif.com-gif-maker (1).gif"
        )
        self.ui.EndEffectorCamera.setMovie(self.ui.movie2)
        self.ui.movie2.start()

        self.ui.movie3 = QMovie(
            "/home/rhip/ros2_ws/src/metu_gui_v2/assets/ezgif.com-gif-maker (2).gif"
        )
        self.ui.ScienceHubCamera.setMovie(self.ui.movie3)
        self.ui.movie3.start()

        self.ui.movie4 = QMovie(
            "/home/yoy/Desktop/metu_rover/src/metu_gui_v2/assets/ezgif.com-gif-maker (4).gif"
        )
        self.ui.BatteryShow.setMovie(self.ui.movie4)
        self.ui.movie4.start()

        m = folium.Map(
            location=[39.889011, 32.7801363], tiles="Stamen Toner", zoom_start=13
        )
        data = io.BytesIO()
        m.save(data, close_file=False)

        w = QtWebEngineWidgets.QWebEngineView()
        w.setHtml(data.getvalue().decode())
        self.ui.GPSMapLayout.addWidget(w)
