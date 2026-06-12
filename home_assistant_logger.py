"""""
home_assistant_logger.py
-----------------------

This script retrieves specified sensor values from a Home Assistant instance and
appends them to a daily Markdown log file. Use this as part of an automation
to record environmental conditions (e.g., temperature, humidity) and personal
metrics (e.g., sleep duration, body battery) into your Obsidian vault.

Before running this script, update the `HOME_ASSISTANT_URL`, `TOKEN`, and
`SENSORS` dictionary with your own Home Assistant details and sensor entity IDs.

Example usage:
  python home_assistant_logger.py

Notes:
  - Ensure `requests` is installed (`pip install requests`).
  - The script appends to a file named `<YYYY-MM-DD>_environment_log.md` in
    the current working directory; adjust the path in `write_markdown` if
    needed.
"""

import datetime
import os
from typing import Dict

import requests


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# URL of your Home Assistant instance (e.g., http://homeassistant.local:8123)
HOME_ASSISTANT_URL: str = "http://homeassistant.local:8123"

# Long-lived access token created in your Home Assistant user profile.
# See: https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token
TOKEN: str = "YOUR_LONG_LIVED_TOKEN"

# Mapping of human‑friendly names to Home Assistant sensor entity IDs. Replace
# these with the actual entity IDs from your configuration. For example,
# 'sensor.humidity_sensor' should match the entity ID of your humidity sensor.
SENSORS: Dict[str, str] = {
    "temperature": "sensor.temperature_sensor",
    "humidity": "sensor.humidity_sensor",
    "sleep_duration": "sensor.sleep_duration",
    "body_battery": "sensor.body_battery",
    # Add your SmartThings climate entity below. Replace 'climate.samsung_aircon'
    # with the actual entity ID once the SmartThings integration is configured.
    "ac_status": "climate.samsung_aircon",
}


def get_sensor_state(sensor_id: str) -> str:
    """Retrieve the current state of a Home Assistant sensor via the REST API.

    Args:
        sensor_id: The entity_id of the sensor (e.g., 'sensor.temperature').

    Returns:
        The sensor's state as a string. If the request fails, returns
        'unknown'.
    """
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(
            f"{HOME_ASSISTANT_URL}/api/states/{sensor_id}", headers=headers, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("state", "unknown")
    except requests.RequestException as exc:
        print(f"Failed to retrieve {sensor_id}: {exc}")
        return "unknown"


def write_markdown(data: Dict[str, str], output_dir: str = ".") -> None:
    """Append sensor data to a daily Markdown file.

    Args:
        data: A mapping of sensor names to their current state values.
        output_dir: Directory where the log file will be written.
    """
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(output_dir, f"{date_str}_environment_log.md")
    lines = []
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    lines.append(f"## Log entry at {timestamp}\n")
    for name, value in data.items():
        lines.append(f"- **{name.replace('_', ' ').title()}**: {value}\n")
    lines.append("\n")
    with open(filename, "a", encoding="utf-8") as file:
        file.writelines(lines)
    print(f"Appended log to {filename}")


def main() -> None:
    """Fetch sensor states and append them to the daily log."""
    sensor_data = {name: get_sensor_state(sensor_id) for name, sensor_id in SENSORS.items()}
    write_markdown(sensor_data)


if __name__ == "__main__":
    main()
""