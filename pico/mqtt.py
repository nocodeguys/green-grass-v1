from umqtt.simple import MQTTClient
import uasyncio as asyncio
import machine
import ujson

import secrets
from schedule import update_schedule
from relay_control import run_zone, all_relays_off
from utils import log

# MQTT Topics
SCHEDULE_SET_TOPIC = "pico/schedule/set"
MANUAL_RUN_TOPIC = "pico/irrigation/manual"
STATUS_TOPIC = "pico/status"

client = None

def callback(topic, msg):
    """Callback function to handle incoming MQTT messages."""
    topic = topic.decode('utf-8')
    msg = msg.decode('utf-8')
    log(f"Received message on topic: {topic}")

    if topic == SCHEDULE_SET_TOPIC:
        update_schedule(msg)
        publish_status("Schedule updated")
    elif topic == MANUAL_RUN_TOPIC:
        try:
            data = ujson.loads(msg)
            zone = data.get("zone")
            duration = data.get("duration")
            if zone and duration:
                log(f"Manual run command received for zone {zone} for {duration} mins.")
                # Run this in a non-blocking way
                asyncio.create_task(run_zone(zone, duration))
                publish_status(f"Manual run started for zone {zone}")
            else:
                log("Invalid manual run format.")
                publish_status("Invalid manual run command")
        except (ValueError, TypeError):
            log("Could not decode manual run JSON.")
            publish_status("Failed to decode manual run command")

def connect_and_subscribe():
    """Connects to the MQTT broker and subscribes to topics."""
    global client
    client_id = f"pico-irrigation-{machine.unique_id().hex()}"
    
    client = MQTTClient(
        client_id,
        secrets.MQTT_BROKER,
        user=secrets.MQTT_USER,
        password=secrets.MQTT_PASSWORD
    )
    
    client.set_callback(callback)
    
    try:
        client.connect()
        client.subscribe(SCHEDULE_SET_TOPIC)
        client.subscribe(MANUAL_RUN_TOPIC)
        log(f"Connected to MQTT broker at {secrets.MQTT_BROKER} and subscribed to topics.")
        publish_status("Pico connected and ready")
        return client
    except OSError as e:
        log(f"Failed to connect to MQTT broker: {e}")
        return None

def publish_status(status_msg):
    """Publishes a status message to the status topic."""
    if client:
        try:
            payload = ujson.dumps({"status": status_msg})
            client.publish(STATUS_TOPIC, payload)
        except Exception as e:
            log(f"Failed to publish status: {e}")

async def mqtt_listener():
    """Async task to listen for MQTT messages."""
    while True:
        if client:
            try:
                client.check_msg()
            except OSError as e:
                log(f"MQTT connection error: {e}. Reconnecting...")
                all_relays_off() # Safety first
                connect_and_subscribe()
        await asyncio.sleep(1)

async def periodic_status_publisher():
    """Async task to publish a 'still alive' status periodically."""
    while True:
        publish_status("Pico is running")
        await asyncio.sleep(300) # Publish status every 5 minutes