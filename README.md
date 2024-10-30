# Projector Control with Home Assistant and MQTT

This project integrates the Optoma UHD35STx projector with Home Assistant, enabling control via RS232 commands sent over MQTT. The setup allows for projector commands such as power on/off, input selection, keystone adjustments, and image shifting through a Home Assistant dashboard. A Raspberry Pi runs an MQTT broker that connects with the projector via its RS232 port.

## Home Assistant Dashboard Layout

Below is an example screenshot of the Home Assistant dashboard layout for projector control:

![Home Assistant Dashboard Layout](dashboard.png)

## Features

- **Power Control**: Turn the projector on or off.
- **Input Selection**: Choose between HDMI1, HDMI2, etc.
- **Aspect Ratio Adjustment**: Switch between 4:3 and 16:9.
- **Keystone and Image Shift**: Adjust keystone and image alignment.
- **Remote Control Layout**: Navigation controls (up, down, left, right, enter, and menu).

## Files Overview

- `ascii.py`: Python script for listening to MQTT messages and sending RS232 commands to the projector.
- `read_responses.py`: This Python script establishes an RS232 connection with the projector, continuously reads all available responses, and prints them to the console. It’s useful for debugging and verifying the commands received by the projector.
- `automations.yml`: Defines automations in Home Assistant to listen for input changes and trigger MQTT messages.
- `configuration.yml`: Sets up Home Assistant entities for projector control (input selectors, sliders).
- `dashboard.yml`: Configures Home Assistant dashboard buttons for projector control.
- `requirements.txt`: Lists required Python packages.

## Hardware Requirements

- Optoma UHD35STx Projector
- Raspberry Pi connected to the projector's RS232 port via a USB-to-serial adapter
- Home Assistant instance with MQTT integration

## Installation

### 1. Create a User in Home Assistant
   - Go to *Settings > People & Zones > Users*.
   - Create a new user for the MQTT broker, assigning a username and password that will later be used for MQTT configuration.
  
### 2. Set up the MQTT Broker
   - **Install the MQTT Add-on in Home Assistant**:
     - Go to *Settings > Add-ons > Add-on Store*.
     - Install the *Mosquitto broker*.
     - Go to *Configuration* and set the username and password created in the previous step.

### 3. Set Up Python Environment on Raspberry Pi
   - Clone the repository and navigate to it:
     ```bash
     git clone https://github.com/IE-Robotics-Lab/optoma_projector_control.git
     cd optoma_projector_control
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

### 4. Configure `ascii.py`
   - The `ascii.py` script listens for MQTT messages on the topic `home/serial/command` and sends the corresponding RS232 command to the projector.
   - Ensure the script points to the correct serial port for RS232 communication:
     ```python
     serial_port = '/dev/ttyUSB0'  # Update if your serial device differs
     baud_rate = 9600  # As per projector manual
     ```

### 5. Set Up Home Assistant Configuration Files
   - Add entries from `configuration.yml` and `automations.yml` to their corresponding files in Home Assistant.

### 6. Dashboard Configuration
   - `dashboard.yml` creates interactive buttons in the Home Assistant interface, including:
     - Power controls
     - Directional controls for menu navigation
     - Input selection and aspect ratio adjustments
     - Keystone and image shift adjustments
   - Add the content from `dashboard.yml` to your Home Assistant dashboard configuration.
   - Each type can have its own card on the dashboard.

### 7. Run `ascii.py` as a Systemd Service

To keep `ascii.py` running in the background and automatically restart it if it fails, set it up as a systemd service.

1. Create a new service file:
   ```bash
   sudo nano /etc/systemd/system/mqtt_serial.service
   ```

2.	Add the following content to mqtt_serial.service:
    ```ini
    [Unit]
    Description=MQTT Serial Command Listener for Projector Control
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /projector_control/ascii.py
    WorkingDirectory=/projector_control
    Restart=always
    User=pi
    Environment=PYTHONUNBUFFERED=1

    [Install]
    WantedBy=multi-user.target
    ```

3.	Save and close the file.
4.	Enable and start the service:
    ```bash
    sudo systemctl enable mqtt_serial.service
    sudo systemctl start mqtt_serial.service
    ```
5. Check the status to make its running
    ```bash
    sudo systemctl status mqtt_serial.service
    ```
6. View the logs to make sure the rasberry pi is receiving the commands
    ```bash
    journalctl -u mqtt_serial.service -f
    ```

### Ressources 
- [Optoma Projectors RS232 Commands List](./RS232_function_list.pdf)


Enjoy seamless control of your Optoma projector through Home Assistant!