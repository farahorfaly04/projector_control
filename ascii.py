import paho.mqtt.client as mqtt
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)  

def format_command(base_command, value):
    """Format the command by inserting the parameter value in the appropriate place."""
    value_hex = f"{value:04X}"  # Convert to hex, padded to 4 characters
    return base_command.replace("n", value_hex)

commands_dict_ascii = {
    # Static commands (no parameters) 
    "HDMI1": "~00305 1\r", # HDMI1 
    "HDMI2": "~0012 15\r", # HDMI2
    "OFF": "~0000 0\r", # OFF
    "ON": "~0000 1\r", # ON

    "4:3": "~0060 1\r", # 4:3 aspect ratio
    "16:9": "~0060 2\r", # 16:9 aspect ratio

    "Up": "~00140 10\r",   # Remote Mouse Up
    "Left": "~00140 11\r", # Remote Mouse Left
    "Enter": "~00140 12\r", # Remote Mouse Enter
    "Right": "~00140 13\r", # Remote Mouse Right
    "Down": "~00140 14\r",  # Remote Mouse Down

    "Menu": "~00140 20\r", # Menu
    "Back": "~00140 74\r", # Back

    # Dynamic commands (require parameters n)
    "Image-Shift-H": "~0063 n\r", # horizontal image shift (-100 <= n <= 100)
    "Image-Shift-V": "~0064 n\r", # vertical image shift (-100 <= n <= 100)

    "Keystone-H": "~0065 n\r", # horizontal keystone (-40 <= n <= 40)
    "Keystone-V": "~0066 n\r", # vertical keystone (-40 <= n <= 40)

    # Four Corners Adjustment
    "Top-left-H": "~0058 n\r", # top-left corner horizontal (0)
    "Top-left-V": "~0058 n\r", # top-left corner vertical

    "Top-right-H": "~0059 n\r", # top-right corner horizontal
    "Top-right-V": "~0059 n\r", # top-right corner vertical

    "Bottom-left-H": "~0058 n\r", # bottom-left corner horizontal
    "Bottom-left-V": "~0058 n\r", # bottom-left corner vertical

    "Bottom-right-H": "~0059 n\r", # bottom-right corner horizontal
    "Bottom-right-V": "~0059 n\r", # bottom-right corner vertical
}

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscription successful with QoS: {granted_qos}")

def on_unsubscribe(client, userdata, mid):
    print("Successfully unsubscribed.")
    client.disconnect()

def on_message(client, userdata, msg):
    received_message = msg.payload.decode()
    print(f"Received message: {received_message} on topic: {msg.topic}")
    parts = received_message.split()
    if len(parts) == 2 and parts[1].isdigit():
        string_command = parts[0]
        n = parts[1]
        print(n)
    else:
        string_command = parts[0]

    if string_command in commands_dict_ascii:
        ascii_command = commands_dict_ascii[string_command]
        if "n" in ascii_command:
            ascii_command = ascii_command.replace("n", n)
        ser.write(ascii_command.encode('utf-8'))
        print(f"Sent {received_message} command: {ascii_command}")
    else:
        print(f"No command found for message: {string_command}")

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