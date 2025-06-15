# 📋 Bill of Materials (BOM)

This list includes all the necessary hardware components for building the irrigation system.

| Category             | Item                                           | Quantity | Notes                                                                                                  |
| -------------------- | ---------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------ |
| **Control Unit**     | Raspberry Pi Pico W                            | 1        | The "W" version with Wi-Fi is required for MQTT communication.                                         |
| **Management Unit**  | Raspberry Pi Zero W                            | 1        | A Pi 3 or 4 would also work and offer better performance for Home Assistant.                           |
|                      | MicroSD Card                                   | 1        | 16GB or larger, Class 10 recommended.                                                                  |
| **Valve Control**    | 4-Channel 5V Relay Module                      | 1        | Ensure it can handle 24VAC on the switched side. Look for modules with opto-isolators.                |
|                      | 24VAC Irrigation Solenoid Valves               | 4        | Standard garden irrigation valves.                                                                     |
| **Sensors**          | Rain Sensor Module                             | 1        | A simple module with a digital output (e.g., YL-83, FC-37).                                            |
| **Power**            | 5V Micro USB Power Adapter                     | 2        | One for the Pico, one for the Pi Zero. A 2A+ supply is recommended for the Pi Zero.                     |
|                      | 24VAC Power Adapter/Transformer                | 1        | Must be rated to handle the current draw of at least one solenoid valve (typically ~250-500mA).       |
| **Wiring & Connectors** | Jumper Wires (Dupont Cables)               | ~20      | For connecting the Pico to the relay and sensor modules. Male-to-Female and Female-to-Female are useful. |
|                      | 18-22 AWG Electrical Wire                      | 1 spool  | For the 24VAC connections between the power supply, relays, and valves.                                |
|                      | Screw Terminals or Wire Nuts                   | several  | For safely connecting the 24VAC wiring.                                                                |
| **Enclosure**        | Weatherproof Project Box                       | 1        | To house the Pico, relay module, and power connections safely outdoors. See `enclosure_notes.md`.      |
| **Optional**         | DS3231 Real-Time Clock (RTC) Module            | 1        | If you need accurate timekeeping without relying on NTP after boot.                                    |
