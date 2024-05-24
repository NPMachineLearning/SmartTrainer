import tensorflow as tf
from .movenet.movenet_infer import load_model, predict, preprocess_input_image, preprocess_kps, INPUT_SIZE
from .pkg.kps_metrics_jumping_jack import KpsMetricsJumpingJack
from .pkg.kps_metrics_push_up import KpsMetricsPushup
from .pkg.kps_metrics import KpsMetrics

class RepetitionCounter:
    def __init__(self, model_path, config_path) -> None:
        self.model_path = model_path
        self.config_path = config_path
        self.current_metric_name = None
        
        self.model, self.input, self.output = self._load_model(model_path=self.model_path)
        self.exercise_metrics = self._load_exercise_metrics(self.config_path)
    
    def _load_model(self, model_path):
        return load_model(model_path=model_path)
    
    def _load_exercise_metrics(self, config_path) -> {str, KpsMetrics}:
        return {
            "jumping_jacks": KpsMetricsJumpingJack(config_path=config_path),
            "push_ups": KpsMetricsPushup(config_path=config_path)
        }
    
    def set_metric(self, exercise_name):
        list_metric_names = list(self.exercise_metrics.keys())
        if not exercise_name in list_metric_names:
            raise Exception(f"{exercise_name} is not one of {list_metric_names}")
        self.current_metric_name = exercise_name
    
    def get_metric(self, exercise_name) -> KpsMetrics:
        list_metric_names = list(self.exercise_metrics.keys())
        if not exercise_name in list_metric_names:
            raise Exception(f"{exercise_name} is not one of {list_metric_names}")
        return self.exercise_metrics[exercise_name]
    
    def reset_metrics(self):
        self.exercise_metrics = self._load_exercise_metrics(self.config_path)
        
    def update_metric(self, cv_frame):
        if self.current_metric_name is None:
            raise Exception("call set_metric method at least once to set current metric name")
        
        input_img = tf.convert_to_tensor(cv_frame)
        input_img = preprocess_input_image(input_img, INPUT_SIZE)
        kps = predict(input_img, self.model, self.input, self.output)
        kps = preprocess_kps(kps)
        metric = self.exercise_metrics[self.current_metric_name]
        metric.update_metrics(kps)
        