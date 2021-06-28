import utime
from machine import Pin, UART, PWM
uart = machine.UART(1, 115200)

#constants
STEPSPERMM = 80
MMPERSTEP = 1/STEPSPERMM
DIR_A = 0
STEP_A = 1
nENABLE_A = 2
STEP_DELAY = 20

DIR_B = 6
STEP_B = 7
nENABLE_B = 8

DIR_C = 10
STEP_C = 11
nENABLE_C = 12

SERVO_PIN = 21

x_step_pos = 0
y_step_pos = 0

#variables just for testing


dir_A = Pin(DIR_A, Pin.OUT)
step_A = Pin(STEP_A, Pin.OUT)
nenable_A = Pin(nENABLE_A, Pin. OUT)

dir_B = Pin(DIR_B, Pin.OUT)
step_B = Pin(STEP_B, Pin.OUT)
nenable_B = Pin(nENABLE_B, Pin. OUT)

servo = None

def EnableMotors():
    nenable_A.value(0)
    nenable_B.value(0)
    

def DisableMotors():
    nenable_A.value(1)
    nenable_B.value(1)
    

#a = 0 move A, a = 1 move B
def OneStep(a, direction):
    if a == 0:
        dir_A.value(direction)
        step_A.value(0)
        step_A.value(1)
    elif a == 1:
        dir_B.value(direction)
        step_B.value(0)
        step_B.value(1)
        
    

#To move to (X, Y) we need to calculate dA = dX + dY and dB = dX - dY
def MoveToPosition(x, y):
    global x_step_pos
    global y_step_pos
    #x and y steps to do, different than a and b steps to do
    x = x/MMPERSTEP
    y = y/MMPERSTEP
    x_steps_to_do = round(x) - x_step_pos
    y_steps_to_do = round(y) - y_step_pos
    a_steps_to_do = x_steps_to_do + y_steps_to_do
    b_steps_to_do = x_steps_to_do - y_steps_to_do
    x_step_pos = x
    y_step_pos = y
    
    #deciding on which way the motors should spin
    directionA = 0 if a_steps_to_do > 0 else 1
    directionB = 0 if b_steps_to_do > 0 else 1
    
    #after obatining the direction we can convert to absolute values for simplicity
    a_steps_to_do = abs(a_steps_to_do)
    b_steps_to_do = abs(b_steps_to_do)

    #here we will store the error for the axis with sliced movement
    if a_steps_to_do == b_steps_to_do:
        for i in range(a_steps_to_do):
            OneStep(0, directionA)
            OneStep(1, directionB)
            StepsDelay()
        
    else:
        sliced_axis_error = 0;
        sliced_axis_increment = b_steps_to_do/a_steps_to_do if a_steps_to_do > b_steps_to_do else a_steps_to_do/b_steps_to_do
        
        if a_steps_to_do > b_steps_to_do:
            for i in range(a_steps_to_do):
                OneStep(0, directionA)
                sliced_axis_error += sliced_axis_increment
                if sliced_axis_error >= 1:
                    OneStep(1, directionB)
                    sliced_axis_error -= 1
                StepsDelay()
            
        elif a_steps_to_do < b_steps_to_do:
            for i in range(b_steps_to_do):
                OneStep(1, directionB)
                sliced_axis_error += sliced_axis_increment
                if sliced_axis_error >= 1:
                    OneStep(0, directionA)
                    sliced_axis_error -= 1
                StepsDelay()
    
    
    
def StepsDelay():
    utime.sleep_us(STEP_DELAY)
    
    
def UartRead():
    return uart.readline()


def UartSendOK():
    uart.write('OK\n')
    

def ProcessGcode(inputLine):
    UartSendOK()
    #dictionary with variables to return
    toReturn = {}
    inputLine = inputLine.strip('\n\r')
    inputLine = inputLine.split(';', 1)[0]
    print(inputLine)
    if len(inputLine) > 0:
        gcode = inputLine.split(' ')
        for command in gcode:
            if command[0] == 'X':
                #do things with X
                toReturn['X'] = command[1:]
            elif command[0] == 'Y':
                #do things with Y
                toReturn['Y'] = command[1:]
            elif command[0] == 'Z':
                #do things with Z
                toReturn['Z'] = command[1:]
            elif command[0] == 'F':
                #do things with F
                toReturn['F'] = command[1:]
            elif command[0] == 'G':
                #do things with G
                toReturn['G'] = command[1:]
    return toReturn


def ExecuteGcode(commands):
    global x_step_pos
    global y_step_pos
    global STEP_DELAY
    if 'F' in commands:        
        STEP_DELAY = int(5000 - 5*int(commands['F']))
        if STEP_DELAY < 20: STEP_DELAY = 20
        print("New step delay: " + str(STEP_DELAY))
    if 'Z' in commands:
        ServoWrite(0 if float(commands['Z']) > 0.1 else 30)
    if 'X' in commands or 'Y' in commands:
        MoveToPosition(float(commands['X']) if 'X' in commands else x_step_pos*MMPERSTEP, float(commands['Y']) if 'Y' in commands else y_step_pos*MMPERSTEP)
    if 'G' in commands:
        if(commands['G'] == '28'):
            x_step_pos = 0
            y_step_pos = 0
    
                
def ServoWrite(angle):
    servo.duty_ns(int((angle/180)*1000000+700000))
    utime.sleep_ms(100)


def ServoInit():
    global servo
    servo = PWM(Pin(21))
    servo.freq(50)
    servo.duty_ns(700000)
    
    
EnableMotors()
ServoInit()
while(1):
    ExecuteGcode(ProcessGcode(str(UartRead(), "utf-8")))
    