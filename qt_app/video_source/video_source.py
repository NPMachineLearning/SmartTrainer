import cv2
import os
import numpy as np
import time
import warnings
import platform

from PySide2.QtCore import QThread, Signal, QWaitCondition, QMutex
if platform.system() == "Linux":
    from linuxpy.video.device import Device, BufferType
from enum import Enum

class VideoSource(QThread):
    onPrepare = Signal()
    onReady = Signal(object)
    onFrame = Signal(np.ndarray)
    onCompleted = Signal()
    onInterrupted = Signal()
    onVideoSourceFail = Signal()
    
    SourceType = Enum("VideoSourceType", ["VideoFile", "Camera"])
    
    def __init__(self, 
                 video_path:str, 
                 source_type:SourceType=SourceType.VideoFile, 
                 frame_per_second:float=30., 
                 video_capture_api:int=cv2.CAP_ANY,
                 pause_at_start:bool=False):
        """
        A Qt thread for capturing video. Support for video clip and camera.
        
        OpenCV is used for reading frame from video clip file. Camera source
        is depend on OS system, Linux system will use V4L2 libraries for
        capturing camera streaming frame, other platform will use OpenCV
        for camera streaming frame.
        
        Subclass can override method _process_frame(frame) to
        do extra work on video frame
        
        Signals:
        - onPrepare (): call when preparing video source
        - onReady (NDArray|None): call when preparing video source ready before entering the frame loop.
        If it is video clip a preview frame is given otherwise None if it is camera.
        - onFrame (NDArray): call when video frame is captured
        a black image
        - onCompleted (): call when video source end
        - onInterrupted (): call when video is interrupted 

        Args:
            - video_path (str): path to video file source or camera device port number
            - source_type (SourceType): type of video source either video file or camera
            - frame_per_second (float, optional): frame per second for video source. Defaults to 30..
            - video_capture_api (int, optional): cv2 VideoCapture api 
            refer to [here](https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html)
            - pause_at_start (bool, optional): pause video source when thread started. Default to False.
            When you need to manually start video source set this to True. Use methods resume() and 
            pause() to start or pause video source.

        Raises:
            Exception: path to video clip file doesn't exists
            Exception: source type unknown
        """
        super().__init__()
        self.source_type = source_type
        self.cv_video_capture_api = video_capture_api
        
        if self.source_type.value == self.SourceType.VideoFile.value:
            if not os.path.exists(video_path):
                raise Exception(f"video {video_path} doesn't exists")
            self.video_path = video_path
        elif self.source_type.value == self.SourceType.Camera.value:
            self.video_path = video_path
        else:
            raise Exception(f"Unknow source type {self.source_type}")
          
        self.fps = 1./frame_per_second 
        self.paused = pause_at_start
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
    
    def read_frame(self, video_clip:cv2.VideoCapture, frame_index=0) -> np.ndarray:
        """
        Get a particular frame from video clip
        
        This is only avaliable when source type is video file
        
        Args:
            frame_index (int, optional): index of frame. Defaults to 0.

        Returns:
            NDArray|None: frame in Numpy array or None can't read frame
        """
        if self.source_type.value == self.SourceType.VideoFile.value:
            video_clip.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = video_clip.read()
            
            # reset frame position to 0
            video_clip.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
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
        if self.source_type.value == self.SourceType.VideoFile.value:
            self.start_video_clip_loop(self.video_path, self.cv_video_capture_api)
        elif self.source_type.value == self.SourceType.Camera.value:
            if platform.system() == 'Linux':
                self.start_camera_capture_loop_v4l2(int(self.video_path))
            else:
                self.start_camera_capture_loop_cv(int(self.video_path))

    def start_video_clip_loop(self, video_path:str, video_capture_api:int=cv2.CAP_ANY):
        """
        For all OS system
        
        Main thread loop for capturing video clip frame 
        """
        try:
            self.onPrepare.emit()
            
            # create video capture for video clip
            # as we allow to read frame from video clip
            self.video_clip_cap = cv2.VideoCapture(video_path, video_capture_api)
            cc = self.video_clip_cap.get(cv2.CAP_PROP_FOURCC)
            self.video_clip_cap.set(cv2.CAP_PROP_FOURCC, cc)
            
            if not self.video_clip_cap.isOpened():
                warnings.warn(f"Video source:{self.video_path}, Type:{self.source_type.name} can't be opend")
            
            # set frame per seconds
            video_fps = self.video_clip_cap.get(cv2.CAP_PROP_FPS)
            self.fps = 1. / video_fps
            
            first_frame = self.read_frame(self.video_clip_cap)
            
            # set frame position at beginning
            self.video_clip_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                
            self.onReady.emit(first_frame)
            
            self.cv_video_capture_loop(self.video_clip_cap)
        except Exception as e:
            print(e)
            self.onVideoSourceFail.emit()
        finally:
            self.video_clip_cap.release()

    def start_camera_capture_loop_cv(self, camera_device_port:int):
        """_summary_
        
        Main thread loop for streaming camera frame
        
        For other OS system than Linux

        Args:
            camera_device_port (int): port number of camera device
        """
        try:
            self.onPrepare.emit()
            
            self.cam = cv2.VideoCapture(camera_device_port, self.cv_video_capture_api)
            
            if not self.cam.isOpened():
                warnings.warn(f"Camera device port:{self.video_path}, Type:{self.source_type.name} can't be opend")
            
            self.onReady.emit(None)
            
            self.cv_video_capture_loop(self.cam)
        except Exception as e:
            print(e)
            self.onVideoSourceFail.emit()
        finally:
            self.cam.release()            
    
    def start_camera_capture_loop_v4l2(self, camera_device_port:int):
        """
        Main thread loop for streaming camera frame
        
        For Linux system with V4L2
        
        [Libraries for capturing video](https://github.com/tiagocoutinho/linuxpy)
        
        Args:
            camera_device_port (int): port number of camera device
        """
        try:
            self.onPrepare.emit()
            
            self.cam = Device.from_id(camera_device_port)
            self.cam.open()
            fmt = self.cam.get_format(BufferType.VIDEO_CAPTURE)
            self.cam.set_format(BufferType.VIDEO_CAPTURE, fmt.width, fmt.height ,'MJPG')
            
            self.onReady.emit(None)
            
            for frame in self.cam:
                # if paused
                self.sync.lock()
                if self.paused:
                    self.cond.wait(self.sync)
                self.sync.unlock()
                
                # if interrupted
                if self.isInterruptionRequested():
                    break
                
                now = time.time()
                
                frame = cv2.imdecode(frame.array, cv2.IMREAD_COLOR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.onFrame.emit(frame)
                
                # process frame
                self._process_frame(frame)
                
                # wait until next frame
                time_diff = time.time() - now
                if time_diff < self.fps:
                    time.sleep(self.fps - time_diff)
            
            if self.isInterruptionRequested():
                self.onInterrupted.emit()
            else:
                self.onCompleted.emit()     
        except Exception as e:
            print(e)
            self.onVideoSourceFail.emit()
        finally:
            self.cam.close()

    def cv_video_capture_loop(self, video_cap:cv2.VideoCapture):
        """
        For video file:
        Take OpenCV VideoCapture object and run in loop to get each frame
        until video file end or interrupted
        
        For camera:
        Take OpenCV VideoCapture object and run in loop to get stream frame
        until stream interrupted or close

        Args:
            video_cap (cv2.VideoCapture): cv2 VideoCapture
        """
        while(True):
            # if paused
            self.sync.lock()
            if self.paused:
                self.cond.wait(self.sync)
            self.sync.unlock()
            
            # if interrupted
            if self.isInterruptionRequested():
                break
            
            now = time.time()
            
            # get a frame
            ret, frame = video_cap.read()
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
                break
        
        if self.isInterruptionRequested():
            self.onInterrupted.emit()
        else:
            self.onCompleted.emit()    
        