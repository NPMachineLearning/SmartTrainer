from .kps_metrics import KpsMetrics
from .kps_constant import KPS_INDEX_DICT

class KpsMtricsJumpingJack(KpsMetrics):
    def __init__(self):
        super().__init__()
    
    def update_metrics(self, kps):
        self.state['shl_dist'] = self.distance(KPS_INDEX_DICT.left_shoulder.value,
                                               KPS_INDEX_DICT.right_shoulder.value,
                                               kps,
                                               'xy')
        self.state['lshl_lpalm_dist'] = self.distance(KPS_INDEX_DICT.left_shoulder.value,
                                                      KPS_INDEX_DICT.left_wrist.value,
                                                      kps,
                                                      'y')
        self.state['rshl_rPalm_dist'] = self.distance(KPS_INDEX_DICT.right_shoulder.value,
                                                      KPS_INDEX_DICT.right_wrist.value,
                                                      kps,
                                                      'y')
        self.state['lshl_rpalm_dist'] = self.distance(KPS_INDEX_DICT.left_shoulder.value,
                                                      KPS_INDEX_DICT.right_wrist.value,
                                                      kps,
                                                      'y')
        self.state['rShl_lpalm_dist'] = self.distance(KPS_INDEX_DICT.right_shoulder.value,
                                                      KPS_INDEX_DICT.left_wrist.value,
                                                      kps,
                                                      'y')
        self.state['lshl_lHip_dist'] = self.distance(KPS_INDEX_DICT.left_shoulder.value,
                                                     KPS_INDEX_DICT.left_hip.value,
                                                     kps,
                                                     'y')
        self.state['rshl_rHip_dist'] = self.distance(KPS_INDEX_DICT.right_shoulder.value,
                                                     KPS_INDEX_DICT.right_hip.value,
                                                     kps,
                                                     'y')
        self.state['lknee_lhip_dist'] = self.distance(KPS_INDEX_DICT.left_knee.value,
                                                      KPS_INDEX_DICT.left_hip.value,
                                                      kps,
                                                      'y')
        self.state['rknee_rhip_dist'] = self.distance(KPS_INDEX_DICT.right_knee.value,
                                                      KPS_INDEX_DICT.right_hip.value,
                                                      kps,
                                                      'y')
        self.state['lknee_lfeet_dist'] = self.distance(KPS_INDEX_DICT.left_knee.value,
                                                       KPS_INDEX_DICT.left_ankle.value,
                                                       kps,
                                                       'y')
        self.state['rknee_rfeet_dist'] = self.distance(KPS_INDEX_DICT.right_knee.value,
                                                       KPS_INDEX_DICT.right_ankle.value,
                                                       kps,
                                                       'y')
        self.state['lhip_lfeet_dist'] = self.distance(KPS_INDEX_DICT.left_hip.value,
                                                      KPS_INDEX_DICT.left_ankle.value,
                                                      kps,
                                                      'y')
        self.state['rhip_rfeet_dist'] = self.distance(KPS_INDEX_DICT.right_hip.value,
                                                      KPS_INDEX_DICT.right_ankle.value,
                                                      kps,
                                                      'y')
        self.state['lpalm_lhip_dist'] = self.distance(KPS_INDEX_DICT.left_wrist.value,
                                                      KPS_INDEX_DICT.left_hip.value,
                                                      kps,
                                                      'y')
        self.state['rpalm_rhip_dist'] = self.distance(KPS_INDEX_DICT.right_wrist.value,
                                                      KPS_INDEX_DICT.right_hip.value,
                                                      kps,
                                                      'y')
        self.state['lpalm_lfeet_dist'] = self.distance(KPS_INDEX_DICT.left_wrist.value,
                                                       KPS_INDEX_DICT.left_ankle.value,
                                                       kps,
                                                       'y')
        self.state['rpalm_rfeet_dist'] = self.distance(KPS_INDEX_DICT.right_wrist.value,
                                                       KPS_INDEX_DICT.right_ankle.value,
                                                       kps,
                                                       'y')
        self.state['lrpalm_dist'] = self.distance(KPS_INDEX_DICT.left_wrist.value,
                                                  KPS_INDEX_DICT.right_wrist.value,
                                                  kps,
                                                  'x')
        self.state['lshl_angle'] = self.angle(KPS_INDEX_DICT.left_elbow.value,
                                              KPS_INDEX_DICT.left_shoulder.value,
                                              KPS_INDEX_DICT.left_hip.value,
                                              kps)
        self.state['rshl_angle'] = self.angle(KPS_INDEX_DICT.right_elbow.value,
                                              KPS_INDEX_DICT.right_shoulder.value,
                                              KPS_INDEX_DICT.right_hip.value,
                                              kps)
    
    def get_metric_names(self):
        metricNames = [
        "shl_dist", "lshl_lpalm_dist", "rshl_rPalm_dist", "lshl_rpalm_dist",
        "rShl_lpalm_dist", "lshl_lHip_dist", "rshl_rhip_dist", "lknee_lhip_dist",
        "rknee_rhip_dist", "lknee_lfeet_dist", "rknee_rfeet_dist", "lhip_lfeet_dist",
        "rhip_rfeet_dist", "lpalm_lhip_dist", "rpalm_rhip_dist", "lpalm_lfeet_dist",
        "rpalm_rfeet_dist", "lrpalm_dist", "lshl_angle", "rshl_angle"
        ]
        
        return metricNames
    
if __name__ == "__main__":
    jj = KpsMtricsJumpingJack()
 

    

    