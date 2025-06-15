# 📦 Enclosure Design & Safety Notes

A proper enclosure is critical for the safety and longevity of the outdoor components of the irrigation system (Pico, relays, and power wiring).

## 1. Safety First

-   **Water and Electricity Don't Mix:** The primary goal is to keep all electronic components completely dry.
-   **High Voltage:** The 24VAC circuit is high voltage. It must be fully enclosed and inaccessible without tools to prevent electric shock.
-   **Heat Dissipation:** Ensure the enclosure has some ventilation to prevent overheating, especially if it's in direct sunlight. However, ventilation openings must be designed to prevent water ingress (e.g., downward-facing louvers).

## 2. Recommended Enclosure

-   **NEMA 4X or IP67 Rated:** Use a certified weatherproof electrical junction box. These are designed to be watertight and are suitable for outdoor installation.
-   **Material:** UV-resistant plastic or fiberglass is ideal. A metal enclosure will also work but must be properly grounded.
-   **Cable Glands:** Use waterproof cable glands for all wires entering or exiting the box. This is the most common point of failure for water ingress. Each cable should have its own gland.

## 3. Internal Layout

-   **Mounting Plate:** Use a non-conductive mounting plate (e.g., a piece of plastic or perfboard) to attach the Pico and relay module inside the box. Avoid letting components rest at the bottom of the enclosure where condensation might collect.
-   **Strain Relief:** Secure all cables inside the box so that a tug on an external wire doesn't pull on the electrical connections.
-   **Separation:** Keep the 24VAC wiring physically separate from the low-voltage (5V/3.3V) Pico wiring as much as possible. Use different colored wires to avoid confusion.

## 4. Mounting Location

-   Mount the enclosure vertically on a wall or post.
-   Do not mount it in a location where it is likely to be submerged (e.g., in a ditch or low-lying area).
-   Choose a spot that is shaded from direct afternoon sun if possible to reduce internal temperatures.