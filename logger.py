import globals
import time

show = 1
log = []

def log(message, weight = 1):
    mess = Message(message, weight)
    log.append(mess)
    if mess.weight >= show:
        print(mess)

class Message():
    def __init__(message, weight):
        self.message = message
        self.weight = weight
        self.time = time.time()