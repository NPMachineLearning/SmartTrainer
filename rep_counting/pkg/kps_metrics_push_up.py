from .kps_metrics import KpsMetrics
from .kps_constant import KPS_INDEX_DICT
from enum import Enum

class KpsMetricsPushup(KpsMetrics):
    metric_names = Enum("PushupMetricNames", [
        "lshl_lpalm_dist", 
        "rshl_rPalm_dist",
        "lshl_lhip_dist",
        "rshl_rhip_dist", 
        "lknee_lhip_dist",
        "rknee_rhip_dist", 
        "lknee_lfeet_dist", 
        "rknee_rfeet_dist", 
        "lhip_lfeet_dist",
        "rhip_rfeet_dist",   
        "lelb_angle", 
        "relb_angle",
        "lshl_angle",
        "rshl_angle"
        ])
    
    exercise_name = 'Pushup'
    
    def __init__(self, low_pass_filter=True, low_pass_filter_alpha=0.4, config_path=None):
        super().__init__(low_pass_filter=low_pass_filter,
                         low_pass_filter_alpha=low_pass_filter_alpha,
                         config_path=config_path)
    
    def get_exercise_name(self) -> str:
        return self.exercise_name.lower()
    
    def _get_query_pattern(self) -> list[int]:
        return [1, 0, 1]
    
    def _process_metrics(self, kps, states, ratio):
        states[self.metric_names.lshl_lpalm_dist.name] = self.distance(KPS_INDEX_DICT.left_shoulder.value,
                                                                        KPS_INDEX_DICT.left_wrist.value,
                                                                        kps,
                                                                        'xy',
                                                                        ratio)
        states[self.metric_names.rshl_rPalm_dist.name] = self.distance(KPS_INDEX_DICT.right_shoulder.value,
                                                                       KPS_INDEX_DICT.right_wrist.value,
                                                                       kps,
                                                                       "xy",
                                                                       ratio)
        states[self.metric_names.lshl_lhip_dist.name] = self.distance(KPS_INDEX_DICT.left_shoulder.value,
                                                                      KPS_INDEX_DICT.left_hip.value,
                                                                      kps,
                                                                      "xy",
                                                                      ratio)
        states[self.metric_names.rshl_rhip_dist.name] = self.distance(KPS_INDEX_DICT.right_shoulder.value,
                                                                      KPS_INDEX_DICT.right_hip.value,
                                                                      kps,
                                                                      "xy",
                                                                      ratio)
        states[self.metric_names.lknee_lhip_dist.name] = self.distance(KPS_INDEX_DICT.left_knee.value,
                                                                       KPS_INDEX_DICT.left_hip.value,
                                                                       kps,
                                                                       "xy",
                                                                       ratio)
        states[self.metric_names.rknee_rhip_dist.name] = self.distance(KPS_INDEX_DICT.right_knee.value,
                                                                       KPS_INDEX_DICT.right_hip.value,
                                                                       kps,
                                                                       "xy",
                                                                       ratio)
        states[self.metric_names.lknee_lfeet_dist.name] = self.distance(KPS_INDEX_DICT.left_knee.value,
                                                                        KPS_INDEX_DICT.left_ankle.value,
                                                                        kps,
                                                                        "xy",
                                                                        ratio)
        states[self.metric_names.rknee_rfeet_dist.name] = self.distance(KPS_INDEX_DICT.right_knee.value,
                                                                        KPS_INDEX_DICT.right_ankle.value,
                                                                        kps,
                                                                        "xy",
                                                                        ratio)
        states[self.metric_names.lhip_lfeet_dist.name] = self.distance(KPS_INDEX_DICT.left_hip.value,
                                                                       KPS_INDEX_DICT.left_ankle.value,
                                                                       kps,
                                                                       "xy",
                                                                       ratio)
        states[self.metric_names.rhip_rfeet_dist.name] = self.distance(KPS_INDEX_DICT.right_hip.value,
                                                                       KPS_INDEX_DICT.right_ankle.value,
                                                                       kps,
                                                                       "xy",
                                                                       ratio)
        states[self.metric_names.lelb_angle.name] = self.angle(KPS_INDEX_DICT.left_shoulder.value,
                                                               KPS_INDEX_DICT.left_elbow.value,
                                                               KPS_INDEX_DICT.left_wrist.value,
                                                               kps)
        states[self.metric_names.relb_angle.name] = self.angle(KPS_INDEX_DICT.right_shoulder.value,
                                                               KPS_INDEX_DICT.right_elbow.value,
                                                               KPS_INDEX_DICT.right_wrist.value,
                                                               kps)
        states[self.metric_names.lshl_angle.name] = self.angle(KPS_INDEX_DICT.left_elbow.value,
                                                               KPS_INDEX_DICT.left_shoulder.value,
                                                               KPS_INDEX_DICT.left_hip.value,
                                                               kps)
        states[self.metric_names.rshl_angle.name] = self.angle(KPS_INDEX_DICT.right_elbow.value,
                                                               KPS_INDEX_DICT.right_shoulder.value,
                                                               KPS_INDEX_DICT.right_hip.value,
                                                               kps)
        
    def get_metric_names(self):
        return self.metric_names
    
if __name__ == "__main__":
    pushup = KpsMetricsPushup()
 

    

    