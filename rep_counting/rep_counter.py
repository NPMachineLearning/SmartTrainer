import cv2
from .movenet.movenet_infer import load_model, predict, preprocess_input_image_cv, preprocess_kps, INPUT_SIZE, MODEL_PATH
from .pkg.kps_metrics_jumping_jack import KpsMetricsJumpingJack
from .pkg.kps_metrics_push_up import KpsMetricsPushup
from .pkg.kps_metrics import KpsMetrics
from .pkg.kps_constant import KPS_SKELETON_DRAW_DATA

class RepetitionCounter:
    def __init__(self, config_path, model_path=MODEL_PATH) -> None:
        """
        RepetitionCounter is a class that can handle multiple supported
        exercises. Each exercise has its own metric which is inherite from
        KpsMetrics.

        Args:
            config_path (str): path to exerise config json file 
            model_path (str): path movenet model tflite file
        """
        self.model_path = model_path
        self.config_path = config_path
        self.current_metric_name = None
        
        self.model = self._load_model(model_path=self.model_path)
        self.exercise_metrics = self._load_exercise_metrics(self.config_path)
    
    def _load_model(self, model_path):
        """
        Load movenet model

        Args:
            model_path (str): path to model tflite file

        Returns:
            tuple: (model, input_detail, output_detail) 
        """
        return load_model(model_path=model_path)
    
    def _load_exercise_metrics(self, config_path) -> {str, KpsMetrics}:
        """
        Load all exercise metrics

        Returns:
            dict: a dictionary where key is exercise name
            and value is exerise metric
        """
        return {
            "jumping_jacks": KpsMetricsJumpingJack(config_path=config_path),
            "push_ups": KpsMetricsPushup(config_path=config_path)
        }
    
    def set_metric(self, exercise_name):
        """
        Set current exercise metric

        Args:
            exercise_name (str): exercise name

        Raises:
            Exception: if exercise name dose not exists 
        """
        list_metric_names = list(self.exercise_metrics.keys())
        if not exercise_name in list_metric_names:
            raise Exception(f"{exercise_name} is not one of {list_metric_names}")
        self.current_metric_name = exercise_name
    
    def get_metric(self, exercise_name) -> KpsMetrics:
        """
        Get specific exercise metric

        Args:
            exercise_name (str): exercise name

        Raises:
            Exception: if exercise name dose not exists

        Returns:
            KpsMetrics: exercise metric
        """
        list_metric_names = list(self.exercise_metrics.keys())
        if not exercise_name in list_metric_names:
            raise Exception(f"{exercise_name} is not one of {list_metric_names}")
        return self.exercise_metrics[exercise_name]
    
    def reset_metrics(self):
        """
        Reset all exercise metrics
        """
        self.exercise_metrics = self._load_exercise_metrics(self.config_path)
        
    def update_metric(self, cv_frame):
        """
        Update repetion counter metric

        Args:
            cv_frame (NDArray): frame from opencv or numpy array

        Raises:
            Exception: if there is no current metric selected

        Returns:
            NDArray: keypoints from movnet in xy coordinate and is normlized 
        """
        if self.current_metric_name is None:
            raise Exception("call set_metric method at least once to set current metric name")
        
        input_img = preprocess_input_image_cv(cv_frame, INPUT_SIZE)
        kps_norm = predict(input_img, self.model)
        kps_norm, conf_rate = preprocess_kps(kps_norm)
        metric:KpsMetrics = self.exercise_metrics[self.current_metric_name]
        metric.update_metrics(kps_norm, confidence_rate=conf_rate)
        return kps_norm 
        
    def draw_kps_skeleton(self, cv_frame, kps_norm, thickness:int=1):
        """
        Draw skleleton with color on frame.

        Args:
            cv_frame (NDArray): frame from Opencv or numpy array
            kps_norm (NDAarry): movenet keypoints and is normalized
            thickness (int, optional): line thickness. Defaults to 1.

        Returns:
            _type_: _description_
        """
        height, width, _ = cv_frame.shape
        
        # will be used to scale kps to frame size
        scale_xy = (width, height)
        
        for draw_name in list(KPS_SKELETON_DRAW_DATA.keys()):
            # get start & end point index and color for drawing line
            start_kp_idx, end_kp_indx, color = KPS_SKELETON_DRAW_DATA[draw_name]
            
            # create line points(start & end) data and scale it to frame size 
            line_points = ((int(kps_norm[start_kp_idx][0] * scale_xy[0]), int(kps_norm[start_kp_idx][1] * scale_xy[1])),
                           (int(kps_norm[end_kp_indx][0] * scale_xy[0]), int(kps_norm[end_kp_indx][1] * scale_xy[1])))
            
            # draw on frame
            cv_frame = cv2.line(cv_frame, line_points[0], line_points[1], color, thickness)

        return cv_frame