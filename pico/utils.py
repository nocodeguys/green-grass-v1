import ntptime
import time
import network
from config import MIN_ZONE, MAX_ZONE, MIN_DURATION, MAX_DURATION

def sync_time():
    """Syncs the Pico's RTC with an NTP server."""
    # Ensure Wi-Fi is connected before trying to sync
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        log("Error: Wi-Fi is not connected. Cannot sync time.")
        return False

    log("Syncing time with NTP server...")
    try:
        ntptime.settime()
        log("Time synced successfully.")
        return True
    except Exception as e:
        log(f"Error syncing time: {e}")
        return False

def log(message):
    """A simple logging function to print messages with a timestamp."""
    try:
        # Get current time tuple
        # (year, month, day, weekday, hours, minutes, seconds, subseconds)
        now = time.localtime()
        
        # Format the timestamp
        timestamp = f"{now[0]:04d}-{now[1]:02d}-{now[2]:02d} {now[3]:02d}:{now[4]:02d}:{now[5]:02d}"
        
        print(f"[{timestamp}] {message}")
    except Exception:
        # Fallback in case time is not set properly
        print(f"[TIME_ERROR] {message}")

def validate_schedule_data(schedule_data):
    """Validates schedule data structure."""
    if not isinstance(schedule_data, dict):
        log("Schedule validation failed: not a dictionary")
        return False
    
    if "schedule" not in schedule_data:
        log("Schedule validation failed: missing 'schedule' key")
        return False
    
    if not isinstance(schedule_data["schedule"], list):
        log("Schedule validation failed: 'schedule' is not a list")
        return False
    
    for i, job in enumerate(schedule_data["schedule"]):
        if not isinstance(job, dict):
            log(f"Schedule validation failed: job {i} is not a dictionary")
            return False
            
        required_keys = ["zone", "hour", "minute", "duration"]
        if not all(key in job for key in required_keys):
            missing_keys = [key for key in required_keys if key not in job]
            log(f"Schedule validation failed: job {i} missing keys: {missing_keys}")
            return False
            
        if not all(isinstance(job[key], int) for key in required_keys):
            log(f"Schedule validation failed: job {i} has non-integer values")
            return False
            
        if not (MIN_ZONE <= job["zone"] <= MAX_ZONE):
            log(f"Schedule validation failed: job {i} zone {job['zone']} out of range ({MIN_ZONE}-{MAX_ZONE})")
            return False
            
        if not (0 <= job["hour"] <= 23):
            log(f"Schedule validation failed: job {i} hour {job['hour']} out of range (0-23)")
            return False
            
        if not (0 <= job["minute"] <= 59):
            log(f"Schedule validation failed: job {i} minute {job['minute']} out of range (0-59)")
            return False
            
        if not (MIN_DURATION <= job["duration"] <= MAX_DURATION):
            log(f"Schedule validation failed: job {i} duration {job['duration']} out of range ({MIN_DURATION}-{MAX_DURATION})")
            return False
    
    log(f"Schedule validation passed: {len(schedule_data['schedule'])} jobs validated")
    return True

def get_system_status():
    """Returns current system status information."""
    import gc
    
    return {
        "free_memory": gc.mem_free(),
        "allocated_memory": gc.mem_alloc(),
        "uptime_seconds": time.time(),
        "local_time": time.localtime()
    }