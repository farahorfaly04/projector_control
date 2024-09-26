
import serial
import time

def send_hex_command_and_check_response(hex_command):
    # Convert the hex string input to bytes
    byte_command = bytearray.fromhex(hex_command)
    
    # Setup serial connection
    ser = serial.Serial(
        port='/dev/ttyUSB0',  # Replace with your actual port
        baudrate=19200,       # Based on projector settings
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    
    # Send the byte command to the projector
    ser.write(byte_command)
        
    # Read and print the response from the projector (if any)
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting).decode('ascii', errors='ignore')
        print(f"Response: {response}")
    else:
        print("No response from the projector.")
    
    # Close the serial connection
    ser.close()

if __name__ == "__main__":
    # Take the hex input from the user in the terminal
    user_command = input("Enter the RS232 command in hex format (e.g., '7E 30 30 33 39 20 31 0D'): ")
    
    # Send the hex command and check the response
    send_hex_command_and_check_response(user_command)

