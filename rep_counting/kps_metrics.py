from abc import ABC, abstractmethod
import math
import numpy as np

class KpsMetrics(ABC):
    def __init__(self):
        super().__init__()
        self.state = {metric_name:0 for metric_name in self.get_metric_names()}
    
    @abstractmethod
    def get_metric_names(self):
        pass
    
    @abstractmethod
    def update_metrics(self, kps):
        pass
    
    def get_metrics(self):
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
    
    
         
    