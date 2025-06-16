# Configuration constants for the irrigation system

# Hardware Configuration
RELAY_PINS = {
    1: 2,  # Zone 1 -> GPIO 2
    2: 3,  # Zone 2 -> GPIO 3
    3: 4,  # Zone 3 -> GPIO 4
    4: 5,  # Zone 4 -> GPIO 5
}

RAIN_SENSOR_PIN = 16  # GPIO pin for rain sensor

# Timing Configuration
RAIN_CHECK_INTERVAL = 3600  # 1 hour in seconds
MAX_RAIN_CHECKS = 2  # Maximum rain checks before skipping the day
SCHEDULE_CHECK_INTERVAL = 60  # Check schedule every 60 seconds
STATUS_PUBLISH_INTERVAL = 300  # Publish status every 5 minutes
MQTT_CHECK_INTERVAL = 1  # Check MQTT messages every second

# File Configuration
CONFIG_FILE = 'config.json'

# MQTT Topics
SCHEDULE_SET_TOPIC = "pico/schedule/set"
MANUAL_RUN_TOPIC = "pico/irrigation/manual"
STATUS_TOPIC = "pico/status"

# System Limits
MIN_DURATION = 1  # Minimum irrigation duration in minutes
MAX_DURATION = 60  # Maximum irrigation duration in minutes
MIN_ZONE = 1  # Minimum zone number
MAX_ZONE = 4  # Maximum zone number 