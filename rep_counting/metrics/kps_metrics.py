from abc import ABC, abstractmethod
from enum import Enum
import math
import numpy as np
from filter.low_pass_filter import LPFilter

class KpsMetrics(ABC):
    def __init__(self, low_pass_filter=True, low_pass_filter_alpha=0.4):
        """
        Create a keypoints metric object
        
        Args:
            low_pass_filter (bool, optional): True using low pass filter to filter out 
            high frequency singal result in a smooth singal. Range (0.0, 1.0]. Defaults to True.
            low_pass_filter_alpha (float, optional): alpha value for low pass filter 1.0 to not filter
            out high frequency singal. Defaults to 0.4.
        """
        super().__init__()
        self.state = {e.name:0. for e in self.get_metric_names()}
        self.lpfs = {e.name:LPFilter() for e in self.get_metric_names()} if low_pass_filter else None
        self.low_pass_filter = low_pass_filter
        if low_pass_filter_alpha <= 0.0 or low_pass_filter_alpha > 1.0:
            raise Exception(f"low_pass_filter must in range (0.0, 1.0], greater than 0.0 and smaller and equal to 1.0")
        self.low_pass_filter_alpha = low_pass_filter_alpha
    
    @abstractmethod
    def get_metric_names(self) -> Enum:
        pass
    
    def update_metrics(self, kps) -> None:
        self.process_metrics(kps)
        # apply low pass filter on metrics
        if self.low_pass_filter and self.lpfs:
            if len(self.state) != len(self.lpfs):
                raise Exception(f"length of state and filter(lpfs) are not equal {len(self.state)} {len(self.lpfs)}")
            self.filter_metrics()
    
    @abstractmethod
    def process_metrics(self, kps) -> None:
        pass
    
    def filter_metrics(self) -> None:
        for metric_name in list(self.state.keys()):
            # get low pass filter
            lpf = self.lpfs[metric_name]
            
            # get current metric 
            metric = self.state[metric_name]
            
            # update metric
            self.state[metric_name] = lpf.update(metric, 
                                                 self.low_pass_filter_alpha)
    
    def get_metrics(self) -> dict[str, float]:
        return self.state
    
    @staticmethod
    def distance(kpi1:int, kpi2:int, kps, on_axis='xy', ratio=None):
        if not ratio:
            ratio = (1, 1)
        
        on_axis = on_axis.lower()    
        dx = (kps[kpi2][0] - kps[kpi1][0]) * ratio[0]
        dy = (kps[kpi2][1] - kps[kpi1][1]) * ratio[1]
        dist = 0
        
        if on_axis == 'xy':
            dxdy = dx**2 - dy**2
            dist = math.sqrt(dxdy)
        elif on_axis == 'x':
            dist = abs(dx)
        elif on_axis == 'y':
            dist = abs(dy)
        else:
            raise Exception("on_axis must be either 'xy', 'x' or 'y'")
        
        return dist
    
    @staticmethod
    def angle(kpi1:int, kpi2:int, kpi3:int, kps):
        # keypoints for kp1 ~ kp3
        kp1 = (kps[kpi1][0], kps[kpi1][1])
        kp2 = (kps[kpi2][0], kps[kpi2][1])
        kp3 = (kps[kpi3][0], kps[kpi3][1])
        
        # vectors for kp21, kp23
        kp21 = (kp1[0]-kp2[0], kp1[1]-kp2[1])
        kp23 = (kp3[0]-kp2[0], kp3[1]-kp2[1])
        
        # magnitude for kp21, kp23
        mag_kp21 = math.sqrt(kp21[0]**2 + kp21[1]**2)
        mag_kp23 = math.sqrt(kp23[0]**2 + kp23[1]**2)
        
        # calculate angle in degree
        angle_degree = math.degrees(
            math.acos(np.dot(kp21, kp23)/(mag_kp21 * mag_kp23))
            )
        
        return angle_degree

    @staticmethod
    def normalize_kps(kps, image_width, image_height):
        for kp in kps:
            kp[0] /= image_width
            kp[1] /= image_height
            
        return kps
    
    
         
    