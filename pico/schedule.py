import ujson
import time
import uasyncio as asyncio
import machine
from relay_control import run_zone
from utils import log, validate_schedule_data
from config import (
    CONFIG_FILE, RAIN_SENSOR_PIN, RAIN_CHECK_INTERVAL, 
    MAX_RAIN_CHECKS, SCHEDULE_CHECK_INTERVAL
)

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
            loaded_data = ujson.load(f)
        
        if validate_schedule_data(loaded_data):
            schedule_data = loaded_data
            log("Schedule loaded successfully from flash.")
        else:
            log("Invalid schedule data in config file, using default schedule.")
            save_schedule()
    except (OSError, ValueError) as e:
        log(f"Could not load schedule from flash: {e}. Using empty schedule.")
        # If the file doesn't exist or is invalid, save the default
        save_schedule()

def save_schedule():
    """Saves the current schedule from memory to config.json."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            ujson.dump(schedule_data, f)
        log("Schedule saved successfully to flash.")
    except OSError as e:
        log(f"Error saving schedule to flash: {e}")

def update_schedule(new_schedule_str):
    """
    Updates the schedule from an incoming MQTT message.
    :param new_schedule_str: (str) JSON string of the new schedule.
    """
    global schedule_data
    try:
        new_data = ujson.loads(new_schedule_str)
        
        if validate_schedule_data(new_data):
            schedule_data = new_data
            save_schedule()
            log("Schedule updated and saved.")
        else:
            log("Invalid schedule format received.")
    except (ValueError, TypeError) as e:
        log(f"Could not decode or parse new schedule JSON: {e}")

def is_raining():
    """Checks the rain sensor. HIGH signal means it's raining."""
    try:
        rain_pin = machine.Pin(RAIN_SENSOR_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
        # The README specifies HIGH = rain.
        # A pull-down ensures it's low when dry.
        return rain_pin.value() == 1
    except Exception as e:
        log(f"Error reading rain sensor: {e}")
        return False  # Default to no rain if sensor fails

def get_current_time():
    """Gets the current time and returns a tuple (hour, minute)."""
    now = time.localtime()
    return now[3], now[4]  # hour, minute

async def handle_rain_delay():
    """Handles the rain delay logic."""
    global rain_delay_active, rain_check_count
    
    if not rain_delay_active:
        log("Rain detected! Delaying watering for 2 hours.")
        rain_delay_active = True
        rain_check_count = 0
    
    # Wait for an hour before checking again
    await asyncio.sleep(RAIN_CHECK_INTERVAL)
    rain_check_count += 1
    
    if rain_check_count >= MAX_RAIN_CHECKS:
        log("Rain continues. Skipping watering for today.")
        # Reset for the next day
        rain_delay_active = False
        rain_check_count = 0
        # Sleep until the next day (approximately)
        await asyncio.sleep(22 * 3600)

async def check_scheduled_jobs():
    """Checks and executes scheduled irrigation jobs."""
    current_hour, current_minute = get_current_time()
    
    for job in schedule_data.get('schedule', []):
        if job['hour'] == current_hour and job['minute'] == current_minute:
            log(f"Time match: Starting job for zone {job['zone']}.")
            # Run the zone asynchronously
            asyncio.create_task(run_zone(job['zone'], job['duration']))

async def schedule_checker():
    """The main async task that checks and runs the irrigation schedule."""
    global rain_delay_active, rain_check_count
    
    log("Schedule checker started.")
    
    while True:
        try:
            # Rain sensor logic
            if is_raining():
                await handle_rain_delay()
                continue  # Re-evaluate from the top of the loop

            # If it was raining but has stopped
            if rain_delay_active and not is_raining():
                log("Rain has stopped. Resuming normal schedule.")
                rain_delay_active = False
                rain_check_count = 0

            # If a rain delay is active, don't run any schedules
            if rain_delay_active:
                await asyncio.sleep(SCHEDULE_CHECK_INTERVAL)
                continue

            # Check for scheduled runs
            await check_scheduled_jobs()
            
            # Check every minute
            await asyncio.sleep(SCHEDULE_CHECK_INTERVAL)
            
        except Exception as e:
            log(f"Error in schedule checker: {e}")
            await asyncio.sleep(SCHEDULE_CHECK_INTERVAL)

