import time
from RoomController import *
time.sleep(0.1) # Wait for USB to become ready

myroom = RoomController()
myroom.run()
