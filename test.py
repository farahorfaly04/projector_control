import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)  
# Original ASCII string
ascii_string = "~0012 15\r"
ser.write(ascii_string.encode())