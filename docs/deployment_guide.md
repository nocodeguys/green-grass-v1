# Deployment Guide

This guide provides step-by-step instructions for deploying the Green Grass v1.0 irrigation system.

## Prerequisites

### Hardware Requirements
- Raspberry Pi Pico W
- Raspberry Pi Zero W with microSD card (8GB+)
- 4-channel relay module (5V or 3.3V compatible)
- Rain sensor module
- 24VAC irrigation solenoid valves
- Power supplies and connecting wires

### Software Requirements
- MicroPython firmware for Pico W
- Raspberry Pi OS Lite for Pi Zero W
- Thonny IDE or similar for Pico programming

## Step 1: Raspberry Pi Zero W Setup

### 1.1 Install Operating System
```bash
# Flash Raspberry Pi OS Lite to SD card
# Enable SSH and configure Wi-Fi before first boot
```

### 1.2 Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Mosquitto MQTT broker
sudo apt install mosquitto mosquitto-clients -y
sudo systemctl enable mosquitto

# Create MQTT user for Pico
sudo mosquitto_passwd -c /etc/mosquitto/passwd pico

# Copy mosquitto configuration
sudo cp pi-zero/mosquitto/mosquitto.conf /etc/mosquitto/conf.d/default.conf
sudo systemctl restart mosquitto
```

### 1.3 Install Home Assistant
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install OS Agent
wget https://github.com/home-assistant/os-agent/releases/latest/download/os-agent_1.2.2_linux_aarch64.deb
sudo dpkg -i os-agent_1.2.2_linux_aarch64.deb

# Install Home Assistant Supervised
wget https://github.com/home-assistant/supervised-installer/releases/latest/download/homeassistant-supervised.deb
sudo dpkg -i homeassistant-supervised.deb
```

### 1.4 Configure Home Assistant
1. Access Home Assistant at `http://<pi-zero-ip>:8123`
2. Complete initial setup
3. Copy configuration files from `pi-zero/home-assistant/` to `/usr/share/hassio/homeassistant/`
4. Restart Home Assistant

## Step 2: Raspberry Pi Pico W Setup

### 2.1 Install MicroPython
1. Download latest MicroPython firmware for Pico W
2. Hold BOOTSEL button while connecting USB
3. Copy firmware file to RPI-RP2 drive

### 2.2 Configure Credentials
1. Create `secrets.py` file with your credentials:
```python
WIFI_SSID = "your_wifi_network"
WIFI_PASSWORD = "your_wifi_password"
MQTT_BROKER = "192.168.1.100"  # Pi Zero IP address
MQTT_USER = "pico"
MQTT_PASSWORD = "your_mqtt_password"
```

### 2.3 Upload Code
1. Copy all files from `pico/` directory to Pico W
2. Ensure `main.py` runs on startup

## Step 3: Hardware Connections

### 3.1 Relay Module
Connect relay module to Pico W:
- VCC → 3V3 (or 5V if using 5V relay module)
- GND → GND
- IN1 → GPIO 2 (Zone 1)
- IN2 → GPIO 3 (Zone 2)
- IN3 → GPIO 4 (Zone 3)
- IN4 → GPIO 5 (Zone 4)

### 3.2 Rain Sensor
Connect rain sensor to Pico W:
- VCC → 3V3
- GND → GND
- DO → GPIO 16

### 3.3 Irrigation Valves
Connect 24VAC solenoid valves through relay module:
- Common wire to 24VAC transformer
- Individual zone wires through relay NO contacts
- Ensure proper electrical safety measures

## Step 4: System Testing

### 4.1 Basic Functionality
1. Power on Pi Zero W and verify Home Assistant access
2. Power on Pico W and check for connection in logs
3. Verify MQTT communication in Home Assistant

### 4.2 Hardware Testing
1. Test each irrigation zone manually via Home Assistant
2. Verify rain sensor functionality
3. Check schedule execution

### 4.3 Integration Testing
1. Set up test irrigation schedule
2. Verify rain delay functionality
3. Test offline operation by disconnecting Wi-Fi

## Step 5: Configuration

### 5.1 Customize Settings
Edit `pico/config.py` to adjust:
- GPIO pin assignments
- Timing intervals
- System limits

### 5.2 Schedule Setup
Use Home Assistant interface to:
- Configure irrigation zones
- Set watering schedules
- Monitor system status

## Troubleshooting

### Common Issues

**Pico W won't connect to Wi-Fi**
- Check credentials in `secrets.py`
- Verify Wi-Fi network availability
- Check for special characters in password

**MQTT connection fails**
- Verify Pi Zero W IP address
- Check Mosquitto service status: `sudo systemctl status mosquitto`
- Verify MQTT credentials

**Relays don't activate**
- Check GPIO pin connections
- Verify relay module voltage requirements
- Test relay module independently

**Rain sensor not working**
- Check sensor connections
- Verify sensor type (digital/analog)
- Test sensor with multimeter

### Log Analysis
- Check Pico W logs via USB connection
- Monitor Home Assistant logs for MQTT messages
- Review Mosquitto logs: `sudo tail -f /var/log/mosquitto/mosquitto.log`

## Maintenance

### Regular Tasks
- Check system logs weekly
- Verify irrigation zone functionality monthly
- Update software components quarterly
- Clean rain sensor seasonally

### Backup Procedures
- Export Home Assistant configuration
- Backup Pico W configuration files
- Document any custom modifications 