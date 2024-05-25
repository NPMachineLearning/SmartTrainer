from PyQt6.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex
from rep_counting.rep_counter import RepetitionCounter

import cv2
import os
import numpy as np
import time

class VideoRepetitionCounter(QThread):
    onRepCount = pyqtSignal(np.ndarray, RepetitionCounter)
    onCompleted = pyqtSignal()
    onInterrupted = pyqtSignal()
    
    def __init__(self, video_path:str, rep_counter:RepetitionCounter, frame_per_second:float=30.):
        """
        A Qt thread for capturing video and coutning repetitoin.
        
        Signals:
        - onRepCount (frame (NDArray), RepetitionCounter): called when a frame is processed and 
        repetiton counter is updated
        - onCompleted (): called when video source end
        - onInterrupted (): call when video is interrupted 
        
        Note:
        This class is only for capturing frame from video source not counting exercise repetition.
        Instead it use RepetitionCounter class for counting exercise repetition.

        Args:
            video_path (str): path to video source
            rep_counter (RepetitionCounter): the object of RepetitionCounter
            frame_per_second (float, optional): frame per second for video source. Defaults to 30..

        Raises:
            Exception: when capturing frame from video source or updating repetiton counter
        """
        super().__init__()
        if not os.path.exists(video_path):
            raise Exception(f"video {video_path} deosn't exists")
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.fps = 1./frame_per_second
        self.paused = False
        self.cond = QWaitCondition()
        self.sync = QMutex()
        self.rep_counter = rep_counter
        
    def pause(self) -> None:
        """
        Pause video source
        """
        self.sync.lock()
        self.paused = True
        self.sync.unlock()
    
    def resume(self) -> None:
        """
        Resume video source
        """
        self.sync.lock()
        self.paused = False
        self.sync.unlock()
        self.cond.wakeAll()
    
    def is_paused(self) -> bool:
        """
        Video source state either in pause or playing
        
        Returns:
            bool: if True video paused otherwise False
        """
        return self.paused
    
    def read_frame(self, frame_index=0) -> np.ndarray|None:
        """
        Get a particular frame from video source
        
        Args:
            frame_index (int, optional): index of frame. Defaults to 0.

        Returns:
            NDArray|None: frame in Numpy array or None can't read frame
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        return None        
            
    def run(self):
        ##
        # Thread main loop
        try:
            # set frame position at beginning
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            while(self.cap.isOpened()):
                # if interrupted
                if self.isInterruptionRequested():
                    break
                
                # if paused
                self.sync.lock()
                if self.paused:
                    self.cond.wait(self.sync)
                self.sync.unlock()
                
                now = time.time()
                
                # get a frame
                ret, frame = self.cap.read()
                if ret:
                    # convert bgr to rgb
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # update metric
                    self.sync.lock()
                    self.rep_counter.update_metric(frame)
                    self.sync.unlock()
                    self.onRepCount.emit(frame, self.rep_counter)
                    
                    # wait until next frame
                    time_diff = time.time() - now
                    if time_diff < self.fps:
                        time.sleep(self.fps - time_diff)
                else:
                    break
                
            if self.isInterruptionRequested():
                self.onInterrupted.emit()
            else:
                self.onCompleted.emit()
        except:
            self.onInterrupted()
        finally:
            self.cap.release()  
        