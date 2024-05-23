from PyQt6.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex
import cv2
import os
import numpy as np
import time

class VideoSource(QThread):
    onFrame = pyqtSignal(np.ndarray)
    onFinished = pyqtSignal()
    onInterrupted = pyqtSignal()
    
    def __init__(self, video_path, frame_per_second=30.):
        super().__init__()
        if not os.path.exists(video_path):
            raise Exception(f"video {video_path} deosn't exists")
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.fps = 1./frame_per_second
        self.paused = False
        self.cond = QWaitCondition()
        self.sync = QMutex()
        
    def pause(self):
        self.sync.lock()
        self.paused = True
        self.sync.unlock()
    
    def resume(self):
        self.sync.lock()
        self.paused = False
        self.sync.unlock()
        self.cond.wakeAll()
    
    def is_paused(self):
        return self.paused
    
    def read_frame(self, frame_index=0):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        return None        
            
    def run(self):
        try:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            while(self.cap.isOpened()):
                if self.isInterruptionRequested():
                    break
                
                self.sync.lock()
                if self.paused:
                    self.cond.wait(self.sync)
                self.sync.unlock()
                
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
            if not self.isInterruptionRequested():
                self.onFinished.emit()
            else:
                self.onInterrupted.emit()
            return
        except:
            self.cap.release()
            self.onInterrupted()
            return  
        