class Observable:
    """The Subject (Observable)"""
    def __init__(self):
        self._observers = set()
        
    def subscribe(self, observer):
        self._observers.add(observer)
        
    def unsubscribe(self, observer):
        self._observers.remove(observer)
        
    def notify(self, *args):
        for observer in self._observers:
            observer.update(self, *args)
            
class Observer:
    """The concrete observer"""
    def __init__(self, observables):
        for observable in observables:
            observable.subscribe(self)
    
