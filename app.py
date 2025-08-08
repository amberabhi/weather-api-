from flask import Flask, request, jsonify
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import os 
import requests
import redis
import json

#it brings environment variables into this file
load_dotenv()

app = Flask(__name__)

API_KEY =  os.getenv("VISUAL_CROSSING_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

#redis connection
redis_client = redis.Redis(host="localhost",port=6379, db=0)
CACHE_EXPIRATION = 600 #TTL - Time to live

#---------------------Flask endpoint ---------------------
@app.route("/weather", methods=['GET'])
def get_weather():
    city = request.args.get("city", "London").lower()

    if not API_KEY:
        return jsonify({"error": "API key not set"}), 500
    
    # extracting data from redish if present and returning it 
    refresh = request.args.get("refresh", "false").lower() == "true"

    if not refresh:
        cached_data = redis_client.get(city)
        if cached_data :
            print("Already in redish")
            return jsonify(json.loads(cached_data)), 200
    
    try:
        url = f"{BASE_URL}/{city}?unitGroup=metric&key={API_KEY}&contentType=json"

        response = requests.get(url, timeout = 5) #requests is used to fetch response from the url 
        response.raise_for_status() # for bad responses

        data = response.json()

        current_conditions = data.get("currentConditions", {})

        weather_info = {
            "city": city,
            "temperature": {
                "celsius": current_conditions.get("temp"),
                "fahrenheit": current_conditions.get("temp") * 9/5 + 32 if current_conditions.get("temp") else None
            },
            "condition": current_conditions.get("conditions"),
            "source": "Visual Crossing",
            "timestamp": current_conditions.get("datetime")
        }

        # save it in cache if not present 
        redis_client.setex(city, CACHE_EXPIRATION, json.dumps(weather_info))

        return jsonify(weather_info), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 502

# refresh cache 
def refreshed_cache_weather():
    keys = redis_client.get("*")
    for key in keys:
        city = key.decode("utf-8")
        try:
            url = f"{BASE_URL}/{city}?unitGroup=metric&key={API_KEY}&contentType=json"
            response = requests.get(url, timeout = 5) #requests is used to fetch response from the url 
            response.raise_for_status() # for bad responses

            data = response.json()

            current_conditions = data.get("currentConditions", {})

            weather_info = {
                "city": city,
                "temperature": {
                    "celsius": current_conditions.get("temp"),
                    "fahrenheit": current_conditions.get("temp") * 9/5 + 32 if current_conditions.get("temp") else None
                },
                "condition": current_conditions.get("conditions"),
                "source": "Visual Crossing",
                "timestamp": current_conditions.get("datetime")
            }

            # save it in cache if not present 
            redis_client.setex(city, CACHE_EXPIRATION, json.dumps(weather_info))
            print(f"✅ Cache refreshed for {city}")

        except Exception as e:
            return jsonify({"error": str(e)}), 502


scheduler = BackgroundScheduler()
scheduler.add_job(refreshed_cache_weather, 'interval', minutes=10)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)