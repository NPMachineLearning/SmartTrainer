from abc import ABC, abstractmethod
from enum import Enum
import math
import numpy as np
import os
import json
from .low_pass_filter import LPFilter

class KpsMetrics(ABC):
    def __init__(self, low_pass_filter=True, low_pass_filter_alpha=0.4, config_path=None):
        """
        Create a keypoints metric object
        
        Args:
            low_pass_filter (bool, optional): True using low pass filter to filter out 
            high frequency singal result in a smooth singal. Range (0.0, 1.0]. Defaults to True.
            low_pass_filter_alpha (float, optional): alpha value for low pass filter 1.0 to not filter
            out high frequency singal. Defaults to 0.4.
            config_path (str, optional): path to json config file contain data for exercise and used to
            count exercise reptition.
        """
        super().__init__()
        self.states = {e.name:0. for e in self.get_metric_names()}
        self.lpfs = {e.name:LPFilter() for e in self.get_metric_names()} if low_pass_filter else None
        self.low_pass_filter = low_pass_filter
        if low_pass_filter_alpha <= 0.0 or low_pass_filter_alpha > 1.0:
            raise Exception(f"low_pass_filter must in range (0.0, 1.0], greater than 0.0 and smaller and equal to 1.0")
        self.low_pass_filter_alpha = low_pass_filter_alpha
        self.config = None
        self.tracked_metrics = []
        self.reptition_count = 0
        
        # load config data if provided
        if config_path:
            if not os.path.exists(config_path):
                raise Exception(f"{config_path} doesn't exists")
            
            if os.path.isdir(config_path):
                raise Exception(f"{config_path} must be a file")
            
            with open(config_path, 'r') as f:
                    config_data = json.load(f)
                    self.config = self._load_config_data(config_data)

    @abstractmethod
    def get_metric_names(self) -> Enum:
        pass
    
    @abstractmethod
    def _load_config_data(self, config_data) -> dict:
        pass
    
    @abstractmethod
    def _process_metrics(self, kps) -> None:
        pass
    
    @abstractmethod
    def _is_a_rep(self, mean, windowed_metrics) -> bool:
        pass
    
    def update_metrics(self, kps) -> None:
        self._process_metrics(kps)
        # apply low pass filter on metrics
        if self.low_pass_filter and self.lpfs:
            if len(self.states) != len(self.lpfs):
                raise Exception(f"length of states and filter(lpfs) are not equal {len(self.states)} {len(self.lpfs)}")
            self._low_pass_filter_metrics()
        
        if self.config is not None:
            # filter out stationary metrics
            motion_names = self.config['motion_names']
            none_stationary_metrics = [[] for _ in motion_names]
            for i, name in enumerate(motion_names):
                metric = self.states[name]
                none_stationary_metrics[i].append(metric)
            none_stationary_metrics = np.array(none_stationary_metrics)
            
            # sum none stationary metrics
            sum_metric = np.sum(none_stationary_metrics, axis=0)[0]
            self.tracked_metrics.append(sum_metric)
            
            # update reptition count
            mean = self.config['reference']['mean']
            window_size = 2
            windowed_metrics = self.tracked_metrics[-window_size:]
            valid_rep = self._is_a_rep(mean, windowed_metrics)
            if valid_rep:
                self.reptition_count += 1
            
    
    def _low_pass_filter_metrics(self) -> None:
        for metric_name in list(self.states.keys()):
            # get low pass filter
            lpf = self.lpfs[metric_name]
            
            # get current metric 
            metric = self.states[metric_name]
            
            # update metric
            self.states[metric_name] = lpf.update(metric, 
                                                 self.low_pass_filter_alpha)
    
    def get_metrics(self) -> dict[str, float]:
        return self.states
    
    def get_reptition_count(self) -> int:
        return self.reptition_count
    
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
            dist = math.sqrt(abs(dxdy))
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
    
    
         
    