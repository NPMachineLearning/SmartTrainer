from PyQt6.QtCore import QThread, pyqtSignal, QMutex
from rep_counting.rep_counter import RepetitionCounter
import numpy as np

class RepetitionCounterWrapper(QThread):
    onRepCounterUpdated = pyqtSignal(RepetitionCounter, np.ndarray)
    
    def __init__(self, model_path, config_path):
        super().__init__()
        self.sync = QMutex()
        self.queue_frame = []
        self.rep_counter = RepetitionCounter(model_path, config_path)      
    
    def set_metric(self, name):
        self.rep_counter.set_metric(name)
        
    def add_frame(self, frame):
        self.queue_frame.append(frame)
             
    def run(self):
        try:
            while(not self.isInterruptionRequested()):
                if len(self.queue_frame) == 0:
                    pass
                else:
                    frame = self.queue_frame.pop(0)
                    self.rep_counter.update_metric(frame)
                    self.onRepCounterUpdated.emit(self.rep_counter, frame)
        except:
                print("Something went wrong")    
             
        