
from PyQt6.QtWidgets import QDialog, QListWidgetItem
from dialog_camera_source import Ui_Dialog
import cv2
import warnings
from video_source import VideoSource

class CameraSourceSelectorDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.camera_source_list.currentItemChanged.connect(self.on_camera_source_changed)
        self.buttonBox.accepted.connect(self.on_accepted)
        self.buttonBox.rejected.connect(self.on_rejected)
        
        self.selected_camera_port = None
        self.preview_vid_source:VideoSource = None
        
    def find_camera_source(self):
        cam_port_list = []
        for port in range(5):
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
        self.preview_vid_source = VideoSource(source, 
                                              VideoSource.SourceType.Camera, 
                                              video_capture_api=cv2.CAP_V4L2)
        self.preview_vid_source.onFrame.connect(self.on_frame)
        self.preview_vid_source.onReadFrameFail.connect(self.on_read_frame_fail)
        self.preview_vid_source.start()
    
    def release_resource(self):
        if self.preview_vid_source:
            if self.preview_vid_source.isRunning():
                self.preview_vid_source.resume()
                self.preview_vid_source.requestInterruption()
                
    def on_frame(self, frame):
        print(frame.shape)
        
    def on_read_frame_fail(self, frame):
        print("unable to read frame")
                   
    def on_accepted(self):
        self.release_resource()
    
    def on_rejected(self):
        self.release_resource()
    
    def on_camera_source_changed(self, current:QListWidgetItem, previous:QListWidgetItem):
        print(f"selected camera port {current.text()}")
        self.selected_camera_port = current.text()
        self.start_preview(self.selected_camera_port)
    
    def closeEvent(self, evt):
        self.release_resource()
        