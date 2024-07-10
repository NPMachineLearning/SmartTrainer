from abc import ABC, abstractmethod
from enum import Enum
import math
import numpy as np
import os
import warnings
import json
from .low_pass_filter import LPFilter

class KpsMetrics(ABC):
    def __init__(self, low_pass_filter=True, low_pass_filter_alpha=0.4, config_path=None):
        """
        Create a keypoints metric object
        
        Args:
            - low_pass_filter (bool, optional): True using low pass filter to filter out 
            high frequency singal result in a smooth singal. Range (0.0, 1.0]. Defaults to True.
            - low_pass_filter_alpha (float, optional): alpha value for low pass filter 1.0 to not filter
            out high frequency singal. Defaults to 0.4.
            - config_path (str, optional): path to json config file contain data for exercise and used to
            count exercise reptition.
        """
        super().__init__()
        # state of metrics and their name
        self.states = {e.name:0. for e in self.get_metric_names()}
        
        # create low pass filter for
        # each metric
        self.lpfs = {e.name:LPFilter() for e in self.get_metric_names()} if low_pass_filter else None
        
        # low pass filter
        self.low_pass_filter = low_pass_filter
        
        # make sure low pass filter is in range
        if low_pass_filter_alpha <= 0.0 or low_pass_filter_alpha > 1.0:
            raise Exception(f"low_pass_filter must in range (0.0, 1.0], greater than 0.0 and smaller and equal to 1.0")
        
        # alpha value for low pass filter
        self.low_pass_filter_alpha = low_pass_filter_alpha
        
        # config data from json for the exercise
        self.config = None
        
        # a list of sum of metrics
        self.tracked_metrics = []
        
        # a list of tracked pattern
        # converted from sum of metrics 
        self.tracked_pattern = []
        
        # pattern to be matched
        self.query_pattern = None
        self.query_pattern = np.array(self._get_query_pattern())
        
        # check if query pattern contain none 0 and 1 value
        none_binary_found = ((self.query_pattern!=0) & (self.query_pattern!=1)).any()
        if none_binary_found:
            raise Exception(f"values of query pattern list can only be 1 or 0. but given {self.query_pattern}")
        
        # total repetition count performed
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
        else:
            warnings.warn("No config file given, metric will not do repetition counting")

    @abstractmethod
    def get_metric_names(self) -> Enum:
        """
        Get all metric names

        Returns:
            Enum: metric names
        """
        pass
    
    @abstractmethod
    def get_exercise_name(self) -> str:
        """
        Get exercise name

        Returns:
            str: name of this exercise
        """
        pass
    
    @abstractmethod
    def _process_metrics(self, kps, states, ratio) -> None:
        """
        Processing keypoints into metrics

        Args:
            - kps (NDArray): all keypoints
            - states (dict): where all metrics to be stored
        """
        pass
    
    @abstractmethod
    def _get_query_pattern(self) -> list[int]:
        """
        Pattern to be used for exercise repetition counting

        Returns:
            list: a sequence of 0 or 1 e.g [0, 1, 1, 0] where
            0 is below mean and 1 above mean
            - 0: normal state
            - 1: exercise motion state
        """
        pass
    
    def update_metrics(self, kps, ratio=(1., 1.), confidence_rate=1.0, confidence_rate_threshold=0.5) -> None:
        """
        Main process to update metrics and do 
        exercise prepetition counting

        Args:
            - kps (dict): all keypoints from movenet
            - ratio (tuple, optional): scale for x and y 
            only for calculate distance on keypoints
            - confidence_rate (float): if this value is equal and greater
            than confidence_rate_threshold, final metric will be updated,
            otherwise it keep as same as last metric. Value between 0.0 ~ 1.0.
            - confidence_rate_threshold (float): if confidence rate equal and greater
            than this value, final metric will be updated. Value between 0.0 ~ 1.0. 

        Raises:
            Exception: low pass filter fail
        """
        confidence_rate = max(min(confidence_rate, 1.0), 0.0)
        confidence_rate_threshold = max(min(confidence_rate_threshold, 1.0), 0.0)
        
        ###
        # process keypoints into metrics
        self._process_metrics(kps, self.states, ratio)
        
        ###
        # apply low pass filter on metrics
        if self.low_pass_filter and self.lpfs:
            if len(self.states) != len(self.lpfs):
                raise Exception(f"length of states and filter(lpfs) are not equal {len(self.states)} {len(self.lpfs)}")
            self._low_pass_filter_metrics()
        
        ### 
        # repetition counting
        # step 1. remove all stationary metrics specific to exercise
        # step 2. add all none stationary metrics together
        # step 3. find number of repetition
        if self.config is not None:
            ###
            # filter out stationary metrics
            
            # get all none stationary exercise names from config
            motion_names = self.config['motion_names']
            none_stationary_metrics = [[] for _ in motion_names]
            for i, name in enumerate(motion_names):
                metric = self.states[name]
                none_stationary_metrics[i].append(metric)
            none_stationary_metrics = np.array(none_stationary_metrics)
            
            ###
            # sum none stationary metrics
            if len(self.tracked_metrics) > 0:
                if confidence_rate >= confidence_rate_threshold:
                    sum_metric = np.sum(none_stationary_metrics, axis=0)[0]
                else:
                    sum_metric = self.tracked_metrics[-1]
            else:
                sum_metric = np.sum(none_stationary_metrics, axis=0)[0]
            self.tracked_metrics.append(sum_metric)
            
            ### 
            # update reptition count
            
            # get mean from config
            mean = self.config['reference']['mean']
            
            # convert sum metric into pattern either 1 or 0
            # mean as threshold
            # pattern value only added when last value from 
            # tracked pattern list is different to the pattern value
            #
            # example:
            # if mean=5.0 signals=[1.0, 2.0, 10.0, 6.0, 3.0]
            # output pattern=[0, 1, 0] 
            if sum_metric < mean:
                if len(self.tracked_pattern) > 0:
                    # only add 0 if last value in pattern
                    # is different than 0
                    if self.tracked_pattern[-1] != 0:
                        self.tracked_pattern.append(0)
                else:
                    self.tracked_pattern.append(0)
                    
            else:
                if len(self.tracked_pattern) > 0:
                    # only add 1 if last value in pattern
                    # is different than 1
                    if self.tracked_pattern[-1] != 1:
                        self.tracked_pattern.append(1)
                else:
                    self.tracked_pattern.append(1)
            
            # length of query pattern
            len_q_pattern = len(self.query_pattern)
            
            # length of tracked pattern
            len_t_pattern = len(self.tracked_pattern)
                    
            if len_t_pattern >= len_q_pattern:
                rep = 0
                
                # find number of query pattern match
                for i in range(len_t_pattern - len_q_pattern + 1):
                    # get subset of tracked pattern
                    t_pattern = np.array(self.tracked_pattern[i:i+len_q_pattern])
                    
                    # pattern match only if sum of difference between
                    # tracked pattern and query pattern is 0
                    # 
                    # example:
                    # substraction pattern 1 and pattern 2 = [1,0,1] - [1,0,1] = [0,0,0]
                    # sum [0,0,0] = 0
                    # substraction pattern 1 and pattern 2 = [1,1,0] - [1,0,1] = [0,1,-1]
                    # absolute [0,1,-1] = [0,1,1]
                    # sum [0,1,1] = 1  
                    if np.absolute(t_pattern - self.query_pattern).sum() == 0:
                       rep += 1
                       
                # update repetition count
                self.reptition_count = rep 
    
    def _load_config_data(self, config_data) -> dict:
        """
        Load config data  

        Args:
            - config_data (dict): config data from json file for exercises

        Returns:
            dict: config data for sepcific exercise
        """
        exercise_name = self.get_exercise_name()
        data = config_data.get(exercise_name, None)
        if data is None:
            raise Exception(f"{exercise_name} was not found in config file")
        return data
                        
    def _low_pass_filter_metrics(self) -> None:
        """
        Low pass filter to smooth signals(metrics)
        """
        for metric_name in list(self.states.keys()):
            # get low pass filter
            lpf = self.lpfs[metric_name]
            
            # get current metric 
            metric = self.states[metric_name]
            
            # update metric
            self.states[metric_name] = lpf.update(metric, 
                                                 self.low_pass_filter_alpha)
    
    def get_metrics(self) -> dict[str, float]:
        """
        Get current metrics

        Returns:
            dict[str, float]: metric name and value pair dictionary
        """
        return self.states
    
    def get_reptition_count(self) -> int:
        """
        Get current total exercise reptition count

        Returns:
            int: repetition count
        """
        return self.reptition_count
    
    @staticmethod
    def distance(kpi1:int, kpi2:int, kps, on_axis='xy', ratio=None):
        """
        Calculate distance between two keypoints
        
        Args:
            - kpi1 (int): index of keypoint 1
            - kpi2 (int): index of keypoint 2
            - kps (dict): all keypoints
            - on_axis (str, optional): which axis to calculate on. Defaults to 'xy'.
            - ratio (tuple, optional): (x_ratio, y_ratio). Defaults to None. If None
            ratio is (1, 1)

        Raises:
            Exception: when on_axis is not one of x, y, xy

        Returns:
            float: distance
        """
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
        """
        Calculate angle(degree) between 3 keypoints
        hence angle between vector -> kpi21 and vector
        -> kpi23

        Args:
            - kpi1 (int): index of keypoints 1
            - kpi2 (int): index of keypoints 2
            - kpi3 (int): index of keypoints 3
            - kps (dict): all keypoints

        Returns:
            angle(degree): angle between kpi21 and kpi23
        """
        # keypoints for kp1 ~ kp3
        kp1 = (kps[kpi1][0], kps[kpi1][1])
        kp2 = (kps[kpi2][0], kps[kpi2][1])
        kp3 = (kps[kpi3][0], kps[kpi3][1])
        
        # vectors for kp21, kp23
        kp21 = [kp1[0]-kp2[0], kp1[1]-kp2[1]]
        kp23 = [kp3[0]-kp2[0], kp3[1]-kp2[1]]
        
        # magnitude for kp21, kp23
        mag_kp21 = math.sqrt(kp21[0]**2 + kp21[1]**2)
        mag_kp23 = math.sqrt(kp23[0]**2 + kp23[1]**2)
        
        # calculate angle in degree
        theta = np.dot(kp21, kp23) / (abs(mag_kp21) * abs(mag_kp23))
        
        # preven theta out of 1 and -1 range
        # otherwise acos will throw error
        theta = min(1, max(theta, -1))
        angle_degree = math.degrees(math.acos(theta))
        
        return angle_degree
    
    
         
    