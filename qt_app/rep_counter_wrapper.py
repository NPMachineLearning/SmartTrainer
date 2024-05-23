from PyQt6.QtCore import QThread, pyqtSignal, QMutex
from rep_counting.rep_counter import RepetitionCounter

class RepetitionCounterWrapper(QThread):
    onRepCounterUpdated = pyqtSignal(RepetitionCounter)
    
    def __init__(self, model_path, config_path):
        super().__init__()
        self.sync = QMutex()
        self.queue_frame = []
        self.rep_counter = RepetitionCounter(model_path, config_path)      
    
    def set_metric(self, name):
        self.sync.lock()
        self.rep_counter.set_metric(name)
        self.sync.unlock()
        
    def add_frame(self, frame):
        self.sync.lock()
        self.queue_frame.append(frame)
        self.sync.unlock()
                
    def run(self):
        try:
            while(not self.isInterruptionRequested()):
                self.sync.lock()
                if len(self.queue_frame) == 0:
                    pass
                else:
                    for frame in self.queue_frame:
                        self.rep_counter.update_metric(frame)
                    self.queue_frame.clear()
                    self.onRepCounterUpdated.emit(self.rep_counter)
                self.sync.unlock()
        except:
                print("Something went wrong")    
             
        