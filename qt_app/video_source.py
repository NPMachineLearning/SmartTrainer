from PyQt6.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex

import cv2
import os
import numpy as np
import time
import warnings
from enum import Enum

class VideoSource(QThread):
    onFrame = pyqtSignal(np.ndarray)
    onReadFrameFail = pyqtSignal(np.ndarray)
    onCompleted = pyqtSignal()
    onInterrupted = pyqtSignal()
    
    SourceType = Enum("VideoSourceType", ["VideoFile", "Camera"])
    
    def __init__(self, 
                 video_path:str, 
                 source_type:SourceType=SourceType.VideoFile, 
                 frame_per_second:float=30., 
                 video_capture_api:int=cv2.CAP_ANY):
        """
        A Qt thread for capturing video.
        
        Signals:
        - onFrame (NDArray): call when video frame is captured
        - onReadFrameFail(NDArray): call when cv2 read frame fail and provide
        a black image
        - onCompleted (): call when video source end
        - onInterrupted (): call when video is interrupted 

        Args:
            video_path (str): path to video source
            source_type (SourceType): type of video source either video file or camera
            frame_per_second (float, optional): frame per second for video source. Defaults to 30..
            video_capture_api (int): refer to [here](https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html)

        Raises:
            Exception: when capturing frame from video source
        """
        super().__init__()
        self.source_type = source_type
        
        try:
            if self.source_type.value == self.SourceType.VideoFile.value:
                if not os.path.exists(video_path):
                    raise Exception(f"video {video_path} deosn't exists")
                self.video_path = video_path
            elif self.source_type.value == self.SourceType.Camera.value:
                self.video_path = int(video_path)
            else:
                raise Exception(f"Unknow source type {self.source_type}")
            
            self.cap = cv2.VideoCapture(self.video_path, video_capture_api)
            cc = self.cap.get(cv2.CAP_PROP_FOURCC)
            self.cap.set(cv2.CAP_PROP_FOURCC, cc)
        except Exception as e:
            raise e
            
        self.fps = 1./frame_per_second
        self.paused = False
        self.cond = QWaitCondition()
        self.sync = QMutex()
        
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
    
    def _process_frame(self, frame:np.ndarray) -> None:
        """
        Subclass should implement this method for processing frame

        Args:
            frame (NDArray): captured frame from video
        """
        pass        
            
    def run(self):
        ##
        # Thread main loop
        try:
            # set frame position at beginning
            if self.source_type.value == self.SourceType.VideoFile.value:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            if not self.cap.isOpened():
                warnings.warn(f"Video source:{self.video_path}, Type:{self.source_type.name} can't be opend")
                
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
                    self.onFrame.emit(frame)
                    
                    # process frame
                    self._process_frame(frame)
                    
                    # wait until next frame
                    time_diff = time.time() - now
                    if time_diff < self.fps:
                        time.sleep(self.fps - time_diff)
                else:
                    self.onReadFrameFail.emit(np.zeros((600,800,3)))

            if self.isInterruptionRequested():
                self.onInterrupted.emit()
            else:
                self.onCompleted.emit()
        except Exception as e:
            self.onInterrupted()
            raise e
        finally:
            self.cap.release()  
        