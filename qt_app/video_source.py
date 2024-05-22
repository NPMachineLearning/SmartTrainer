from PyQt6.QtCore import QThread, pyqtSignal
import cv2
import os
import numpy as np
import time

class VideoSource(QThread):
    onFrame = pyqtSignal(np.ndarray)
    onFinished = pyqtSignal()
    
    def __init__(self, video_path, frame_per_second=30.):
        super().__init__()
        if not os.path.exists(video_path):
            raise Exception(f"video {video_path} deosn't exists")
        self.video_path = video_path
        self.cap = None
        self.exit = False
        self.fps = 1./frame_per_second
    
    def stop(self):
        self.exit = True
        
    def run(self):
        self.cap = cv2.VideoCapture(self.video_path)
        while(self.cap.isOpened() and not self.exit):
            now = time.time()
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.onFrame.emit(frame)
                time_diff = time.time() - now
                if time_diff < self.fps:
                    time.sleep(self.fps - time_diff)
            else:
                break
        self.cap.release()
        self.onFinished.emit()       
        