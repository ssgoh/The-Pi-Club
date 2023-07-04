from machine import Pin,PWM

class Robotcar:
    def __init__(self, enA, in1, in2, enB, in3, in4):
        self.left_motor_enA = PWM(Pin(enA))
        self.left_motor_forward_in1 = Pin(in1, Pin.OUT)
        self.left_motor_backward_in2 = Pin(in2, Pin.OUT)
        self.right_motor_enB = PWM(Pin(enB))
        self.right_motor_backward_in3 = Pin(in3, Pin.OUT)
        self.right_motor_forward_in4 = Pin(in4, Pin.OUT)
        self.stop()
    # Forward
    def move_forward(self):
        self.left_motor_forward_in1.on()    #left wheel forward
        self.left_motor_backward_in2.off()  #left wheel backward
        self.right_motor_backward_in3.off() #right wheel backward
        self.right_motor_forward_in4.on()   #right wheel forward
        
    # Backward
    def move_backward(self):
        self.left_motor_forward_in1.off()  #left wheel forward
        self.left_motor_backward_in2.on()  #left wheel backward
        self.right_motor_backward_in3.on() #right wheel backward
        self.right_motor_forward_in4.off() #right wheel forward
        
    #Turn Right
    def turn_right(self):
        self.left_motor_forward_in1.on()    #left wheel forward
        self.left_motor_backward_in2.off()  #left wheel backward
        self.right_motor_backward_in3.off() #right wheel backward
        self.right_motor_forward_in4.off()  #right wheel forward

    #Turn Left
    def turn_left(self):

        self.left_motor_forward_in1.off()   #left wheel forward
        self.left_motor_backward_in2.off()  #left wheel backward
        self.right_motor_backward_in3.off() #right wheel backward
        self.right_motor_forward_in4.on()   #right wheel forward

       
    #Stop
    def stop(self):
        self.left_motor_forward_in1.off()   #left wheel forward
        self.left_motor_backward_in2.off()  #left wheel backward
        self.right_motor_backward_in3.off() #right wheel backward
        self.right_motor_forward_in4.off()  #right wheel forward


