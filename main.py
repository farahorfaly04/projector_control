import serial
import paho.mqtt.client as mqtt

# Setup the serial connection to the projector
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)  # Adjust serial port and baud rate if necessary

# Command to Hex Code Mapping (Replace with your projector's actual hex codes)
command_map = {
    "on": b'\x7E\x30\x30\x30\x20\x31\x20\x30\x31\x0D',   # Example hex code for "Power On"
    "off": b'\x7E\x30\x30\x30\x20\x31\x20\x30\x30\x0D',  # Example hex code for "Power Off"
    "up": b'\x7E\x30\x30\x30\x20\x32\x20\x30\x35\x0D',   # Example hex code for "Volume Up"
    "down": b'\x7E\x30\x30\x30\x20\x32\x20\x30\x36\x0D'  # Example hex code for "Volume Down"
}

def send_command(command):
    """Send a command to the projector via RS232."""
    if command in command_map:
        try:
            hex_command = command_map[command]
            ser.write(hex_command)  # Send the command in hex format
            response = ser.read(64)  # Read up to 64 bytes of response
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error sending command: {e}")
    else:
        print(f"Unknown command: {command}")

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    """Callback when the client connects to the MQTT broker."""
    if rc == 0:
        print("Connected to MQTT Broker")
        # Subscribe to the desired topic on successful connection
        client.subscribe("homeassistant/projector/control")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """Callback when a message is received on a subscribed topic."""
    command = msg.payload.decode().lower()  # Decode the message and convert to lowercase
    print(f"Received command: {command}")
    send_command(command)  # Send the received command to the projector

# Setup MQTT client
mqtt_client = mqtt.Client()

# Attach callbacks
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker (adjust IP address/port if necessary)
mqtt_client.connect("10.205.3.196", 1883, 60)

# Start the MQTT client loop in a non-blocking manner
mqtt_client.loop_start()

print("Projector control service is running...")

# Keep the script running indefinitely
try:
    while True:
        pass  # This keeps the script alive
except KeyboardInterrupt:
    print("Shutting down...")

# Close the serial connection when the script exits
ser.close()
