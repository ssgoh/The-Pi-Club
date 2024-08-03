from machine import Pin,PWM

class robotcar:
    def __init__(self, enA, in1, in2, in3, in4, enB):
        self.enA = PWM(Pin(enA))
        self.in1 = Pin(in1, Pin.OUT)
        self.in2 = Pin(in2, Pin.OUT)
        self.enB = PWM(Pin(enB))
        self.in3 = Pin(in3, Pin.OUT)
        self.in4 = Pin(in4, Pin.OUT)
        #self.stop()
    
    def LW_forward(self):
        self.in1.on()
        self.in2.off()
    
    def LW_backward(self):
        self.in1.off()
        self.in2.on()
        
        
    def RW_forward(self):
        self.in3.off()
        self.in4.on()
        
    def RW_backward(self):
        self.in3.on()
        self.in4.off()
        


        
    def LW_stop(self):
        self.in1.off()
        self.in2.off()        
        
    def RW_stop(self):
        self.in3.off()
        self.in4.off()        
        
    # Forward
    def move_forward(self):
        self.RW_forward()    #left wheel forward
        self.LW_forward()  #left wheel backward
    # Backward
    def move_backward(self):
        self.RW_backward()
        self.LW_backward() #left wheel backward
    #Turn Right
    def turn_right(self):
        self.LW_forward()    
        self.RW_stop()   


   #Turn Left
    def turn_left(self):
        self.RW_forward()  
        self.LW_stop()   
         
    #Stop
    def stop(self):
        self.RW_stop()   #left wheel forward
        self.LW_stop()  #left wheel backward
        

 
