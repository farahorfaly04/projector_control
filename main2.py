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

commands_dict_hex = {
    # Static commands (no parameters)
    "HDMI1": b'\x7E\x30\x30\x31\x34\x30\x20\x34\x32\x0D', # HDMI1
    "HDMI2": b'\x7E\x30\x30\x31\x32\x20\x31\x35\x0D', # HDMI2

    "OFF": b'\x7E\x30\x30\x30\x30\x20\x30\x0D', # OFF
    "ON": b'\x7E\x30\x30\x30\x30\x20\x31\x0D', # ON

    "4:3": b'\x7E\x30\x30\x36\x30\x20\x31\x0D', # 4:3 aspect ratio
    "16:9": b'\x7E\x30\x30\x36\x30\x20\x32\x0D', # 16:9 aspect ratio

    "Up": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x30\x0D', # Remote Mouse Up
    "Left": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x31\x0D', # Remote Mouse Left
    "Enter": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x32\x0D', # Remote Mouse Enter
    "Right": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x33\x0D', # Remote Mouse Right
    "Down": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x34\x0D', # Remote Mouse Down

    "Menu": b'\x7E\x30\x30\x31\x34\x30\x20\x32\x30\x0D', # Menu
    "Back": b'\x7E\x30\x30\x31\x34\x30\x20\x37\x34\x0D', # Back

    # Dynamic commands (require parameters)
    "Image-Shift-H": "\x7E\x30\x30\x35\x34\x30\x20n\x0D", # horizontal image shift
    "Image-Shift-V": "\x7E\x30\x30\x35\x34\x31\x20n\x0D", # vertical image shift

    "H-Keystone": "\x7E\x30\x30\x36\x36\x20n\x0D", # horizontal keystone
    "V-Keystone": "\x7E\x30\x30\x36\x36\x20n\x0D", # vertical keystone

    # Four Corners Adjustment
    "Top-left-H": "\x7E\x30\x30\x35\x38\x20n\x0D", # top-left corner horizontal
    "Top-left-V": "\x7E\x30\x30\x35\x38\x20n\x0D", # top-left corner vertical
    "Top-right-H": "\x7E\x30\x30\x35\x39\x20n\x0D", # top-right corner horizontal
    "Top-right-V": "\x7E\x30\x30\x35\x39\x20n\x0D", # top-right corner vertical
    "Bottom-left-H": "\x7E\x30\x30\x35\x38\x20n\x0D", # bottom-left corner horizontal
    "Bottom-left-V": "\x7E\x30\x30\x35\x38\x20n\x0D", # bottom-left corner vertical
    "Bottom-right-H": "\x7E\x30\x30\x35\x39\x20n\x0D", # bottom-right corner horizontal
    "Bottom-right-V": "\x7E\x30\x30\x35\x39\x20n\x0D", # bottom-right corner vertical
}

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscription successful with QoS: {granted_qos}")

def on_unsubscribe(client, userdata, mid):
    print("Successfully unsubscribed.")
    client.disconnect()

def on_message(client, userdata, msg):
    received_message = msg.payload.decode()
    print(f"Received message: {received_message} on topic: {msg.topic}")
    
    if received_message[0] in commands_dict_ascii:
        ascii_command = commands_dict_ascii[received_message[0]]
        if "n" in ascii_command:
            n = received_message[1]
            ascii_command.replace("n", n)
        ser.write(ascii_command.encode('utf-8'))
        print(f"Sent {received_message} command: {ascii_command}")
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
