📘 Irrigation System Documentation – Raspberry Pi Pico + Raspberry Pi Zero + Home Assistant

⸻

🧱 System Overview
	•	Goal: Automate garden irrigation in 4 zones
	•	Control Unit: Raspberry Pi Pico W with local schedule
	•	Management Unit: Raspberry Pi Zero W running Home Assistant and MQTT broker
	•	Communication: Wi-Fi (MQTT)
	•	Resilience: Pico runs independently if Wi-Fi goes down
	•	Rain Logic: If rain is detected (HIGH signal), delay watering for up to 2 hours with checks once per hour. If rain continues, skip to the next day.

⸻

📡 System Architecture

                +-----------------------------+
                |     Home Assistant (Pi0)    |
                |    + Mosquitto MQTT broker  |
                +--------------+--------------+
                               |
                         Wi-Fi / MQTT
                               |
              +-------------------------------+
              |     Raspberry Pi Pico W       |
              | - Local schedule              |
              | - Relay control via GPIO      |
              | - MQTT client (sub/pub)       |
              | - Schedule stored in flash    |
              | - Rain sensor logic (HIGH = rain) |
              +-------------------------------+
                               |
                        GPIO -> 4 relays
                               |
                          24VAC solenoid valves


⸻

📋 Functional Checklist

Raspberry Pi Pico W
	•	Run daily irrigation based on stored schedule
	•	Receive updated schedule via MQTT
	•	Store schedule to flash (JSON format)
	•	Control 4 GPIO relay outputs
	•	Offline mode fallback (uses last known schedule)
	•	Manual override via MQTT topic (e.g. pico/irrigation/manual)
	•	Publish status to MQTT (e.g. pico/status)
	•	Check rain sensor (HIGH when raining): delay watering 2 hours, retry check once per hour, skip day if still raining

Raspberry Pi Zero W
	•	Install Home Assistant
	•	Install and configure Mosquitto (MQTT broker)
	•	Build user interface to manage schedule
	•	Automations (weather, sensors, etc.)

⸻

🧾 Schedule Data Format (sent via MQTT)

{
  "schedule": [
    {"zone": 1, "hour": 6, "minute": 0, "duration": 10},
    {"zone": 2, "hour": 6, "minute": 15, "duration": 10},
    {"zone": 3, "hour": 18, "minute": 0, "duration": 12},
    {"zone": 4, "hour": 18, "minute": 20, "duration": 8}
  ]
}

MQTT topic: pico/schedule/set

⸻

🛠️ TODO Checklist

🔌 Hardware:
	•	Install relay board and test with Pico
	•	Power setup for Pico + valves (step-down converters, safety)
	•	Wire and connect 24VAC solenoid valves
	•	(Optional) Add RTC module (e.g. DS3231) to Pico
	•	Connect rain sensor to GPIO (HIGH = rain)

💾 Software:
	•	MicroPython code for Pico:
	•	Schedule logic with RTC/NTP
	•	GPIO relay control
	•	MQTT subscribe/publish
	•	JSON read/write from flash
	•	Rain sensor handling: 2-hour delay w/ hourly checks
	•	Set up HA + Mosquitto on Pi Zero
	•	Automations and dashboard in Home Assistant

⸻

🚀 Future Extensions
	•	Soil moisture sensors
	•	Rain detection via weather API fallback
	•	Irrigation logs stored locally or in HA
	•	Mobile access via Home Assistant Companion App

⸻

🇵🇱 Wersja skrócona (PL)

📋 Założenia:
	•	System podlewania ogrodu w 4 sekcjach
	•	Pico W steruje zaworami z harmonogramem offline
	•	Pi Zero W z Home Assistantem + MQTT do zarządzania
	•	Komunikacja Wi-Fi, fallback offline
	•	Jeśli czujnik deszczu (HIGH = pada) wykryje opady – opóźnij podlewanie o 2h, sprawdzając raz na godzinę. Jeśli nadal pada – pomiń podlewanie tego dnia.

🧾 Format harmonogramu:

MQTT topic: pico/schedule/set, dane JSON (sekcja, godzina, czas podlewania)

✅ TODO:
	•	Kod MicroPython na Pico z obsługą deszczu i opóźnieniem
	•	Instalacja HA + MQTT
	•	Dashboard do ustawień
	•	Test przekaźników, zasilania i czujnika deszczu