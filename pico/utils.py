import ntptime
import time
import network

def sync_time():
    """Syncs the Pico's RTC with an NTP server."""
    # Ensure Wi-Fi is connected before trying to sync
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Error: Wi-Fi is not connected. Cannot sync time.")
        return False

    print("Syncing time with NTP server...")
    try:
        ntptime.settime()
        print("Time synced successfully.")
        return True
    except Exception as e:
        print(f"Error syncing time: {e}")
        return False

def log(message):
    """A simple logging function to print messages with a timestamp."""
    # Get current time tuple
    # (year, month, day, weekday, hours, minutes, seconds, subseconds)
    now = time.localtime()
    
    # Format the timestamp
    timestamp = f"{now[0]:04d}-{now[1]:02d}-{now[2]:02d} {now[3]:02d}:{now[4]:02d}:{now[5]:02d}"
    
    print(f"[{timestamp}] {message}")