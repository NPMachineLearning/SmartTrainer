from PyQt6.QtCore import pyqtSignal
from rep_counting.rep_counter import RepetitionCounter
from video_source import VideoSource

import numpy as np


class VideoRepetitionCounter(VideoSource):
    onRepCount = pyqtSignal(np.ndarray, RepetitionCounter)
    
    def __init__(self, 
                 video_path:str, 
                 source_type:VideoSource.SourceType=VideoSource.SourceType.VideoFile, 
                 rep_counter:RepetitionCounter=None, 
                 frame_per_second:float=30.):
        """
        A Qt thread for capturing video and coutning repetitoin.
        
        Signals:
        - onFrame (NDArray): call when video frame is captured
        - onReadFrameFail(NDArray): call when cv2 read frame fail and provide
        a black image
        - onCompleted (): call when video source end
        - onInterrupted (): call when video is interrupted 
        
        Note:
        This class is only for capturing frame from video source not counting exercise repetition.
        Instead it use RepetitionCounter class for counting exercise repetition.

        Args:
            video_path (str): path to video source
            source_type (SourceType): type of video source either video file or camera
            frame_per_second (float, optional): frame per second for video source. Defaults to 30..
            video_capture_api (int): refer to [here](https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html)

        Raises:
            Exception: updating repetiton counter
        """
        super().__init__(video_path=video_path, 
                         source_type=source_type, 
                         frame_per_second=frame_per_second)
        self.rep_counter = rep_counter
    
    def _process_frame(self, frame: np.ndarray) -> None:
        if self.rep_counter is not None:
            self.sync.lock()
            self.rep_counter.update_metric(frame)
            self.sync.unlock()
            self.onRepCount.emit(frame, self.rep_counter)              
        