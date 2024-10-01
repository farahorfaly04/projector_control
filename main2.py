import paho.mqtt.client as mqtt
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)  

commands_dict = {
    "HDMI1": b'\x7E\x30\x30\x31\x32\x20\x31\x0D',  # Hex code for HDMI1
    "HDMI2": b'\x7E\x30\x30\x31\x32\x20\x31\x35\x0D',  # Hex code for HDMI2
    "OFF": b'\x7E\x30\x30\x30\x30\x20\x30\x0D',  # Hex code for OFF
    "ON": b'\x7E\x30\x30\x30\x30\x20\x31\x0D',  # Hex code for ON

    "4:3": b'\x7E\x30\x30\x36\x30\x20\x31\x20\x0D',  # Hex code for 4:3 aspect ratio
    "16:9": b'\x7E\x30\x30\x36\x30\x20\x32\x20\x0D',  # Hex code for 16:9 aspect ratio
    "16:10": b'\x7E\x30\x30\x36\x30\x20\x33\x20\x0D',  # Hex code for 16:10 aspect ratio
    "Native": b'\x7E\x30\x30\x36\x30\x20\x36\x20\x0D',  # Hex code for Native aspect ratio
    "Auto": b'\x7E\x30\x30\x36\x30\x20\x39\x20\x0D',  # Hex code for Auto aspect ratio

    "Remote Mouse Up": b'\x7E\x30\x30\x31\x34\x30\x20\x33\x0D',    # Hex code for Remote Mouse Up
    "Remote Mouse Left": b'\x7E\x30\x30\x31\x34\x30\x20\x34\x0D',  # Hex code for Remote Mouse Left
    "Remote Mouse Enter": b'\x7E\x30\x30\x31\x34\x30\x20\x35\x0D', # Hex code for Remote Mouse Enter
    "Remote Mouse Right": b'\x7E\x30\x30\x31\x34\x30\x20\x36\x0D', # Hex code for Remote Mouse Right
    "Remote Mouse Down": b'\x7E\x30\x30\x31\x34\x30\x20\x37\x0D'   # Hex code for Remote Mouse Down
}

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscription successful with QoS: {granted_qos}")

def on_unsubscribe(client, userdata, mid):
    print("Successfully unsubscribed.")
    client.disconnect()

def on_message(client, userdata, msg):
    received_message = msg.payload.decode()
    print(f"Received message: {received_message} on topic: {msg.topic}")
    
    if received_message in commands_dict:
        hex_command = commands_dict[received_message]
        ser.write(hex_command)
        print(f"Sent hex command: {hex_command}")
    else:
        print(f"No command found for message: {received_message}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully.")
        client.subscribe("home/serial/command")
    else:
        print(f"Failed to connect, error code: {rc}")

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

mqttc.username_pw_set("mqtt", "123456789") 
mqttc.connect("10.205.3.196", 1883, 60)  
mqttc.loop_forever()
