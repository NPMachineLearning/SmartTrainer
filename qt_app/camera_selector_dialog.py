import time
from PyQt6.QtWidgets import QDialog, QListWidgetItem
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from dialog_camera_source import Ui_Dialog
import cv2
import warnings
from video_source import VideoSource

class CameraSourceSelectorDialog(QDialog, Ui_Dialog):
    onCameraSelected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.camera_source_list.currentItemChanged.connect(self.on_camera_source_changed)
        self.buttonBox.accepted.connect(self.on_accepted)
        self.buttonBox.rejected.connect(self.on_rejected)
        
        self.selected_camera_port = None
        self.cam_source:VideoSource = None
        self.current_camera_avaliable = False
        
    def find_camera_source(self, device_port_range:int=5):
        cam_port_list = []
        for port in range(device_port_range):
            try:
                cap = cv2.VideoCapture(port)
                if cap.isOpened():
                    cam_port_list.append(str(port))
                cap.release()
            except:
                cap.release()
                warnings.warn(f"No camera device detected at port {port}")
        
        if len(cam_port_list) > 0:
            self.camera_source_list.addItems(cam_port_list)
            selected_item = self.camera_source_list.item(0)
            self.camera_source_list.setCurrentItem(selected_item)
    
    def start_preview(self, source):
        if self.cam_source and self.cam_source.isRunning():
            self.cam_source.requestInterruption()
            self.cam_source.onFrame.disconnect()
            
        self.cam_source = VideoSource(source, VideoSource.SourceType.Camera)
        self.cam_source.onFrame.connect(self.on_frame)
        self.cam_source.onVideoSourceFail.connect(self.on_camera_fail)
        self.cam_source.finished.connect(self.cam_source.deleteLater)
        self.cam_source.start()
    
    def release_resource(self):
        if self.cam_source:
            if self.cam_source.isRunning():
                self.cam_source.resume()
                self.cam_source.requestInterruption()
                
    def on_frame(self, frame):
        self.current_camera_avaliable = True
        
         # get widget width and height
        d_width = self.preview_cam_img.size().width()-5
        d_height = self.preview_cam_img.size().height()-5
        
        # create qt image
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
        
        # scale image
        image = image.scaled(d_width, d_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        # display frame
        self.preview_cam_img.setPixmap(QPixmap.fromImage(image))
        
    def on_read_frame_fail(self, frame):
        self.current_camera_avaliable = False
        
        self.preview_cam_img.setText(f"Unable to stream at camera device port {self.cam_source.video_path}")
        self.preview_cam_img.setStyleSheet("color: rgb(255, 0, 0);")
        
    def on_camera_fail(self):
        self.current_camera_avaliable = False
        
        self.preview_cam_img.setText(f"Unable to open camera at device port {self.cam_source.video_path}")
        self.preview_cam_img.setStyleSheet("color: rgb(255, 0, 0);")
                   
    def on_accepted(self):
        if self.current_camera_avaliable:
            vid_path = self.cam_source.video_path
            self.release_resource()
            # wait 1 second for camera resource to be released
            time.sleep(1.)
            self.onCameraSelected.emit(vid_path)
        
    def on_rejected(self):
        self.release_resource()
    
    def on_camera_source_changed(self, current:QListWidgetItem, previous:QListWidgetItem):
        self.selected_camera_port = current.text()
        self.start_preview(self.selected_camera_port)
        