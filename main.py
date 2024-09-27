import paho.mqtt.client as mqtt
import serial
import time

# Setup the serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust as necessary

# Define the MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("home/serial/command")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    if message == "ON":
        hex_command = b'\x01\x02\x03\x04'  # Replace with the specific hex code you need
        ser.write(hex_command)
        print("Hex command sent:", hex_command)

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.205.3.196", 1883, 60)  # Replace with your broker's address

# Blocking call - processes network traffic and dispatches callbacks
client.loop_forever()

