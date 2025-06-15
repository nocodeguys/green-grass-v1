# 🛠️ Raspberry Pi Zero W - Setup Instructions

This guide explains how to set up the Raspberry Pi Zero W as the management unit for the irrigation system. It will run Home Assistant and a Mosquitto MQTT broker.

## 1. Operating System Setup

- **Install Raspberry Pi OS Lite.** Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash the OS onto your microSD card.
- **Enable SSH and configure Wi-Fi.** Before ejecting the SD card, create a file named `ssh` in the boot partition to enable SSH. Create another file named `wpa_supplicant.conf` with your Wi-Fi credentials:

  ```
  country=US
  ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
  update_config=1
  
  network={
       ssid="YOUR_WIFI_SSID"
       psk="YOUR_WIFI_PASSWORD"
  }
  ```
- **Boot and connect.** Insert the SD card into the Pi Zero, power it on, and find its IP address from your router's dashboard. Connect to it via SSH: `ssh pi@<IP_ADDRESS>`.

## 2. Install Mosquitto MQTT Broker

Mosquitto will handle communication between Home Assistant and the Pico.

```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install Mosquitto and the client tools
sudo apt install mosquitto mosquitto-clients -y

# Enable Mosquitto to start on boot
sudo systemctl enable mosquitto

# Create a user for the Pico
# You will be prompted for a password. Use the one from your Pico's secrets.py
sudo mosquitto_passwd -c /etc/mosquitto/passwd pico

# Apply the configuration
sudo cp ./mosquitto/mosquitto.conf /etc/mosquitto/conf.d/default.conf
sudo systemctl restart mosquitto
```

## 3. Install Home Assistant

We will use the official supervised installation method.

```bash
# Install dependencies
sudo apt-get install -y jq wget curl udisks2 libglib2.0-bin network-manager dbus

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install the OS Agent
wget https://github.com/home-assistant/os-agent/releases/latest/download/os-agent_1.2.2_linux_aarch64.deb
sudo dpkg -i os-agent_1.2.2_linux_aarch64.deb

# Install Home Assistant Supervised
wget https://github.com/home-assistant/supervised-installer/releases/latest/download/homeassistant-supervised.deb
sudo dpkg -i homeassistant-supervised.deb
```

## 4. Configure Home Assistant

- Access the Home Assistant frontend by navigating to `http://<IP_ADDRESS>:8123`.
- Complete the initial setup.
- **Copy the configuration files:** Transfer the contents of the `home-assistant/` directory from this repository into your Home Assistant configuration directory (usually `/usr/share/hassio/homeassistant`). You can do this via Samba, SCP, or by pasting the contents into the appropriate files using the File Editor add-on.
- **Restart Home Assistant.** Go to **Settings > System > Restart** to apply the new configuration. You should now see the Irrigation Control dashboard.