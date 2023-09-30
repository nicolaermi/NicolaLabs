import time
from GameController import*
time.sleep(0.1) # Wait for USB to become ready

myroom = GameController()
myroom.run()
