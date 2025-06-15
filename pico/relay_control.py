import machine
import uasyncio as asyncio

# GPIO pins for the 4 relays
# NOTE: Adjust these pins to match your hardware wiring
RELAY_PINS = {
    1: 2,  # Zone 1 -> GPIO 2
    2: 3,  # Zone 2 -> GPIO 3
    3: 4,  # Zone 3 -> GPIO 4
    4: 5,  # Zone 4 -> GPIO 5
}

relays = {}

def setup_relays():
    """Initialize relay pins as outputs and set them to OFF."""
    for zone, pin in RELAY_PINS.items():
        relays[zone] = machine.Pin(pin, machine.Pin.OUT)
        relays[zone].value(0)  # Active LOW relays might need value(1) to be off
    print("Relays initialized.")

def control_relay(zone, state):
    """
    Control a single relay.
    :param zone: (int) The zone number (1-4)
    :param state: (bool) True for ON, False for OFF
    """
    if zone in relays:
        relays[zone].value(1 if state else 0)
        print(f"Zone {zone} relay {'ON' if state else 'OFF'}")
    else:
        print(f"Error: Zone {zone} is not a valid zone.")

async def run_zone(zone, duration_minutes):
    """
    Run a specific irrigation zone for a set duration.
    :param zone: (int) The zone number
    :param duration_minutes: (int) Duration in minutes
    """
    print(f"Starting irrigation for zone {zone} for {duration_minutes} minutes.")
    control_relay(zone, True)
    await asyncio.sleep(duration_minutes * 60)
    control_relay(zone, False)
    print(f"Finished irrigation for zone {zone}.")

def all_relays_off():
    """Turn all relays off."""
    for zone in relays:
        control_relay(zone, False)
    print("All relays turned OFF.")
