import network
import time
import uasyncio as asyncio

import secrets
from utils import sync_time, log
from relay_control import setup_relays, all_relays_off
from schedule import load_schedule, schedule_checker
from mqtt import connect_and_subscribe, mqtt_listener, periodic_status_publisher

def connect_wifi():
    """Connects the Pico to Wi-Fi."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        log("Waiting for Wi-Fi connection...")
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('Wi-Fi connection failed')
    else:
        log('Connected to Wi-Fi')
        status = wlan.ifconfig()
        log(f'IP Address: {status[0]}')

async def main():
    """Main function to initialize and run the system."""
    log("--- Starting Irrigation System ---")

    try:
        connect_wifi()
        
        # It's critical to have the correct time for the schedule
        if not sync_time():
             # If NTP fails, the system can still run with the last known time,
             # but it might be inaccurate. A reboot could be forced here if needed.
            log("Warning: Failed to sync time. Schedule might be inaccurate.")

        # Initialize hardware and load data
        setup_relays()
        load_schedule()

        # Connect to MQTT broker
        mqtt_client = connect_and_subscribe()
        
        if not mqtt_client:
            log("CRITICAL: Could not connect to MQTT. System will run in offline mode.")
            # Even if MQTT fails, the schedule checker can run with the stored schedule
        
        # Create and run async tasks
        log("Starting async tasks...")
        
        # Task for running scheduled jobs
        asyncio.create_task(schedule_checker())
        
        # Tasks for MQTT communication (only if connected)
        if mqtt_client:
            asyncio.create_task(mqtt_listener())
            asyncio.create_task(periodic_status_publisher())

        # Keep the main loop running to let async tasks execute
        while True:
            await asyncio.sleep(10)

    except Exception as e:
        log(f"An unexpected error occurred in main: {e}")
        log("Resetting all relays and attempting to reboot in 30 seconds...")
        all_relays_off()
        time.sleep(30)
        machine.reset()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Program stopped by user.")
        all_relays_off()
    except Exception as e:
        log(f"Fatal error, rebooting. Error: {e}")
        all_relays_off()
        time.sleep(10)
        machine.reset()
