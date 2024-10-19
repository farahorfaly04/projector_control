import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)  
# Original ASCII string
ascii_string = "~00518 1\r"
ser.write(ascii_string.encode())