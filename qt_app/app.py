import sys
import os
from PyQt6.QtGui import QCloseEvent, QImage, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from main_window import Ui_MainWindow
from video_source import VideoSource

class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.action_open_video.triggered.connect(self.open_video)
        self.video_path = None
        self.video_source = None
    
    def open_video(self):
        vid_path, _ = QFileDialog.getOpenFileName(self,
                                               "Open video",
                                               filter="Video file (*.mp4)")
        if os.path.exists(vid_path):
            self.video_path = vid_path
            self.video_source = VideoSource(self.video_path,
                                            30.)
            self.video_source.onFrame.connect(self.on_frame)
            self.video_source.onFinished.connect(self.on_video_finished)
            self.video_source.finished.connect(self.video_source.deleteLater)
            self.video_source.start()
            
    def on_frame(self, frame):
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
        self.img_frame.setPixmap(QPixmap.fromImage(image))
    
    def on_video_finished(self):
        self.video_source = None
        self.img_frame.setText("video frame")
        
    def resizeEvent(self, _):
        pass
                    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # todo: do extra stuff here before app exit
        a0.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())        