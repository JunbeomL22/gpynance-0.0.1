class MyException(Exception):
    def __init__(self, message, cls=None, name = "undefined"):
        if cls is not None:
            message += ", class: " + cls.__class__.__name__
        message += ", name: " + name
        super().__init__(message)
        
