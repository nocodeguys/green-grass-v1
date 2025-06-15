# Project Structure

This file outlines the directory and file structure of the Green Grass v1.0 project.

```
.
├── README.md
├── hardware/
│   ├── bill_of_materials.md
│   ├── enclosure_notes.md
│   └── wiring_diagram.md
├── pico/
│   ├── main.py
│   ├── secrets.py
│   ├── config.json
│   ├── mqtt.py
│   ├── schedule.py
│   ├── relay_control.py
│   └── utils.py
├── pi-zero/
│   ├── README.md
│   ├── home-assistant/
│   │   ├── configuration.yaml
│   │   ├── automations.yaml
│   │   ├── sensors.yaml
│   │   └── ui-lovelace.yaml
│   └── mosquitto/
│       ├── mosquitto.conf
│       └── passwd.placeholder
└── docs/
    ├── deployment_guide.md
    └── future_extensions.md
```

## Directory Descriptions

-   `README.md`: The main project README file with a high-level overview.
-   `hardware/`: Contains documentation related to the physical build of the system.
-   `pico/`: All MicroPython source code intended to be deployed on the Raspberry Pi Pico W.
-   `pi-zero/`: All configuration files and setup guides for the Raspberry Pi Zero W.
-   `docs/`: Contains supplementary documentation for deployment and future development.

