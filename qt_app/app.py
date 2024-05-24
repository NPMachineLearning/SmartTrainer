import sys
import os
sys.path.insert(0, os.getcwd())
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent, QImage, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from main_window import Ui_MainWindow
from video_source import VideoSource
from rep_counter_wrapper import RepetitionCounterWrapper, RepetitionCounter
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from rep_counting.pkg.kps_metrics import KpsMetrics

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
        
        # create signal plot
        dynamic_canvas = FigureCanvasQTAgg(Figure(figsize=(10, 2)))
        self.plotLayout.addWidget(dynamic_canvas)
        self.dynamic_ax = dynamic_canvas.figure.subplots()
        self.dynamic_ax.set_xlabel("Frames", loc="left")
        self.dynamic_ax.set_ylabel("Signal")
        self.dynamic_ax.set_title("Exercise signals")
        self.metric_plot = self.dynamic_ax.plot([], [], 'b-')[0]
        
        # connect slots
        self.action_open_video.triggered.connect(self.open_video)
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
        self.video_source = None
        
        # rep counter wrapper
        self.rep_counter = RepetitionCounterWrapper(MODEL_PATH, CONFIG_FILE)
        self.rep_counter.onRepCounterUpdated.connect(self.on_rep_counter_updated)
    
    def open_video(self):
        vid_path, _ = QFileDialog.getOpenFileName(self,
                                               "Open video",
                                               filter="Video file (*.mp4)")
                
        if os.path.exists(vid_path):
            # set video path
            self.video_path = vid_path
            
            # remove current video source
            self.remove_video_source()
            
            # create new video source
            self.video_source = VideoSource(self.video_path, 30.)
            
            # render first frame
            first_frame = self.video_source.read_frame()
            if first_frame is not None:
                self.render_frame(first_frame)
            
            # connect slots    
            self.video_source.onFrame.connect(self.on_video_frame)
            self.video_source.onFinished.connect(self.on_video_finished)
            self.video_source.onInterrupted.connect(self.on_interrupted)
            self.video_source.finished.connect(self.video_source.deleteLater)
            
            # enable buttons
            self.start_button.setEnabled(True)
            self.toggle_pause_button.setEnabled(True)
            
    def remove_video_source(self):
        if self.video_source and self.video_source.isRunning():
            # make sure video source is in playing state
            self.video_source.resume()
            
            # tell video source to stop
            self.video_source.requestInterruption()
            
            # don't receive signal for new frame
            self.video_source.onFrame.disconnect()
            self.video_source = None
    
    def render_frame(self, frame):
        # get widget width and height
        d_width = self.img_frame.size().width()-5
        d_height = self.img_frame.size().height()-5
        
        # create qt image
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
        
        # scale image
        image = image.scaled(d_width, d_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        # display frame
        self.img_frame.setPixmap(QPixmap.fromImage(image))
    
    def update_metric_plot(self, metric:KpsMetrics):
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
        
        # recalculate limit
        self.dynamic_ax.relim()
        
        # auto scale axes
        self.dynamic_ax.autoscale_view(True, True, True)
        
        # redraw
        self.metric_plot.figure.canvas.draw()
        
    def on_rep_counter_updated(self, counter:RepetitionCounter, frame:np.ndarray):
        # get metric
        metric = counter.get_metric(counter.current_metric_name)
        
        # update repetition count for label
        self.rep_count_label.setText(str(metric.reptition_count))
        
        # display frame
        self.render_frame(frame)
        
        # update signal plot
        self.update_metric_plot(metric)
                    
    def on_video_frame(self, frame):
        # add frame for repetition counter processing
        self.rep_counter.add_frame(frame)
        
    def on_video_finished(self):
        self.video_source = None
        self.img_frame.setText(NO_VIDEO_SOURCE_MSG)
        self.start_button.setEnabled(False)
        self.toggle_pause_button.setEnabled(False)
        
    def on_interrupted(self):
        print("Video source interrupted")
        
    def on_start_clicked(self):
        if self.video_source and not self.video_source.isRunning():
            self.video_source.start()
        if self.rep_counter:
            self.rep_count_label.setText("0")
            self.rep_counter.reset_metrics()
            self.rep_counter.start()
            
    def on_toggle_pause(self):
        if self.video_source and self.video_source.isRunning():
            if self.video_source.is_paused():
                self.video_source.resume()
                self.toggle_pause_button.setText("Pause")
            else:
                self.video_source.pause()
                self.toggle_pause_button.setText("Resume")
    
    def on_exercise_changed(self, current, previous):
        exercise_name = current.text()
        self.rep_counter.set_metric(EXERCISE_METRICS_MAP[exercise_name])
                    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # todo: do extra stuff here before app exit
        self.remove_video_source()
        if self.rep_counter:
            self.rep_counter.requestInterruption()
        a0.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())        