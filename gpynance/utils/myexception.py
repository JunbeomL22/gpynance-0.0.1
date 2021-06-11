class MyException(Exception):
    def __init__(self, message, cls=None, name = ""):
        if cls is not None:
            message += ", class: " + cls.__class__.__name__
        message += ", name: " + name
        super().__init__(message)

class MyFunctionException(Exception):
    def __init__(self, message, name = ""):
        message += ", function: " + name
        super().__init__(message)

