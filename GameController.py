"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.

Currently supports only 4 buttons (hardcoded to BTN1 through BTN4)
and a TIMEOUT event for internal tranisitions.

For processing your own events such as sensors, you can implement
those in your run method for transitions based on sensor events.
"""

# Import whatever Library classes you need - Model is obviously needed
import time
import random
from Model import *
from Button import *
from Counters import *
from Lights import *
from CompositeLights import *
from Sensors import *
from Players import *
from Displays import *
from Buzzer import *

"""
This is the template Model Runner - you should rename this class to something
that is supported by your class diagram. This should associate with your other
classes, and any PicoLibrary classes. If you are using Buttons, you will implement
buttonPressed and buttonReleased.

To implement the model, you will need to implement 3 methods to support entry actions,
exit actions, and state actions.

This template currently implements a very simple state model that uses a button to
transition from state 0 to state 1 then a 5 second timer to go back to state 0.
"""

class GameController:

    def __init__(self):
        
        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling
        self._button1 = Button(16, "button1")
        self._button2 = Button(17, "button2")
        self._button3 = Button(18, "button3")
        self._button4 = Button(19, "button4")

        self._timer = SoftwareTimer(None)
        self._light1 = Light(15,'light1')
        self._light2 = Light(14,'light2')
        self._light3 = Light(13,'light3')
        self._light4 = Light(12,'light4')

        self._buzzer = PassiveBuzzer(3)
        
        self._display=LCDDisplay(sda=0,scl=1,i2cid=0)

        self._player1=Players("P1",score=0)
        self._player2=Players("P2",score=0)
        self._order = []
        self._max_length = 2
        self._max_length2 = 2
        self._index= 0




        
        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = Model(9, self, debug=True)
        
        # Up to 4 buttons and a timer can be added to the model for use in transitions
        # Buttons must be added in the sequence you want them used. The first button
        # added will respond to BTN1_PRESS and BTN1_RELEASE, for example
        self._model.addButton(self._button1)
        self._model.addButton(self._button2)
        self._model.addButton(self._button3)
        self._model.addButton(self._button4)
        
        # add other buttons (up to 3 more) if needed
        
        # Add any timer you have.
        self._model.addTimer(self._timer)
        
        # Now add all the transitions that are supported by my Model
        # obvously you only have BTN1_PRESS through BTN4_PRESS
        # BTN1_RELEASE through BTN4_RELEASE
        # and TIMEOUT
        
        # some examples:
        self._model.addTransition(0, [BTN1_PRESS,BTN2_PRESS,BTN3_PRESS,BTN4_PRESS], 1)
        self._model.addTransition(4, [BTN1_PRESS,BTN2_PRESS,BTN3_PRESS,BTN4_PRESS], 5)
        # etc.
    
    """
    Create a run() method - you can call it anything you want really, but
    this is what you will need to call from main.py or someplace to start
    the state model.
    """

    def run(self):
        # The run method should simply do any initializations (if needed)
        # and then call the model's run method.
        # You can send a delay as a parameter if you want something other
        # than the default 0.1s. e.g.,  self._model.run(0.25)
        self._model.run()

    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
            
        # Now if you want to do different things for each state you can do it:
        if state == 0:
            # State 0 do/actions
            self._display.showText(str(self._player1.get_name())+" Your Turn \n" + str(self._player1) + " " + str(self._player2))
        elif state == 1:
            # State1 do/actions
            # You can check your sensors here and perform transitions manually if needed
            # For example, if you want to go from state 1 to state 2 when the motion sensor
            # is tripped you can do something like this
            # if self.motionsensor.tripped():
            # 	gotoState(2)
            self._index=0

            # State 0 do/actions
            self._display.reset()
            self._display.showText(str(self._max_length)+" to go   \n" +str(self._player1) + " " + str(self._player2))
            while self._index < self._max_length:
                if self._order[self._index] == 1: 
                    if self._button1.isPressed(): 
                        self._light1.blink()
                        self._index+=1
                    elif self._button2.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(2)
                elif self._order[self._index] == 2: 
                    time.sleep(1)
                    if self._button2.isPressed(): 
                        self._light2.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(2)
                elif self._order[self._index] == 3: 
                    if self._button3.isPressed(): 
                        self._light3.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(2)
                elif self._order[self._index] == 4: 
                    if self._button4.isPressed(): 
                        self._light4.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button2.isPressed() or self._button3.isPressed(): 
                        self._model.gotoState(2)
                else: 
                    print("error")
            self._player1.increase_score()
            self._display.showText("Sweet you Win")
            self._buzzer.beep(tone=250)
            self._max_length +=1
            self._model.gotoState(4)
        elif state ==2:
            self._display.showText("Press the Red Button to Steal, Button green not to")
            if self._button1.isPressed():
                self._model.gotoState(3)
            elif self._button2.isPressed():
                self._model.gotoState(3)
                
                

        elif state == 3 :
            self._display.showText(str(self._max_length)+" to go      \n" +str(self._player1) + " " + str(self._player2))
            self._index = 0 
            while self._index < self._max_length:
                if self._order[self._index] == 1: 
                    if self._button1.isPressed(): 
                        self._light1.blink()
                        self._index+=1
                    elif self._button2.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(4)
                elif self._order[self._index] == 2: 
                    if self._button2.isPressed(): 
                        self._light2.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(4)
                elif self._order[self._index] == 3: 
                    if self._button3.isPressed(): 
                        self._light3.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(4)
                elif self._order[self._index] == 4: 
                    if self._button4.isPressed(): 
                        self._light4.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button2.isPressed() or self._button3.isPressed(): 
                        self._model.gotoState(4)
                else: 
                    print("error")
            self._player2.increase_score()
            self._display.showText("Sweet you Win")
            self._buzzer.beep(tone=250)
            self._model.gotoState(4)

        elif state ==4:
            self._display.showText(str(self._player2.get_name())+" Your Turn    \n" + str(self._player1) + " " + str(self._player2))
        elif state == 5:
            self._display.reset()
            self._display.showText(str(self._max_length2)+" to go      \n" +str(self._player1) + " " + str(self._player2))
            self._index=0 
            while self._index < self._max_length2:
                if self._order[self._index] == 1: 
                    if self._button1.isPressed(): 
                        self._light1.blink()
                        self._index+=1
                    elif self._button2.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(6)
                elif self._order[self._index] == 2: 
                    if self._button2.isPressed(): 
                        self._light2.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(6)
                elif self._order[self._index] == 3: 
                    if self._button3.isPressed(): 
                        self._light3.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(6)
                elif self._order[self._index] == 4: 
                    if self._button4.isPressed(): 
                        self._light4.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button2.isPressed() or self._button3.isPressed(): 
                        self._model.gotoState(6)
                else: 
                    print("error")
            self._player2.increase_score()
            self._display.showText("Sweet you Win")
            self._buzzer.beep(tone=250)
            self._max_length2 +=1
            self._model.gotoState(0)
        elif state ==6: 
            self._display.showText("Press the Red Button to Steal, Button green not to")
        elif state == 7:
            self._display.reset()
            self._display.showText(str(self._max_length2)+" to go \n" +str(self._player1) + " " + str(self._player2))
            self._index=0 
            while self._index < self._max_length2:
                if self._order[self._index] == 1: 
                    if self._button1.isPressed(): 
                        self._light1.blink()
                        self._index+=1
                    elif self._button2.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(0)
                elif self._order[self._index] == 2: 
                    if self._button2.isPressed(): 
                        self._light2.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(0)
                elif self._order[self._index] == 3: 
                    if self._button3.isPressed(): 
                        self._light3.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button3.isPressed() or self._button4.isPressed(): 
                        self._model.gotoState(0)
                elif self._order[self._index] == 4: 
                    if self._button4.isPressed(): 
                        self._light4.blink()
                        self._index+=1
                    elif self._button1.isPressed() or self._button2.isPressed() or self._button3.isPressed(): 
                        self._model.gotoState(0)
                else: 
                    print("error")
            self._player1.increase_score()
            self._display.showText("Sweet you Win")
            self._buzzer.beep(tone=250)
            self._model.gotoState(0)
        elif state==8:
            if (self._player1.get_score() -self._player2.get_score()) == 2:
                self._display.showText("Player 1 WINSSSSS")
            else:
                self._display.showText("Player 2 WINSSSSS")





            
            
    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """
    def stateEntered(self, state, event):
        # Again if statements to do whatever entry/actions you need
        if state == 0:
            # entry actions for state 0
            if (self._player1.get_score() -self._player2.get_score()) == 2 or (self._player1.get_score() -self._player2.get_score()) == -2: 
                self._model.gotoState(8)
    
            
        
        elif state == 1:
            if self._max_length > self._max_length2 and self._player1.get_score()==self._player2.get_score(): 
                pass
            else:
                self._max_length=self._max_length2
            while len(self._order) < self._max_length:
                number = random.randint(1, 4) 
                self._order.append(number)  
            print(self._order)
            self._display.showText("Watch " + str(self._max_length)+" Blinks")
            for i in self._order:
                if i==1:
                    self._light1.blink()
                    print(self._order[i])
                elif i==2:
                    self._light2.blink()
                elif i==3:
                    self._light3.blink()
                elif i==4:
                    self._light4.blink()
                else:
                    print("error")
        elif state == 2: 
            print("state 2")
        elif state==4: 
            self._display.reset()
            if (self._player1.get_score() -self._player2.get_score()) == 2 or (self._player1.get_score() -self._player2.get_score()) == -2: 
                self._model.gotoState(8)
        elif state == 5:
            if self._max_length2 >2: 
                if self._max_length2 > self._max_length and self._player1.get_score()==self._player2.get_score(): 
                    pass
                else:
                    self._max_length2=self._max_length
            else:
                pass
            while len(self._order) < self._max_length2:
                number = random.randint(1, 4) 
                self._order.append(number)  
            print(self._order)
            self._display.showText("Watch " + str(self._max_length2)+" Blinks")
            for i in self._order:
                if i==1:
                    self._light1.blink()
                elif i==2:
                    self._light2.blink()
                elif i==3:
                    self._light3.blink()
                elif i==4:
                    self._light4.blink()
                else:
                    print("error")
        elif state == 6:
            pass

            


            
        
            
    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    
    This is just like stateEntered, perform only exit/actions here
    """

    def stateLeft(self, state, event):
        if state == 0:
            # State 0 do/actions
            self._display.reset()
        elif state == 1:
            pass
        elif state == 2 : 
            pass
        elif state == 4: 
            self._display.reset()
        elif state == 6:
            pass

        

    

# Test your model. Note that this only runs the template class above
# If you are using a separate main.py or other control script,
# you will run your model from there.
if __name__ == '__main__':
   GameController().run()