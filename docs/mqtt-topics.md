# MQTT Topics Documentation

This document describes all MQTT topics used in the Green Grass v1.0 irrigation system.

## Topic Overview

The system uses three main MQTT topics for communication between the Raspberry Pi Pico W and Home Assistant:

| Topic | Direction | QoS | Retained | Description |
|-------|-----------|-----|----------|-------------|
| `pico/schedule/set` | HA → Pico | 1 | Yes | Update irrigation schedule |
| `pico/irrigation/manual` | HA → Pico | 0 | No | Manual zone control |
| `pico/status` | Pico → HA | 0 | Yes | System status updates |

## Topic Details

### pico/schedule/set

**Purpose**: Updates the irrigation schedule on the Pico W  
**Direction**: Home Assistant → Pico  
**QoS**: 1 (At least once delivery)  
**Retained**: Yes (Last schedule is retained for new subscribers)

**Payload Format**:
```json
{
  "schedule": [
    {
      "zone": 1,
      "hour": 6,
      "minute": 0,
      "duration": 10
    },
    {
      "zone": 2,
      "hour": 6,
      "minute": 15,
      "duration": 10
    },
    {
      "zone": 3,
      "hour": 18,
      "minute": 0,
      "duration": 12
    },
    {
      "zone": 4,
      "hour": 18,
      "minute": 20,
      "duration": 8
    }
  ]
}
```

**Field Validation**:
- `zone`: Integer 1-4 (irrigation zone number)
- `hour`: Integer 0-23 (24-hour format)
- `minute`: Integer 0-59
- `duration`: Integer 1-60 (minutes)

**Example Usage**:
```bash
mosquitto_pub -h localhost -t "pico/schedule/set" -m '{"schedule":[{"zone":1,"hour":6,"minute":0,"duration":10}]}'
```

### pico/irrigation/manual

**Purpose**: Manually trigger irrigation for a specific zone  
**Direction**: Home Assistant → Pico  
**QoS**: 0 (At most once delivery)  
**Retained**: No

**Payload Format**:
```json
{
  "zone": 1,
  "duration": 5
}
```

**Field Validation**:
- `zone`: Integer 1-4 (irrigation zone number)
- `duration`: Integer 1-60 (minutes)

**Example Usage**:
```bash
mosquitto_pub -h localhost -t "pico/irrigation/manual" -m '{"zone":1,"duration":5}'
```

### pico/status

**Purpose**: System status and health information  
**Direction**: Pico → Home Assistant  
**QoS**: 0 (At most once delivery)  
**Retained**: Yes (Last status is retained)

**Payload Format**:
```json
{
  "status": "Pico is running",
  "timestamp": 1672531200
}
```

**Common Status Messages**:
- `"Pico connected and ready"` - Initial connection established
- `"Pico is running"` - Periodic heartbeat (every 5 minutes)
- `"Schedule updated"` - Schedule successfully received and saved
- `"Manual run started for zone X"` - Manual irrigation started
- `"Rain detected! Delaying watering for 2 hours"` - Rain delay activated
- `"Rain has stopped. Resuming normal schedule"` - Rain delay cleared

**Example Usage**:
```bash
mosquitto_sub -h localhost -t "pico/status"
```

## Error Handling

### Invalid Payloads

When the Pico receives an invalid payload, it will:
1. Log the error locally
2. Publish a status message indicating the failure
3. Continue operation with the previous valid configuration

**Example Error Status Messages**:
- `"Invalid schedule format received"`
- `"Invalid manual run command"`
- `"Failed to decode manual run command"`

### Connection Issues

If MQTT connection is lost:
1. Pico continues operation with stored schedule
2. Automatic reconnection attempts every 60 seconds
3. All relays turn OFF for safety during reconnection
4. Status published upon successful reconnection

## Home Assistant Integration

### Sensors

Create sensors in Home Assistant to monitor system status:

```yaml
mqtt:
  sensor:
    - name: "Irrigation System Status"
      state_topic: "pico/status"
      value_template: "{{ value_json.status }}"
      json_attributes_topic: "pico/status"
      
    - name: "Irrigation Last Update"
      state_topic: "pico/status"
      value_template: "{{ value_json.timestamp | timestamp_local }}"
      device_class: timestamp
```

### Automations

Example automation to send schedule updates:

```yaml
automation:
  - alias: "Update Irrigation Schedule"
    trigger:
      - platform: state
        entity_id: input_boolean.update_irrigation_schedule
        to: 'on'
    action:
      - service: mqtt.publish
        data:
          topic: "pico/schedule/set"
          payload_template: >
            {
              "schedule": [
                {
                  "zone": 1,
                  "hour": {{ states('input_number.zone1_hour') | int }},
                  "minute": {{ states('input_number.zone1_minute') | int }},
                  "duration": {{ states('input_number.zone1_duration') | int }}
                }
              ]
            }
```

## Testing and Debugging

### MQTT Client Tools

Use mosquitto client tools for testing:

```bash
# Subscribe to all pico topics
mosquitto_sub -h localhost -t "pico/#" -v

# Publish test schedule
mosquitto_pub -h localhost -t "pico/schedule/set" -f test_schedule.json

# Manual zone test
mosquitto_pub -h localhost -t "pico/irrigation/manual" -m '{"zone":1,"duration":1}'
```

### Monitoring

Monitor MQTT traffic:
```bash
# Real-time topic monitoring
mosquitto_sub -h localhost -t "#" -v

# Check retained messages
mosquitto_sub -h localhost -t "pico/status" -C 1
```