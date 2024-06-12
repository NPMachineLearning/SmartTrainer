import sys
import os

# Solve custom module rep_counting import
# issue.
#
# rep_counting module must located at same
# level of qt_app or within qt_app
sys.path.insert(0, os.getcwd())
sys.path.insert(0, '../')

# Numpy
import numpy as np

# Qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

# Qt UI
from ui.main_window import Ui_MainWindow
from ui.camera_selector_dialog import CameraSourceSelectorDialog

# matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from video_source.video_rep_counter import VideoRepetitionCounter

# Repetition counter
from rep_counting.pkg.kps_metrics import KpsMetrics
from rep_counting.rep_counter import RepetitionCounter

# Get absolute path current working directory where
# sys.argv[0] contain path to current program.
# This solve bundle executable app path issue.
#
# e.g on MacOS os.path.getcwd() always resolve to
# incorrect path /Users/XXX-user-name-XXX not the program 
# working directory
CWDPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
NO_VIDEO_SOURCE_MSG = "No video source"
CONFIG_FILE = os.path.join(CWDPATH,
                           'smart_trainer_config/config.json')

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
        self.action_camera_source.triggered.connect(self.on_open_camera)
        self.start_button.clicked.connect(self.on_start_clicked)
        self.pause_button.clicked.connect(self.on_pause_clicked)
        self.exercise_list.currentItemChanged.connect(self.on_exercise_changed)
        self.draw_skeleton_checkbox.stateChanged.connect(self.on_draw_skeleton_changed)
        
        # disable buttons
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        
        # init variables
        self.img_frame.setText(NO_VIDEO_SOURCE_MSG)
        self.exercise_list.addItems(list(EXERCISE_METRICS_MAP.keys()))
        self.video_path = None
        self.current_exercise_name = ''
        self.camera_selector_dialog = None
        
        # video queue
        self.video_queue:list[VideoRepetitionCounter] = []
        
        # create repetition counter 
        self.rep_counter = RepetitionCounter(CONFIG_FILE)
        
    def on_draw_skeleton_changed(self):
        if len(self.video_queue):
            video = self.video_queue[-1]
            video.set_draw_skeleton(self.draw_skeleton_checkbox.isChecked())
        
    def on_open_camera(self):
        # show dialog
        self.camera_selector_dialog = CameraSourceSelectorDialog(self)
        self.camera_selector_dialog.onCameraSelected.connect(self.on_camera_selected)
        self.camera_selector_dialog.show()
        self.camera_selector_dialog.find_camera_source()
        
    def on_camera_selected(self, cam_port):
        self.video_path = cam_port
        
        if len(self.video_queue):
            self._cancel_current_video(self.video_queue[-1])
            
        counter = self._create_camera_rep_counter(cam_port, self.rep_counter)
        
        # add video to queue
        self.video_queue.append(counter)
        
        self.rep_count_label.setText("0")
        self.rep_counter.reset_metrics()
            
        counter.start()
        
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
            
            # add video to queue
            self.video_queue.append(counter)
            
            self.rep_count_label.setText("0")
            self.rep_counter.reset_metrics()
             
            counter.start()
            
    def _cancel_current_video(self, v_rep_counter:VideoRepetitionCounter):
        if v_rep_counter and v_rep_counter.isRunning():
            # make sure video source is in playing state
            # otherwise thread thread will be locked
            # in waiting state
            v_rep_counter.resume()
            
            # tell video source to stop
            v_rep_counter.requestInterruption()
        else:
            # pop first video from queue
            self.video_queue.pop(0)
    
    def _create_video_rep_counter(self, rep_counter:RepetitionCounter):
        # create new video repetition counter
        counter = VideoRepetitionCounter(video_path=self.video_path, 
                                         rep_counter=rep_counter, 
                                         frame_per_second=30.,
                                         pause_at_start=True,
                                         draw_skeleton=self.draw_skeleton_checkbox.isChecked())
        
        # connect slots
        counter.onPrepare.connect(self.on_prepare)
        counter.onReady.connect(self.on_ready)    
        counter.onRepCount.connect(self.on_rep_count)
        counter.onInterrupted.connect(self.on_interrupted)
        counter.onCompleted.connect(self.on_video_completed)
        counter.finished.connect(counter.deleteLater)
        
        return counter
    
    def _create_camera_rep_counter(self, camera_device_port:str, rep_counter:RepetitionCounter):
        draw_skeleton = self.draw_skeleton_checkbox.checkState == Qt.CheckState.Checked
        
        counter = VideoRepetitionCounter(video_path=camera_device_port,
                                         source_type=VideoRepetitionCounter.SourceType.Camera, 
                                         rep_counter=rep_counter, 
                                         frame_per_second=30.,
                                         pause_at_start=True,
                                         draw_skeleton=self.draw_skeleton_checkbox.isChecked())
        
        # connect slots
        counter.onPrepare.connect(self.on_prepare)
        counter.onReady.connect(self.on_ready)  
        counter.onRepCount.connect(self.on_rep_count)
        counter.onInterrupted.connect(self.on_interrupted)
        counter.onCompleted.connect(self.on_video_completed)
        counter.finished.connect(counter.deleteLater)
        
        return counter
                
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
            
        # update title
        self.dynamic_ax.set_title(f"{self.current_exercise_name} signals")
        
        # add horizontal line for mean
        self.dynamic_ax.axhline(mean, 0, len(t_frame), color='r')
        
        # recalculate limit for plot
        self.dynamic_ax.relim()
        
        # auto scale axes
        self.dynamic_ax.autoscale_view(True, True, True)
        
        # redraw
        self.metric_plot.figure.canvas.draw()
    
    def on_prepare(self):
        self.img_frame.setText("Preparing video source....")
    
    def on_ready(self, preview_frame):
        # if no frame then it is camera stream
        if preview_frame is not None:
            self._render_frame(preview_frame)
        else:
            self.img_frame.setText("Click start to start camera streaming")
            
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(True)
            
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
        
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        
    def on_interrupted(self):
        # pop first video from queue
        self.video_queue.pop(0)
                
    def on_start_clicked(self):
        # start last video in queue if it is not running
        if len(self.video_queue) > 0:
            video = self.video_queue[-1]
            if video.is_paused():
                video.resume()
            
    def on_pause_clicked(self):
        if len(self.video_queue) > 0:
            video = self.video_queue[-1] 
            if not video.is_paused():
                video.pause()
    
    def on_exercise_changed(self, current, previous):
        self.current_exercise_name = current.text()
        self.current_exercise_label.setText(self.current_exercise_name)
        self.rep_counter.set_metric(EXERCISE_METRICS_MAP[self.current_exercise_name])
                    
    def closeEvent(self, a0: QCloseEvent) -> None:
        if len(self.video_queue):
            self._cancel_current_video(self.video_queue[-1])
        a0.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())        