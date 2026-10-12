import os
import zoneinfo
from datetime import datetime, timezone
from typing import Tuple, Dict, Any, Optional

def get_target_timezone() -> zoneinfo.ZoneInfo:
    """
    Get configured application timezone. Defaults to Asia/Kolkata
    to align with the target crop environment and user time zone.
    Falls back to UTC if the configured timezone is invalid.
    """
    tz_name = os.getenv("APP_TIMEZONE", "Asia/Kolkata")
    try:
        return zoneinfo.ZoneInfo(tz_name)
    except Exception:
        return zoneinfo.ZoneInfo("UTC")

def parse_thingspeak_timestamp(ts_str: str) -> Dict[str, Any]:
    """
    Parse an ISO 8601 timestamp string from ThingSpeak (e.g. '2026-10-12T16:57:11Z').
    Converts to target timezone and derives:
    - day: day of the month (1-31) matching the dataset's Day representation
    - hour: hour of the day (0-23)
    - minute: minute of the hour (0-59)
    - second: second of the minute (0-59)
    - time_in_hours: float time representation (hour + minute/60 + second/3600)
    """
    if not ts_str or not isinstance(ts_str, str):
        raise ValueError(f"Invalid timestamp: {ts_str}")
        
    normalized_ts = ts_str.strip()
    if normalized_ts.endswith("Z"):
        normalized_ts = normalized_ts[:-1] + "+00:00"
        
    try:
        dt_utc = datetime.fromisoformat(normalized_ts)
    except Exception as e:
        raise ValueError(f"Failed to parse ISO timestamp '{ts_str}': {e}")
        
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    else:
        dt_utc = dt_utc.astimezone(timezone.utc)
        
    target_tz = get_target_timezone()
    dt_local = dt_utc.astimezone(target_tz)
    
    day = dt_local.day
    hour = dt_local.hour
    minute = dt_local.minute
    second = dt_local.second
    time_in_hours = round(hour + (minute / 60.0) + (second / 3600.0), 4)
    
    return {
        "utc_datetime": dt_utc,
        "local_datetime": dt_local,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
        "time_in_hours": time_in_hours,
        "iso_timestamp": ts_str
    }

def calculate_freshness(dt_utc: datetime, threshold_seconds: Optional[float] = None) -> str:
    """
    Determines if telemetry data is 'LIVE' or 'STALE'.
    Free-tier ThingSpeak has a 15-20s upload interval.
    Default freshness window is 120 seconds.
    """
    if threshold_seconds is None:
        try:
            threshold_seconds = float(os.getenv("TELEMETRY_FRESHNESS_THRESHOLD_SECONDS", "120"))
        except (ValueError, TypeError):
            threshold_seconds = 120.0
            
    now_utc = datetime.now(timezone.utc)
    age_seconds = (now_utc - dt_utc).total_seconds()
    
    # Allow small clock skew (-60s to threshold)
    if -60.0 <= age_seconds <= threshold_seconds:
        return "LIVE"
    return "STALE"
