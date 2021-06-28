from serial import Serial
import time

#change to serial port for your raspberry pi pico
#you can check that in Arduino IDE
SERIALPORT ='/dev/cu.usbserial-1410'
#change to your Gcode path
FilePath = '/Users/nikodembartnik/Desktop/rocket.gcode'
ploter = Serial(SERIALPORT, 115200, timeout=0.01)

#simple method that waits until there is OK detected on the serial port
def WaitForOK():
    while(1):
        if(ploter.readline() == b'OK\n'):
            break

#next 3 lines are just for calculating file length
#so that we can calculate the progress
fileLength = 0
for line in open(FilePath):
    fileLength+=1


#sending Gcode line by line and printing progress on every change.
commandNumber = 0
for line in open(FilePath):
    ploter.write(line.encode('UTF-8'))
    commandNumber+=1
    if commandNumber % int(fileLength/100) == 0:
        print(str(int(commandNumber*100/fileLength)) + "% ready...")
    WaitForOK()
