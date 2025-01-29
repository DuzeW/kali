import requests
import os
import logging
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError



# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class HotelTool(BaseTool):
    name:str = "Hotel Tool"
    description:str = "Hotel tool helps you find hotels"
    api_key:str = os.getenv("GEOAPIFY_API_KEY")




    def _run(self) -> str:
        if not self.api_key:
            return str({"error": "Missing API key for hotels"})

        url = "https://api.geoapify.com/v2/places"
        params = {
            'categories': 'accommodation.hotel',
            'filter': 'rect:20.94752376937708,52.266861892301705,21.070476230619736,52.19628',
            'limit': '5',
            'apiKey': self.api_key,
        }

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                hotels = []

                for feature in data.get("features", []):
                    properties = feature.get("properties", {})
                    hotel_name = properties.get("name", "Unknown")
                    hotel_website = properties.get("website", "No website available")
                    hotel_stars = properties.get("accommodation", {}).get("stars", "Not rated")

                    hotels.append({
                        "hotel_name": hotel_name,
                        "hotel_website": hotel_website,
                        "hotel_stars": hotel_stars,
                    })

                # Return results as a stringified JSON
                return str(hotels)

            elif response.status_code == 401:
                logger.error("Invalid or inactive API key for hotel")
                return str({"error": "Hotel API authorization error - check your API key"})
            elif response.status_code == 404:
                logger.error("Location not found")
                return str({"error": "Hotel information not found for the city"})
            else:
                error_msg = f"Hotel API error ({response.status_code}): {response.text}"
                logger.error(error_msg)
                return str({"error": "Failed to fetch hotel information"})

        except Exception as e:
            logger.error(f"Error while fetching hotel: {str(e)}")
            return str({"error": "Error while fetching hotel information"})
