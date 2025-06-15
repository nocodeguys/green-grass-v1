import ujson
import time
import uasyncio as asyncio
import machine
from relay_control import run_zone
from utils import log

CONFIG_FILE = 'config.json'
RAIN_SENSOR_PIN = 16  # Use a valid GPIO pin for the rain sensor

# State for rain delay
rain_delay_active = False
rain_check_count = 0

schedule_data = {
    "schedule": []
}

def load_schedule():
    """Loads the schedule from config.json into memory."""
    global schedule_data
    try:
        with open(CONFIG_FILE, 'r') as f:
            schedule_data = ujson.load(f)
        log("Schedule loaded successfully from flash.")
    except (OSError, ValueError):
        log("Could not load schedule from flash, using empty schedule.")
        # If the file doesn't exist or is invalid, save the default
        save_schedule()

def save_schedule():
    """Saves the current schedule from memory to config.json."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            ujson.dump(schedule_data, f)
        log("Schedule saved successfully to flash.")
    except OSError:
        log("Error saving schedule to flash.")

def update_schedule(new_schedule_str):
    """
    Updates the schedule from an incoming MQTT message.
    :param new_schedule_str: (str) JSON string of the new schedule.
    """
    global schedule_data
    try:
        new_data = ujson.loads(new_schedule_str)
        if "schedule" in new_data and isinstance(new_data["schedule"], list):
            schedule_data = new_data
            save_schedule()
            log("Schedule updated and saved.")
        else:
            log("Invalid schedule format received.")
    except (ValueError, TypeError):
        log("Could not decode or parse new schedule JSON.")

def is_raining():
    """Checks the rain sensor. HIGH signal means it's raining."""
    rain_pin = machine.Pin(RAIN_SENSOR_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
    # The README specifies HIGH = rain.
    # A pull-down ensures it's low when dry.
    return rain_pin.value() == 1

async def schedule_checker():
    """The main async task that checks and runs the irrigation schedule."""
    global rain_delay_active, rain_check_count
    
    while True:
        now = time.localtime()
        current_hour = now[3]
        current_minute = now[4]

        # Rain sensor logic
        if is_raining():
            if not rain_delay_active:
                log("Rain detected! Delaying watering for 2 hours.")
                rain_delay_active = True
                rain_check_count = 0
            
            # This block will be entered if rain continues
            await asyncio.sleep(3600) # Wait for an hour before checking again
            rain_check_count += 1
            
            if rain_check_count >= 2:
                log("Rain continues. Skipping watering for today.")
                # Reset for the next day
                rain_delay_active = False
                rain_check_count = 0
                # Sleep until the next day
                await asyncio.sleep(22 * 3600) 
            continue # Re-evaluate from the top of the loop

        # If it was raining but has stopped
        if rain_delay_active and not is_raining():
            log("Rain has stopped. Resuming normal schedule.")
            rain_delay_active = False
            rain_check_count = 0

        # If a rain delay is active, don't run any schedules
        if rain_delay_active:
            await asyncio.sleep(60)
            continue

        # Check for scheduled runs
        for job in schedule_data.get('schedule', []):
            if job['hour'] == current_hour and job['minute'] == current_minute:
                log(f"Time match: Starting job for zone {job['zone']}.")
                await run_zone(job['zone'], job['duration'])
        
        # Check every 60 seconds
        await asyncio.sleep(60)

