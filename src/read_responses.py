import serial
import time

def read_all_responses():
    # Setup serial connection
    ser = serial.Serial(
        port='/dev/ttyUSB0',  # Replace with your actual port
        baudrate=19200,       # Baud rate as per projector settings
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1             # Set a timeout (1 second)
    )
    
    # Make sure the serial connection is open
    if ser.isOpen():
        print("Serial port opened successfully.")

    # Empty buffer to store all responses
    responses = []

    try:
        # Keep reading while there is data available
        while True:
            if ser.in_waiting > 0:
                # Read the response from the serial buffer
                response = ser.read(ser.in_waiting).decode('ascii', errors='ignore')
                
                if response:
                    print(f"Response received: {response}")
                    responses.append(response)
            
            # Sleep for a short time to allow more data to arrive
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        # If interrupted, exit the loop gracefully
        print("\nStopped reading responses.")
        
    finally:
        # Close the serial connection
        ser.close()
        print("Serial port closed.")
    
    return responses

# Example usage
all_responses = read_all_responses()

# Print the captured responses
for idx, response in enumerate(all_responses):
    print(f"Response {idx + 1}: {response}")
