import serial 
import time 


SerialObj = serial.Serial(port='COM3') 
SerialObj.baudrate = 9600  # set Baud rate to 9600
SerialObj.bytesize = 8   # Number of data bits = 8
SerialObj.parity  ='N'   # No parity
SerialObj.stopbits = 1   # Number of Stop bits = 1
time.sleep(3)
	

#SerialObj.write(b'<')    #transmit 'A' (8bit) to micro/Arduino
SerialObj.write(bytes('W','ascii'))    #transmit 'A' (8bit) to micro/Arduino
#SerialObj.write(b'>')    #transmit 'A' (8bit) to micro/Arduino
SerialObj.close()      # Close the port