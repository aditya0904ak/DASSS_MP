import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class ThingSpeakService:
    def __init__(self):
        self.channel_id = os.getenv("THINGSPEAK_CHANNEL_ID", "3523427")
        self.api_key = os.getenv("THINGSPEAK_READ_API_KEY", "")
        self.base_url = f"https://api.thingspeak.com/channels/{self.channel_id}/feeds.json"

    def get_latest_data(self):
        params = {"results": 1}
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
            
            feeds = data.get("feeds", [])
            if not feeds:
                raise ValueError("Empty response from ThingSpeak. No feeds available.")
            
            latest = feeds[0]
            
            # Map fields
            field1 = latest.get("field1")
            field2 = latest.get("field2")
            field3 = latest.get("field3")
            field4 = latest.get("field4")
            
            if any(f is None for f in [field1, field2, field3, field4]):
                raise ValueError("Missing sensor field in ThingSpeak response.")
                
            try:
                soil_moisture = float(field1)
                temperature = float(field2)
                humidity = float(field3)
                light = float(field4)
            except ValueError:
                raise ValueError("Invalid sensor value (not a float) in ThingSpeak response.")
            
            return {
                "timestamp": latest.get("created_at"),
                "soil_moisture": soil_moisture,
                "temperature": temperature,
                "humidity": humidity,
                "light": light
            }
            
        except httpx.TimeoutException:
            raise ConnectionError("Request to ThingSpeak timed out.")
        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to fetch data from ThingSpeak: {e}")
        except ValueError as e: # This catches json decoding error and our custom ValueErrors
            raise e
            
thingspeak_service = ThingSpeakService()
