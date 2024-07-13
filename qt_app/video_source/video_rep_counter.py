from PySide2.QtCore import Signal
from rep_counting.rep_counter import RepetitionCounter
from .video_source import VideoSource

import numpy as np


class VideoRepetitionCounter(VideoSource):
    onRepCount = Signal(np.ndarray, RepetitionCounter)
    
    def __init__(self, 
                 video_path:str, 
                 source_type:VideoSource.SourceType=VideoSource.SourceType.VideoFile, 
                 rep_counter:RepetitionCounter=None, 
                 frame_per_second:float=30.,
                 pause_at_start:bool=False,
                 draw_skeleton:bool=False):
        """
        A Qt thread for capturing video and coutning repetitoin.
        
        This class is a subclass of VideoSource.
        
        Note:
        This class is only for capturing frame from video source not counting exercise repetition.
        Instead it use RepetitionCounter class for counting exercise repetition.
        
        Signals:
        - onPrepare (): call when preparing video source
        - onReady (NDArray|None): call when preparing video source ready before entering the frame loop.
        If it is video clip a preview frame is given otherwise None if it is camera.
        - onFrame (NDArray): call when video frame is captured
        a black image
        - onCompleted (): call when video source end
        - onInterrupted (): call when video is interrupted 
        - onRepCount (NDArray, RepetitionCounter): call when repetition counter updated

        Args:
            - video_path (str): path to video file source or camera device port number.
            - source_type (SourceType): type of video source either video file or camera.
            - rep_counter (RepetitionCounter): RepetitionCounter object for counting repetition.
            - frame_per_second (float, optional): frame per second for video source. Defaults to 30..
            - pause_at_start (bool, optional): pause video source when thread started. Default to False.
            When you need to manually start video source set this to True. Use methods resume() and 
            pause() to start or pause video source.
            - draw_skeleton (bool, optional): whether to draw skeleton or not. Default to False.
            Enable drawing skeleton could decrease performance.

        Raises:
            Exception: updating repetiton counter went wrong
        """
        super().__init__(video_path=video_path, 
                         source_type=source_type, 
                         frame_per_second=frame_per_second,
                         pause_at_start=pause_at_start)
        self.rep_counter = rep_counter
        self.draw_skeleton = draw_skeleton
    
    def set_draw_skeleton(self, value:bool) -> None:
        self.sync.lock()
        self.draw_skeleton = value
        self.sync.unlock()
        
    def _process_frame(self, frame: np.ndarray) -> None:
        if self.isInterruptionRequested():
            return
        
        self.sync.lock()
        if self.rep_counter is not None:
            kps_norm = self.rep_counter.update_metric(frame)
            if self.draw_skeleton:
                frame = self.rep_counter.draw_kps_skeleton(frame, kps_norm, 5)
            self.onRepCount.emit(frame, self.rep_counter)
        self.sync.unlock()              
        