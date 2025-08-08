# 🌦 Weather API with Flask, Redis Caching, and Background Scheduler

A Flask-based API that fetches real-time weather data from the **Visual Crossing Weather API**, caches it in **Redis** to improve performance, and automatically updates the cache every 10 minutes using **APScheduler**.

---

## 📌 Features
- Fetch current weather data for any city.
- Caches results in **Redis** to reduce API calls.
- Background job updates cache automatically every 10 minutes.
- Handles API errors gracefully.
- Returns temperature in both **Celsius** and **Fahrenheit**.

---

## 🛠 Tech Stack
- **Flask** – Web framework
- **Redis** – In-memory caching
- **APScheduler** – Background task scheduler
- **Requests** – For HTTP requests to the Visual Crossing API
- **dotenv** – Environment variable management

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/weather-api.git
cd weather-api

```

### 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt

```

### 4️⃣ Set up environment variables
```bash
VISUAL_CROSSING_API_KEY=your_api_key_here

```

You can get your free api link - (https://www.visualcrossing.com/weather-api)

---

🗄 Redis Setup
Refer to this link -(https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/install-redis-on-windows/)
---

### ▶️ Running the App
```bash
python app.py
```

## Server will start at:
``` bash 
http://127.0.0.1:5000

```
### 🌍 API Usage
Endpoint:
```bash
GET /weather?city={city_name}
```

Example request:
```bash
GET http://127.0.0.1:5000/weather?city=London
```

Example response:
```bash
{
  "city": "london",
  "temperature": {
    "celsius": 28,
    "fahrenheit": 82.4
  },
  "condition": "Partially cloudy",
  "source": "Visual Crossing",
  "timestamp": "2025-08-08T10:00:00"
}
```


