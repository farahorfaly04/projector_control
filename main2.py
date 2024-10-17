import paho.mqtt.client as mqtt
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)  

def format_command(base_command, value):
    """Format the command by inserting the parameter value in the appropriate place."""
    # Convert the value to hexadecimal
    value_hex = f"{value:X}".zfill(4)  # Convert to hex, padded to 4 characters
    return base_command.replace("XXXX", value_hex)

commands_dict = {
    # Static commands (no parameters)
    "HDMI1": b'\x7E\x30\x30\x31\x34\x30\x20\x34\x32\x0D',  # Hex code for HDMI1
    "HDMI2": b'\x7E\x30\x30\x31\x32\x20\x31\x35\x0D',  # Hex code for HDMI2
    "OFF": b'\x7E\x30\x30\x30\x30\x20\x30\x0D',  # Hex code for OFF
    "ON": b'\x7E\x30\x30\x30\x30\x20\x31\x0D',  # Hex code for ON

    "4:3": b'\x7E\x30\x30\x36\x30\x20\x31\x0D',  # Hex code for 4:3 aspect ratio
    "16:9": b'\x7E\x30\x30\x36\x30\x20\x32\x0D',  # Hex code for 16:9 aspect ratio

    "Up": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x30\x0D',    # Hex code for Remote Mouse Up
    "Left": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x31\x0D',  # Hex code for Remote Mouse Left
    "Enter": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x32\x0D', # Hex code for Remote Mouse Enter
    "Right": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x33\x0D', # Hex code for Remote Mouse Right
    "Down": b'\x7E\x30\x30\x31\x34\x30\x20\x31\x34\x0D',   # Hex code for Remote Mouse Down

    "Menu": b'\x7E\x30\x30\x31\x34\x30\x20\x32\x30\x0D', # Hex code for Menu
    "Back": b'\x7E\x30\x30\x31\x34\x30\x20\x37\x34\x0D', # Hex code for Back

    # Dynamic commands (require parameters)
    "Image-Shift-H": "\x7E\x30\x30\x35\x34\x30\x20XXXX\x0D",  # Placeholder for value
    "Image-Shift-V": "\x7E\x30\x30\x35\x34\x31\x20XXXX\x0D",  # Placeholder for value

    "H-Keystone": "\x7E\x30\x30\x36\x36\x20XXXX\x0D",  # Placeholder for value
    "V-Keystone": "\x7E\x30\x30\x36\x36\x20XXXX\x0D",  # Placeholder for value

    # Four Corners Adjustment
    "Top-left-H": "\x7E\x30\x30\x35\x38\x20XXXX\x0D",  # Placeholder for value
    "Top-left-V": "\x7E\x30\x30\x35\x38\x20XXXX\x0D",  # Placeholder for value
    "Top-right-H": "\x7E\x30\x30\x35\x39\x20XXXX\x0D",  # Placeholder for value
    "Top-right-V": "\x7E\x30\x30\x35\x39\x20XXXX\x0D",  # Placeholder for value
    "Bottom-left-H": "\x7E\x30\x30\x35\x38\x20XXXX\x0D",  # Placeholder for value
    "Bottom-left-V": "\x7E\x30\x30\x35\x38\x20XXXX\x0D",  # Placeholder for value
    "Bottom-right-H": "\x7E\x30\x30\x35\x39\x20XXXX\x0D",  # Placeholder for value
    "Bottom-right-V": "\x7E\x30\x30\x35\x39\x20XXXX\x0D",  # Placeholder for value
}

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscription successful with QoS: {granted_qos}")

def on_unsubscribe(client, userdata, mid):
    print("Successfully unsubscribed.")
    client.disconnect()

def on_message(client, userdata, msg):
    received_message = msg.payload.decode()
    print(f"Received message: {received_message} on topic: {msg.topic}")
    
    # Split the command and the parameter
    parts = received_message.split(" ")
    command = parts[0]
    param = int(parts[1]) if len(parts) > 1 else None

    if command in commands_dict:
        base_command = commands_dict[command]
        
        if "XXXX" in base_command:  # If this command expects a parameter
            if param is not None:
                formatted_command = format_command(base_command, param)
                ser.write(bytes.fromhex(formatted_command))
                print(f"Sent formatted command with parameter: {formatted_command}")
            else:
                print(f"No parameter provided for command: {command}")
        else:  # Commands that don't require parameters
            ser.write(base_command)
            print(f"Sent command: {base_command}")
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
