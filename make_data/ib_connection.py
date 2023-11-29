from ib_insync import *


def ib_connection(func):
    def wrapper(*args, **kwargs):
        util.startLoop()
        with IB() as ib:
            ib.connect("127.0.0.1", 7497, clientId=4)
            result = func(*args, **kwargs, ib=ib)
        return result

    return wrapper
