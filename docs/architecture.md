# System Architecture

This document describes the technical architecture of the Green Grass v1.0 irrigation system.

## Overview

The system consists of two main components:
- **Raspberry Pi Pico W**: Control unit for irrigation scheduling and hardware control
- **Raspberry Pi Zero W**: Management unit running Home Assistant and MQTT broker

## Component Architecture

### Raspberry Pi Pico W (Control Unit)

#### Hardware Connections
- **GPIO 2-5**: Relay control outputs for irrigation zones 1-4
- **GPIO 16**: Rain sensor input (HIGH = rain detected)
- **Wi-Fi**: 802.11n connectivity for MQTT communication

#### Software Components

##### Core Modules
- **main.py**: System initialization and main event loop
- **config.py**: Centralized configuration constants
- **utils.py**: Utility functions including logging and validation

##### Functional Modules
- **mqtt.py**: MQTT client implementation for communication
- **schedule.py**: Irrigation scheduling logic with rain detection
- **relay_control.py**: Hardware control for irrigation valves
- **secrets.py**: Configuration file for credentials (not in version control)

##### Data Flow
1. System boots and connects to Wi-Fi
2. Time synchronization via NTP
3. Load irrigation schedule from flash storage
4. Connect to MQTT broker
5. Start async tasks:
   - Schedule checker (every 60 seconds)
   - MQTT message listener
   - Status publisher (every 5 minutes)

### Raspberry Pi Zero W (Management Unit)

#### Services
- **Home Assistant**: Web-based management interface
- **Mosquitto MQTT Broker**: Message broker for Pico communication
- **Docker**: Container runtime for Home Assistant

#### Data Flow
1. User configures irrigation schedule via Home Assistant UI
2. Home Assistant publishes schedule to MQTT topic `pico/schedule/set`
3. Pico receives and validates schedule
4. Pico saves schedule to local flash storage
5. Pico publishes status updates to `pico/status`

## Communication Protocol

### MQTT Topics

| Topic | Direction | Purpose | Payload Format |
|-------|-----------|---------|----------------|
| `pico/schedule/set` | HA → Pico | Update irrigation schedule | JSON schedule object |
| `pico/irrigation/manual` | HA → Pico | Manual zone control | `{"zone": 1, "duration": 10}` |
| `pico/status` | Pico → HA | System status updates | `{"status": "message", "timestamp": epoch}` |

### Schedule Data Format
```json
{
  "schedule": [
    {
      "zone": 1,
      "hour": 6,
      "minute": 0,
      "duration": 10
    }
  ]
}
```

## Fault Tolerance

### Offline Operation
- Pico stores schedule in flash memory
- System continues operation if MQTT connection fails
- Automatic MQTT reconnection with exponential backoff

### Rain Detection
- Delays irrigation by 2 hours when rain detected
- Checks every hour for up to 2 hours
- Skips to next day if rain continues

### Hardware Safety
- All relays turn OFF on system error
- System reset on critical failures
- Input validation on all external data

## Configuration Management

All system constants are centralized in `config.py`:
- GPIO pin assignments
- Timing intervals
- MQTT topics
- System limits and validation rules

This allows easy customization without modifying core logic.