import threading

class ThreadHandler(threading.Thread):
    def __init__(self, target, stop_event):
        super().__init__()
        self.target = target
        self.stop_event = stop_event

    def run(self):
        self.target()
