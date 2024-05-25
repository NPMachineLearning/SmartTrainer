import sys
import os
sys.path.insert(0, os.getcwd())

# Numpy
import numpy as np

# Qt
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent, QImage, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog

# Qt UI
from main_window import Ui_MainWindow

# matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from qt_app.video_rep_counter import VideoRepetitionCounter

# Repetition counter
from rep_counting.pkg.kps_metrics import KpsMetrics
from rep_counting.rep_counter import RepetitionCounter


NO_VIDEO_SOURCE_MSG = "No video source"
CONFIG_FILE = './smart_trainer_config/config.json'
MODEL_PATH = './rep_counting/movenet/movenet_singlepose_thunder_3.tflite'

EXERCISE_METRICS_MAP = {
    "Jumping jacks": "jumping_jacks",
    "Push ups": "push_ups",
}

class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # create signal/metric plot
        dynamic_canvas = FigureCanvasQTAgg(Figure(figsize=(10, 2)))
        self.plotLayout.addWidget(dynamic_canvas)
        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.dynamic_ax.set_xlabel("Frames", loc="left")
        self.dynamic_ax.set_ylabel("Signal")
        self.dynamic_ax.set_title("Exercise signals")
        self.metric_plot = self.dynamic_ax.plot([], [], 'b-')[0]
        
        # connect slots
        self.action_open_video.triggered.connect(self.on_open_video)
        self.start_button.clicked.connect(self.on_start_clicked)
        self.toggle_pause_button.clicked.connect(self.on_toggle_pause)
        self.exercise_list.currentItemChanged.connect(self.on_exercise_changed)
        
        # disable buttons
        self.start_button.setEnabled(False)
        self.toggle_pause_button.setEnabled(False)
        
        # init variables
        self.img_frame.setText(NO_VIDEO_SOURCE_MSG)
        self.exercise_list.addItems(list(EXERCISE_METRICS_MAP.keys()))
        self.video_path = None
        
        # video queue
        self.video_queue:list[VideoRepetitionCounter] = []
        
        # create repetition counter 
        self.rep_counter = RepetitionCounter(MODEL_PATH, CONFIG_FILE)
    
    def on_open_video(self):
        vid_path, _ = QFileDialog.getOpenFileName(self,
                                               "Open video",
                                               filter="Video file (*.mp4)")
                
        if os.path.exists(vid_path):
            # set video path
            self.video_path = vid_path
            
            # cancel current video
            if len(self.video_queue):
                self._cancel_current_video(self.video_queue[-1])
        
            # create a video repetition counter
            counter = self._create_video_rep_counter(self.rep_counter)
            
            # only prepare video when there is no video in queue
            # otherwise prepare video will be called within
            # previous video complete/interrupt event
            should_prepare = not len(self.video_queue)
            
            # add video to queue
            self.video_queue.append(counter)
            
            if should_prepare:
                self._prepare_video()
            
    def _cancel_current_video(self, v_rep_counter:VideoRepetitionCounter):
        if v_rep_counter and v_rep_counter.isRunning():
            # make sure video source is in playing state
            # otherwise thread thread will be locked
            # in waiting state
            v_rep_counter.resume()
            
            # tell video source to stop
            v_rep_counter.requestInterruption()
    
    def _create_video_rep_counter(self, rep_counter:RepetitionCounter):
        # create new video repetition counter
        counter = VideoRepetitionCounter(self.video_path, rep_counter, 30.)
        
        # connect slots    
        counter.onRepCount.connect(self.on_rep_count)
        counter.onInterrupted.connect(self.on_interrupted)
        counter.onCompleted.connect(self.on_video_completed)
        counter.finished.connect(counter.deleteLater)
        
        return counter
    
    def _prepare_video(self):
        if len(self.video_queue):
            # render first frame of video in last video queue
            video = self.video_queue[-1]
            first_frame = video.read_frame()
            if first_frame is not None:
                self._render_frame(first_frame)
                
            self.start_button.setEnabled(True)
            self.toggle_pause_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)
            self.toggle_pause_button.setEnabled(False)
                
    def _render_frame(self, frame):
        # get widget width and height
        d_width = self.img_frame.size().width()-5
        d_height = self.img_frame.size().height()-5
        
        # create qt image
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
        
        # scale image
        image = image.scaled(d_width, d_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        # display frame
        self.img_frame.setPixmap(QPixmap.fromImage(image))
    
    def _update_metric_plot(self, metric:KpsMetrics):
        t_frame = list(range(len(metric.tracked_metrics)))
        
        # update signal plot data
        self.metric_plot.set_data(t_frame, 
                                  metric.tracked_metrics)
        
        # get metric's mean
        mean = metric.config['reference']['mean']
        
        # if axes contain more than 2 artists
        # remove last one since last one is horizontal
        # line for mean 
        if len(self.dynamic_ax.lines) >= 2:
            self.dynamic_ax.lines[-1].remove()
        
        # add horizontal line for mean
        self.dynamic_ax.axhline(mean, 0, len(t_frame), color='r')
        
        # recalculate limit for plot
        self.dynamic_ax.relim()
        
        # auto scale axes
        self.dynamic_ax.autoscale_view(True, True, True)
        
        # redraw
        self.metric_plot.figure.canvas.draw()
    
    def on_rep_count(self, frame:np.ndarray, counter:RepetitionCounter):
        # get metric
        metric = counter.get_metric(counter.current_metric_name)
        
        # update repetition count for label
        self.rep_count_label.setText(str(metric.reptition_count))
        
        # display frame
        self._render_frame(frame)
        
        # update signal plot
        self._update_metric_plot(metric)
            
    def on_video_completed(self):
        # pop first video from queue
        self.video_queue.pop(0)
        
        # prepare next queued video
        self._prepare_video()
        
    def on_interrupted(self):
        # pop first video from queue
        self.video_queue.pop(0)
        
        # prepare next queued video
        self._prepare_video()
                
    def on_start_clicked(self):
        # start last video in queue if it is not running
        if len(self.video_queue) and not self.video_queue[-1].isRunning():
            self.rep_count_label.setText("0")
            self.rep_counter.reset_metrics()
            self.video_queue[-1].start()
            
    def on_toggle_pause(self):
        if len(self.video_queue) and self.video_queue[-1].isRunning():
            video = self.video_queue[-1]
            if video.is_paused():
                video.resume()
                self.toggle_pause_button.setText("Pause")
            else:
                video.pause()
                self.toggle_pause_button.setText("Resume")
    
    def on_exercise_changed(self, current, previous):
        exercise_name = current.text()
        self.rep_counter.set_metric(EXERCISE_METRICS_MAP[exercise_name])
                    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if len(self.video_queue):
            self._cancel_current_video(self.video_queue[-1])
        a0.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())        