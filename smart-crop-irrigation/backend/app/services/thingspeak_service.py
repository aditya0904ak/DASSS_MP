import httpx
import os
import math
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ThingSpeakService:
    def __init__(self):
        pass

    @property
    def channel_id(self) -> str:
        return os.getenv("THINGSPEAK_CHANNEL_ID", "3523427")

    @property
    def api_key(self) -> str:
        return os.getenv("THINGSPEAK_READ_API_KEY", "").strip()

    @property
    def base_url(self) -> str:
        return f"https://api.thingspeak.com/channels/{self.channel_id}/feeds.json"

    def _fetch_data(self, results: int = 1):
        if not self.channel_id:
            raise ValueError("THINGSPEAK_CHANNEL_ID is not configured.")

        params = {"results": results}
        if self.api_key:
            params["api_key"] = self.api_key

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(self.base_url, params=params)
                
            if response.status_code == 404:
                raise ValueError("ThingSpeak channel not found. Check Channel ID.")
            if response.status_code == 400 and response.text.strip() == "-1":
                raise ValueError("ThingSpeak channel is private or invalid. Provide a valid THINGSPEAK_READ_API_KEY.")
            
            response.raise_for_status()
            data = response.json()
            return data.get("feeds", [])
            
        except httpx.TimeoutException:
            raise ConnectionError("Request to ThingSpeak timed out.")
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to fetch data from ThingSpeak: {e}")

    def _parse_feed(self, feed: dict):
        if not feed or not isinstance(feed, dict):
            return None

        created_at = feed.get("created_at")
        if not created_at or not isinstance(created_at, str) or not created_at.strip():
            return None

        # Verify timestamp is a valid ISO string
        ts_check = created_at.strip()
        if ts_check.endswith("Z"):
            ts_check = ts_check[:-1] + "+00:00"
        try:
            datetime.fromisoformat(ts_check)
        except Exception:
            return None

        field1 = feed.get("field1")
        field2 = feed.get("field2")
        field3 = feed.get("field3")
        field4 = feed.get("field4")
        
        if any(f is None or (isinstance(f, str) and not f.strip()) for f in [field1, field2, field3, field4]):
            return None
            
        try:
            soil_moisture = float(field1)
            temperature = float(field2)
            humidity = float(field3)
            light = float(field4)
            
            if not (math.isfinite(soil_moisture) and math.isfinite(temperature) and 
                    math.isfinite(humidity) and math.isfinite(light)):
                return None
                
        except (ValueError, TypeError):
            return None
        
        return {
            "timestamp": created_at,
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity,
            "light": light
        }

    def get_latest_data(self):
        feeds = self._fetch_data(results=5)
        if not feeds:
            raise ValueError("Empty response from ThingSpeak. No feeds available.")
            
        # Traverse in reverse to pick the newest valid feed
        for feed in reversed(feeds):
            parsed = self._parse_feed(feed)
            if parsed:
                return parsed
                
        raise ValueError("Invalid or missing sensor data in ThingSpeak response.")
        
    def get_history_data(self, results: int = 100):
        # Bound results between 1 and 8000 (ThingSpeak API limit)
        bounded_results = max(1, min(int(results), 8000))
        feeds = self._fetch_data(results=bounded_results)
        if not feeds:
            raise ValueError("Empty response from ThingSpeak. No feeds available.")
            
        parsed_feeds = []
        seen_timestamps = set()
        
        for feed in feeds:
            parsed = self._parse_feed(feed)
            if parsed:
                ts = parsed["timestamp"]
                if ts not in seen_timestamps:
                    seen_timestamps.add(ts)
                    parsed_feeds.append(parsed)
                
        if not parsed_feeds:
            raise ValueError("No valid historical data found in ThingSpeak response.")
            
        # Ensure chronological ordering (oldest to newest)
        parsed_feeds.sort(key=lambda x: x["timestamp"])
        return parsed_feeds

thingspeak_service = ThingSpeakService()
