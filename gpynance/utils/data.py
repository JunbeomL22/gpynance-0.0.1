from gpynance.utils.observer import Observable

class Data(Observable):
    def __init__(self, data, name=""):
        super().__init__()
        self.data = data
        
        
