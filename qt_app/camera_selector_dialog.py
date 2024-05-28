
from PyQt6.QtWidgets import QDialog, QListWidgetItem
from dialog_camera_source import Ui_Dialog
import cv2
import warnings

class CameraSourceSelectorDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.camera_source_list.currentItemChanged.connect(self.on_camera_source_changed)
        self.buttonBox.accepted.connect(self.on_accepted)
        self.buttonBox.rejected.connect(self.on_rejected)
        
        self.selected_camera_port = None
        
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
          
    def on_accepted(self):
        pass
    
    def on_rejected(self):
        pass
    
    def on_camera_source_changed(self, current:QListWidgetItem, previous:QListWidgetItem):
        print(f"selected camera port {current.text()}")
        self.selected_camera_port = int(current.text())
        