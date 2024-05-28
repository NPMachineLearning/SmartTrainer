from PyQt6.QtCore import pyqtSignal
from rep_counting.rep_counter import RepetitionCounter
from video_source import VideoSource

import numpy as np


class VideoRepetitionCounter(VideoSource):
    onRepCount = pyqtSignal(np.ndarray, RepetitionCounter)
    
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
            Exception: updating repetiton counter
        """
        super().__init__(video_path, frame_per_second)
        self.rep_counter = rep_counter
    
    def _process_frame(self, frame: np.ndarray) -> None:
        self.sync.lock()
        self.rep_counter.update_metric(frame)
        self.sync.unlock()
        self.onRepCount.emit(frame, self.rep_counter)              
        