import machine
import uasyncio as asyncio
from utils import log
from config import RELAY_PINS, MIN_ZONE, MAX_ZONE, MIN_DURATION, MAX_DURATION

relays = {}

def setup_relays():
    """Initialize relay pins as outputs and set them to OFF."""
    for zone, pin in RELAY_PINS.items():
        relays[zone] = machine.Pin(pin, machine.Pin.OUT)
        relays[zone].value(0)  # Active LOW relays might need value(1) to be off
    log("Relays initialized.")

def control_relay(zone, state):
    """
    Control a single relay.
    :param zone: (int) The zone number (1-4)
    :param state: (bool) True for ON, False for OFF
    """
    if zone in relays:
        relays[zone].value(1 if state else 0)
        log(f"Zone {zone} relay {'ON' if state else 'OFF'}")
    else:
        log(f"Error: Zone {zone} is not a valid zone.")

async def run_zone(zone, duration_minutes):
    """
    Run a specific irrigation zone for a set duration.
    :param zone: (int) The zone number
    :param duration_minutes: (int) Duration in minutes
    """
    if zone not in relays:
        log(f"Error: Zone {zone} is not a valid zone.")
        return
    
    if not (MIN_DURATION <= duration_minutes <= MAX_DURATION):
        log(f"Error: Invalid duration {duration_minutes} minutes for zone {zone}. Must be between {MIN_DURATION} and {MAX_DURATION}.")
        return
    
    log(f"Starting irrigation for zone {zone} for {duration_minutes} minutes.")
    control_relay(zone, True)
    
    try:
        await asyncio.sleep(duration_minutes * 60)
    except asyncio.CancelledError:
        log(f"Irrigation for zone {zone} was cancelled.")
    finally:
        control_relay(zone, False)
        log(f"Finished irrigation for zone {zone}.")

def all_relays_off():
    """Turn all relays off."""
    for zone in relays:
        control_relay(zone, False)
    log("All relays turned OFF.")
