class LPFilter:
    def __init__(self):
        self.value = None
    
    def update(self, x, alpha=0.4):
        if self.value is None:
            self.value = x
        else:
            self.value = alpha * x + (1.0 - alpha) * self.value
        return self.value
        