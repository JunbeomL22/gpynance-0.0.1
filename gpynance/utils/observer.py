from abc import ABCMeta, abstractmethod

class IObservable(metaclass=ABCMeta):
    "The Observable Interface"
    @staticmethod
    @abstractmethod
    def subscribe(observer):
        ""
    @staticmethod
    @abstractmethod
    def unsubscribe(observer):
        ""
    @staticmethod
    @abstractmethod
    def notify(observer):
        ""
        
class Observable(IObservable):
    "The Subject (Observable)"
    def __init__(self):
        self._observers = set()
        
    def subscribe(self, observer):
        self._observers.add(observer)
        
    def unsubscribe(self, observer):
        self._observers.remove(observer)
        
    def notify(self, *args):
        for observer in self._observers:
            observer.update(self, *args)
            
class IObserver(metaclass=ABCMeta):
    "A method for the Observer to implement"
    @staticmethod
    @abstractmethod
    def update(observable, *args):
        ""
class Observer(IObserver):
    "The concrete observer"
    def __init__(self, observable):
        observable.subscribe(self)
        
    #def update(self, observable, *args):
