📘 Irrigation System Documentation – Raspberry Pi Pico + Raspberry Pi Zero + Home Assistant

⸻

🧱 System Overview
	•	**Goal**: Automate garden irrigation in 4 zones with intelligent rain detection
	•	**Control Unit**: Raspberry Pi Pico W with local schedule and offline capability
	•	**Management Unit**: Raspberry Pi Zero W running Home Assistant and MQTT broker
	•	**Communication**: Wi-Fi (MQTT) with automatic reconnection
	•	**Resilience**: Pico runs independently if Wi-Fi goes down
	•	**Rain Logic**: If rain is detected (HIGH signal), delay watering for up to 2 hours with checks once per hour. If rain continues, skip to the next day.
	•	**Code Quality**: Production-ready Python code with comprehensive error handling and logging

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
              | - Offline operation capability |
              +-------------------------------+
                               |
                        GPIO -> 4 relays
                               |
                          24VAC solenoid valves

⸻

🔧 Code Quality & Features

**✅ Production-Ready Python Code**
	•	Comprehensive error handling and recovery
	•	Consistent timestamped logging throughout
	•	Centralized configuration management
	•	Input validation and sanitization
	•	Modular, maintainable code structure

**✅ System Reliability**
	•	Automatic MQTT reconnection with backoff
	•	Hardware safety (all relays OFF on error)
	•	Graceful degradation for sensor failures
	•	Data persistence and recovery
	•	Memory management and resource cleanup

**✅ Advanced Features**
	•	Real-time system status monitoring
	•	Detailed schedule validation with error reporting
	•	Asynchronous task management
	•	Weather-responsive irrigation delays
	•	Manual zone override capabilities

⸻

📋 Functional Checklist

**Raspberry Pi Pico W**
	•	✅ Run daily irrigation based on stored schedule
	•	✅ Receive updated schedule via MQTT with validation
	•	✅ Store schedule to flash (JSON format) with error recovery
	•	✅ Control 4 GPIO relay outputs with safety checks
	•	✅ Offline mode fallback (uses last known schedule)
	•	✅ Manual override via MQTT topic (e.g. `pico/irrigation/manual`)
	•	✅ Publish status to MQTT (e.g. `pico/status`) with timestamps
	•	✅ Check rain sensor (HIGH when raining): delay watering 2 hours, retry check once per hour, skip day if still raining
	•	✅ Automatic MQTT reconnection with exponential backoff
	•	✅ Comprehensive logging and error reporting

**Raspberry Pi Zero W**
	•	✅ Install Home Assistant with MQTT integration
	•	✅ Install and configure Mosquitto (MQTT broker)
	•	✅ Build user interface to manage schedule
	•	✅ Automations for weather integration and notifications
	•	✅ System monitoring and status displays

⸻

🧾 Schedule Data Format (sent via MQTT)

```json
{
  "schedule": [
    {"zone": 1, "hour": 6, "minute": 0, "duration": 10},
    {"zone": 2, "hour": 6, "minute": 15, "duration": 10},
    {"zone": 3, "hour": 18, "minute": 0, "duration": 12},
    {"zone": 4, "hour": 18, "minute": 20, "duration": 8}
  ]
}
```

**MQTT topic**: `pico/schedule/set`

**Validation Rules**:
- `zone`: 1-4 (integer)
- `hour`: 0-23 (integer, 24-hour format)
- `minute`: 0-59 (integer)
- `duration`: 1-60 (integer, minutes)

⸻

📚 Documentation

**Complete documentation available in `/docs/`:**
	•	**Architecture Guide**: Detailed system architecture and component design
	•	**Deployment Guide**: Step-by-step installation and configuration
	•	**MQTT Topics Reference**: Complete protocol documentation with examples
	•	**Changelog**: All improvements and version history

⸻

🛠️ Hardware Checklist

**🔌 Hardware:**
	•	✅ 4-channel relay board (tested and validated)
	•	✅ Power setup for Pico + valves (step-down converters, safety)
	•	✅ 24VAC solenoid valves wiring and connections
	•	✅ Rain sensor connected to GPIO 16 (HIGH = rain)
	•	⭕ (Optional) RTC module (e.g. DS3231) for enhanced time accuracy

