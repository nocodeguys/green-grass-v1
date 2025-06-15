#  Wiring Diagram

This document describes the electrical connections between the Raspberry Pi Pico W, the relay module, the rain sensor, and the power supplies.

## Components:
- Raspberry Pi Pico W
- 4-Channel Relay Module (5V)
- 24VAC Solenoid Valves
- 24VAC Power Supply (for valves)
- 5V Power Supply (for Pico and relay module)
- Rain Sensor Module (e.g., YL-83 or similar)

---

## Connections:

### 1. Raspberry Pi Pico W to 4-Channel Relay Module

The relay module typically has a VCC, GND, and four input pins (IN1, IN2, IN3, IN4).

| Raspberry Pi Pico Pin | Relay Module Pin | Purpose                               |
| --------------------- | ---------------- | ------------------------------------- |
| **VBUS (Pin 40)**     | VCC              | 5V Power to Relay Module              |
| **GND (Pin 38)**      | GND              | Common Ground                         |
| **GPIO2 (Pin 4)**     | IN1              | Control Signal for Relay 1 (Zone 1)   |
| **GPIO3 (Pin 5)**     | IN2              | Control Signal for Relay 2 (Zone 2)   |
| **GPIO4 (Pin 6)**     | IN3              | Control Signal for Relay 3 (Zone 3)   |
| **GPIO5 (Pin 7)**     | IN4              | Control Signal for Relay 4 (Zone 4)   |

*Note: The GPIO pins used here must match the `RELAY_PINS` dictionary in `pico/relay_control.py`.*

### 2. Raspberry Pi Pico W to Rain Sensor

The rain sensor module usually has VCC, GND, and a digital output (DO).

| Raspberry Pi Pico Pin | Rain Sensor Pin  | Purpose                               |
| --------------------- | ---------------- | ------------------------------------- |
| **3V3(OUT) (Pin 36)** | VCC              | 3.3V Power to Sensor                  |
| **GND (Pin 33)**      | GND              | Common Ground                         |
| **GPIO16 (Pin 21)**   | DO (Digital Out) | Rain Signal (HIGH = Rain)             |

*Note: The GPIO pin used here must match `RAIN_SENSOR_PIN` in `pico/schedule.py`.*

### 3. Relay Module to Solenoid Valves (High Voltage Path - 24VAC)

**⚠️ CAUTION: Handle 24VAC wiring with care. Ensure power is disconnected when wiring.**

The 24VAC power supply has two outputs (typically no polarity).

1.  Connect **one wire** from the 24VAC power supply directly to **one terminal** of EACH of the four solenoid valves. This is the common wire.
2.  Connect the **other wire** from the 24VAC power supply to the **common (C)** terminal of **each relay** on the module. You may need to create short jumper wires to link the C terminals together.
3.  For each zone, connect the **Normally Open (NO)** terminal of the relay to the **remaining terminal** on the corresponding solenoid valve.

-   Relay 1 (NO) -> Solenoid 1 (Zone 1)
-   Relay 2 (NO) -> Solenoid 2 (Zone 2)
-   Relay 3 (NO) -> Solenoid 3 (Zone 3)
-   Relay 4 (NO) -> Solenoid 4 (Zone 4)

When a relay is activated by the Pico, it closes the circuit between C and NO, allowing 24VAC to flow to the solenoid and open the valve.

---

## Visual Diagram

Here is a visual representation of the connections described above. GitHub will render this into a diagram.

```mermaid
graph TD
    subgraph "Logic Power & Control (DC)"
        pico[Raspberry Pi Pico W]
        relay_logic[Relay Module Logic Side]
        rain_sensor[Rain Sensor]
        power_5v[5V Power via USB]

        power_5v --> pico
        pico -- "VBUS (5V) & GND" --> relay_logic
        pico -- "GPIO 2-5 (Control Signals)" --> relay_logic(IN1-4)

        pico -- "3V3 & GND" --> rain_sensor
        rain_sensor -- "Digital Out" --> pico(GPIO16)
    end

    subgraph "High Voltage & Irrigation (24VAC)"
        relay_switch[Relay Module Switch Side]
        valves[Solenoid Valves (x4)]
        power_24vac[24VAC Power Supply]

        power_24vac -- "Common Wire to All Valves" --> valves
        power_24vac -- "Hot Wire" --> relay_switch(Common Terminals)
        relay_switch(Normally Open Terminals) -- "Switched Hot to Each Valve" --> valves
    end

    %% Styling
    classDef component fill:#f9f,stroke:#333,stroke-width:2px;
    classDef power fill:#f2f2f2,stroke:#333;
    class pico,relay_logic,relay_switch,rain_sensor,valves,power_24vac,power_5v component;
    class power_5v,power_24vac power;
```

---

## Power Supply

-   The **Raspberry Pi Pico W** is powered via its Micro USB port from a reliable 5V source.
-   The **Relay Module** is powered by the Pico's VBUS pin.
-   The **Solenoid Valves** are powered by a separate 24VAC transformer.

**IMPORTANT:** Do NOT mix the 5V/3.3V DC logic power with the 24VAC valve power. The relay module provides the necessary electrical isolation. 