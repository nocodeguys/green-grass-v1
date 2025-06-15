# 🚀 Future Extensions

This document outlines potential future upgrades and features that can be added to the irrigation system.

## 1. Soil Moisture Sensors

-   **Concept:** Instead of watering on a fixed schedule, water only when the soil is actually dry. This is more efficient and better for the plants.
-   **Hardware:** Add capacitive soil moisture sensors (which are more durable than resistive ones) connected to the analog-to-digital converter (ADC) pins on the Raspberry Pi Pico.
-   **Logic:**
    -   The Pico would periodically read the moisture level for each zone.
    -   In `schedule.py`, before a scheduled watering, check the corresponding sensor.
    -   If the soil moisture is above a certain threshold, skip the watering for that zone.
    -   Publish moisture levels to Home Assistant for monitoring and graphing.

## 2. Rain Detection via Weather API

-   **Concept:** Add a secondary, more reliable rain check by using a public weather API. This can predict rain and prevent watering *before* it even starts.
-   **Hardware:** No new hardware needed on the Pico.
-   **Logic:**
    -   In Home Assistant, create an automation that runs periodically (e.g., every hour).
    -   Use a weather integration (like OpenWeatherMap) to check the forecast for rain in the next few hours.
    -   If rain is predicted, the automation could send an MQTT message to a new topic like `pico/rain_forecast/set`.
    -   The Pico would subscribe to this topic. If it receives a "rain predicted" message, it would enter a delay state similar to the physical rain sensor logic. This provides a great fallback if the physical sensor fails.

## 3. Irrigation Logs

-   **Concept:** Keep a detailed history of when each zone was watered and for how long.
-   **Logic:**
    -   **On the Pico:** Modify the `run_zone` function in `relay_control.py`. After a zone finishes, publish an MQTT message to a topic like `pico/irrigation/log`. The payload would be a JSON string, e.g., `{"zone": 1, "duration_minutes": 10, "timestamp": "2023-10-27T06:10:00Z"}`.
    -   **In Home Assistant:**
        -   Create an MQTT sensor to listen to the `pico/irrigation/log` topic.
        -   Use the `logbook` integration or a custom database integration (like InfluxDB + Grafana) to store and visualize this data over time.

## 4. Mobile Access via Home Assistant Companion App

-   **Concept:** Control and monitor the irrigation system from anywhere using your phone.
-   **Implementation:**
    -   This is the easiest extension. Once Home Assistant is set up and accessible from outside your local network (using Nabu Casa or your own reverse proxy), the entire UI, including the irrigation dashboard, becomes available in the Home Assistant Companion App.
    -   You can receive notifications, manually trigger watering, and adjust schedules from your phone. 