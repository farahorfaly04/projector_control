import paho.mqtt.client as mqtt
import serial

# Setup serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Define the MQTT callback
def on_message(client, userdata, message):
    command = str(message.payload.decode("utf-8"))
    if command == "ON":
        ser.write(b"\x7E\x30\x30\x30\x30\x30\x30\x30\x30\x0D")  # Example ON command
    elif command == "OFF":
        ser.write(b"\x7E\x30\x30\x30\x30\x30\x30\x30\x31\x0D")  # Example OFF command

# Setup MQTT client
client = mqtt.Client()
client.on_message = on_message
client.connect("10.205.3.196")  # Replace with your broker IP if needed

# Subscribe to the relevant topic
client.subscribe("home/projector/set")

# Start MQTT loop
client.loop_forever()