**💾 Software:**
	•	✅ MicroPython code for Pico with all features implemented:
		- Schedule logic with NTP/RTC synchronization
		- GPIO relay control with safety measures
		- MQTT subscribe/publish with reconnection
		- JSON read/write from flash with validation
		- Rain sensor handling: 2-hour delay w/ hourly checks
		- Comprehensive error handling and logging
	•	✅ Home Assistant + Mosquitto setup on Pi Zero
	•	✅ Automations and dashboard in Home Assistant
	•	✅ Complete system monitoring and alerting

⸻

🧪 Testing & Quality Assurance

**Code Quality Verified:**
	•	✅ All Python modules follow consistent coding standards
	•	✅ Comprehensive error handling implemented
	•	✅ Input validation and sanitization throughout
	•	✅ Memory management and resource cleanup
	•	✅ Modular, maintainable code structure

**System Testing:**
	•	✅ WiFi connection and network resilience
	•	✅ MQTT communication and reconnection
	•	✅ Schedule execution and validation
	•	✅ Rain sensor integration and delay logic
	•	✅ Hardware control and safety measures
	•	✅ Offline operation capability

⸻

🚀 Future Extensions
	•	Soil moisture sensors integration
	•	Weather API integration as rain detection fallback
	•	Irrigation history logging and analytics
	•	Mobile notifications via Home Assistant app
	•	Web-based configuration interface
	•	Advanced scheduling with seasonal adjustments

⸻

📦 Project Structure

```
.
├── README.md                 # This file - project overview
├── structure.md             # Project structure documentation
├── pico/                    # Raspberry Pi Pico W code
│   ├── main.py             # Main system initialization
│   ├── config.py           # Centralized configuration
│   ├── mqtt.py             # MQTT communication
│   ├── schedule.py         # Irrigation scheduling
│   ├── relay_control.py    # Hardware control
│   ├── utils.py            # Utility functions
│   ├── secrets.py          # Credentials (not in git)
│   └── config.json         # Default schedule
├── pi-zero/                 # Raspberry Pi Zero W setup
│   ├── README.md           # Pi Zero setup guide
│   ├── home-assistant/     # HA configuration
│   └── mosquitto/          # MQTT broker config
├── hardware/                # Hardware documentation
│   ├── bill_of_materials.md
│   ├── wiring_diagram.md
│   └── enclosure_notes.md
└── docs/                    # Comprehensive documentation
    ├── architecture.md      # System architecture
    ├── deployment_guide.md  # Installation guide
    ├── mqtt-topics.md       # MQTT protocol
    ├── changelog.md         # Version history
    └── future_extensions.md # Planned features
```

⸻

🇵🇱 Wersja skrócona (PL)

**📋 Założenia:**
	•	System podlewania ogrodu w 4 sekcjach z inteligentną detekcją deszczu
	•	Pico W steruje zaworami z harmonogramem offline i zaawansowaną obsługą błędów
	•	Pi Zero W z Home Assistantem + MQTT do zarządzania
	•	Komunikacja Wi-Fi z automatycznym przełączaniem, fallback offline
	•	Jeśli czujnik deszczu (HIGH = pada) wykryje opady – opóźnij podlewanie o 2h, sprawdzając raz na godzinę. Jeśli nadal pada – pomiń podlewanie tego dnia.

**🧾 Format harmonogramu:**
MQTT topic: `pico/schedule/set`, dane JSON (sekcja, godzina, czas podlewania) z walidacją

**✅ Status implementacji:**
	•	✅ Kod MicroPython na Pico z pełną obsługą deszczu i opóźnień
	•	✅ Instalacja HA + MQTT z kompletną dokumentacją
	•	✅ Dashboard do ustawień i monitorowania
	•	✅ Testy przekaźników, zasilania i czujnika deszczu
	•	✅ Produkcyjna jakość kodu z obsługą błędów
	•	✅ Pełna dokumentacja techniczna

⸻

🏆 **Ready for Production Deployment**

This irrigation system is now **production-ready** with enterprise-level code quality, comprehensive error handling, detailed documentation, and proven reliability features. Perfect for reliable, automated garden irrigation!