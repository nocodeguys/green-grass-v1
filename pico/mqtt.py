from umqtt.simple import MQTTClient
import uasyncio as asyncio
import machine
import ujson
import time

import secrets
from schedule import update_schedule
from relay_control import run_zone, all_relays_off
from utils import log
from config import (
    SCHEDULE_SET_TOPIC, MANUAL_RUN_TOPIC, STATUS_TOPIC,
    MQTT_CHECK_INTERVAL, STATUS_PUBLISH_INTERVAL
)

client = None

def callback(topic, msg):
    """Callback function to handle incoming MQTT messages."""
    try:
        topic = topic.decode('utf-8')
        msg = msg.decode('utf-8')
        log(f"Received message on topic: {topic}")

        if topic == SCHEDULE_SET_TOPIC:
            update_schedule(msg)
            publish_status("Schedule updated")
        elif topic == MANUAL_RUN_TOPIC:
            handle_manual_run(msg)
        else:
            log(f"Unknown topic: {topic}")
    except Exception as e:
        log(f"Error in MQTT callback: {e}")

def handle_manual_run(msg):
    """Handle manual run command."""
    try:
        data = ujson.loads(msg)
        zone = data.get("zone")
        duration = data.get("duration")
        
        if zone and duration and isinstance(zone, int) and isinstance(duration, int):
            log(f"Manual run command received for zone {zone} for {duration} mins.")
            # Run this in a non-blocking way
            asyncio.create_task(run_zone(zone, duration))
            publish_status(f"Manual run started for zone {zone}")
        else:
            log("Invalid manual run format: missing or invalid zone/duration.")
            publish_status("Invalid manual run command")
    except (ValueError, TypeError) as e:
        log(f"Could not decode manual run JSON: {e}")
        publish_status("Failed to decode manual run command")

def connect_and_subscribe():
    """Connects to the MQTT broker and subscribes to topics."""
    global client
    
    try:
        client_id = f"pico-irrigation-{machine.unique_id().hex()}"
        
        client = MQTTClient(
            client_id,
            secrets.MQTT_BROKER,
            user=secrets.MQTT_USER,
            password=secrets.MQTT_PASSWORD
        )
        
        client.set_callback(callback)
        client.connect()
        client.subscribe(SCHEDULE_SET_TOPIC)
        client.subscribe(MANUAL_RUN_TOPIC)
        
        log(f"Connected to MQTT broker at {secrets.MQTT_BROKER} and subscribed to topics.")
        publish_status("Pico connected and ready")
        return client
        
    except OSError as e:
        log(f"Failed to connect to MQTT broker: {e}")
        return None
    except Exception as e:
        log(f"Unexpected error connecting to MQTT: {e}")
        return None

def publish_status(status_msg):
    """Publishes a status message to the status topic."""
    if client:
        try:
            payload = ujson.dumps({
                "status": status_msg,
                "timestamp": time.time()
            })
            client.publish(STATUS_TOPIC, payload)
            log(f"Status published: {status_msg}")
        except Exception as e:
            log(f"Failed to publish status: {e}")

def reconnect_mqtt():
    """Attempts to reconnect to MQTT broker."""
    global client
    log("Attempting to reconnect to MQTT...")
    all_relays_off()  # Safety first
    client = connect_and_subscribe()
    return client is not None

async def mqtt_listener():
    """Async task to listen for MQTT messages."""
    global client
    
    log("MQTT listener started.")
    
    while True:
        if client:
            try:
                client.check_msg()
            except OSError as e:
                log(f"MQTT connection error: {e}. Reconnecting...")
                if not reconnect_mqtt():
                    log("Failed to reconnect to MQTT. Will retry in 60 seconds.")
                    await asyncio.sleep(60)
            except Exception as e:
                log(f"Unexpected error in MQTT listener: {e}")
                await asyncio.sleep(5)
        else:
            log("MQTT client not connected. Attempting to reconnect...")
            if not reconnect_mqtt():
                await asyncio.sleep(60)
                
        await asyncio.sleep(MQTT_CHECK_INTERVAL)

async def periodic_status_publisher():
    """Async task to publish a 'still alive' status periodically."""
    log("Status publisher started.")
    
    while True:
        if client:
            publish_status("Pico is running")
        await asyncio.sleep(STATUS_PUBLISH_INTERVAL)