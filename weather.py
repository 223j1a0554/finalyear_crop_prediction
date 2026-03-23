import requests

def get_weather(lat, lon):

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"

    response = requests.get(url)
    data = response.json()

    # temperature
    temperature = data.get("current_weather", {}).get("temperature", 30)

    # rainfall (default if missing)
    rainfall = data.get("hourly", {}).get("precipitation", [0])[0]

    # humidity
    humidity = data.get("hourly", {}).get("relativehumidity_2m", [50])[0]

    return rainfall, temperature, humidity