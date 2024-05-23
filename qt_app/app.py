import sys
import os
import time
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QImage, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from main_window import Ui_MainWindow
from video_source import VideoSource

NO_VIDEO_SOURCE_MSG = "No video source"

class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # connect slots
        self.action_open_video.triggered.connect(self.open_video)
        self.start_button.clicked.connect(self.on_start_clicked)
        self.toggle_pause_button.clicked.connect(self.on_toggle_pause)
        self.exercise_list.currentItemChanged.connect(self.on_exercise_changed)
        
        # disable buttons
        self.start_button.setEnabled(False)
        self.toggle_pause_button.setEnabled(False)
        
        # init variables
        self.img_frame.setText(NO_VIDEO_SOURCE_MSG)
        self.video_path = None
        self.video_source = None
    
    def open_video(self):
        vid_path, _ = QFileDialog.getOpenFileName(self,
                                               "Open video",
                                               filter="Video file (*.mp4)")
                
        if os.path.exists(vid_path):
            # set video path
            self.video_path = vid_path
            
            # remove current video source
            self.remove_video_source()
            
            # create new video source
            self.video_source = VideoSource(self.video_path, 30.)
            
            # render first frame
            first_frame = self.video_source.read_frame()
            if first_frame is not None:
                self.on_frame(first_frame)
            
            # connect slots    
            self.video_source.onFrame.connect(self.on_frame)
            self.video_source.onFinished.connect(self.on_video_finished)
            self.video_source.onInterrupted.connect(self.on_interrupted)
            self.video_source.finished.connect(self.video_source.deleteLater)
            
            # enable buttons
            self.start_button.setEnabled(True)
            self.toggle_pause_button.setEnabled(True)
            
    def remove_video_source(self):
        if self.video_source and self.video_source.isRunning():
            # make sure video source is in playing state
            self.video_source.resume()
            
            # tell video source to stop
            self.video_source.requestInterruption()
            
            # don't receive signal for new frame
            self.video_source.onFrame.disconnect()
            self.video_source = None
                
    def on_frame(self, frame):
        d_width = self.img_frame.size().width()-5
        d_height = self.img_frame.size().height()-5
        
        # create qt image
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
        
        # scale image
        image = image.scaled(d_width, d_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.img_frame.setPixmap(QPixmap.fromImage(image))
    
    def on_video_finished(self):
        self.video_source = None
        self.img_frame.setText(NO_VIDEO_SOURCE_MSG)
        self.start_button.setEnabled(False)
        self.toggle_pause_button.setEnabled(False)
        
    def on_interrupted(self):
        print("Video source interrupted")
        
    def on_start_clicked(self):
        if self.video_source and not self.video_source.isRunning():
            self.video_source.start()
            
    def on_toggle_pause(self):
        if self.video_source and self.video_source.isRunning():
            if self.video_source.is_paused():
                self.video_source.resume()
                self.toggle_pause_button.setText("Pause")
            else:
                self.video_source.pause()
                self.toggle_pause_button.setText("Resume")
    
    def on_exercise_changed(self, current, previous):
        self.current_exercise_label.setText(current.text())
                    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # todo: do extra stuff here before app exit
        self.remove_video_source()
        a0.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())        