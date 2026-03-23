from flask import Flask, render_template, request
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from water_check import check_water_source
from weather import get_weather
from model import predict_crop_suitability, get_suitable_crops
import os

app = Flask(__name__)

# Load trained model
model = load_model("model.h5")

# Load encoders
with open("encoders.pkl", "rb") as f:
    y_encoder = pickle.load(f)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():

    # Form inputs
    crop = request.form['crop'].lower()
    soil = request.form['soil'].lower()
    season = request.form['season'].lower()
    lat = float(request.form['latitude'])
    lon = float(request.form['longitude'])

    # -----------------------------
    # 🌱 Soil → NPK mapping
    # -----------------------------
    soil_npk = {
        "clay": [90, 40, 40],
        "loamy": [80, 50, 50],
        "red": [60, 30, 30],
        "black": [70, 35, 35],
        "alluvial": [85, 45, 45]
    }

    N, P, K = soil_npk.get(soil, [70, 40, 40])

    # -----------------------------
    # 🌱 Soil → pH mapping
    # -----------------------------
    soil_ph = {
        "clay": 7.5,
        "loamy": 6.8,
        "red": 6.5,
        "black": 7.2,
        "alluvial": 7.0
    }

    ph = soil_ph.get(soil, 7)

    # -----------------------------
    # 💧 Water availability
    # -----------------------------
    water_status, distance = check_water_source(lat, lon)

    if water_status not in ["Good", "Moderate", "Poor"]:
        water_status = "Poor"

    water_map = {"Poor": 1, "Moderate": 2, "Good": 3}
    water_level = water_map.get(water_status, 1)

    # -----------------------------
    # 🌦 Weather API
    # -----------------------------
    rainfall, temperature, humidity = get_weather(lat, lon)

    if rainfall < 50:
        rainfall_model = 20
        rainfall_level = 1
    elif rainfall < 100:
        rainfall_model = 80
        rainfall_level = 2
    else:
        rainfall_model = 120
        rainfall_level = 3

    # -----------------------------
    # 🤖 Model Input
    # -----------------------------
    input_data = [N, P, K, temperature, humidity, ph, rainfall_model]
    input_array = np.array(input_data, dtype=np.float32).reshape(1, -1)

    # -----------------------------
    # 🔮 Prediction
    # -----------------------------
    prediction = model.predict(input_array)
    predicted_class = np.argmax(prediction)
    result = y_encoder.inverse_transform([predicted_class])[0]

    # -----------------------------
    # 📊 Suitability
    # -----------------------------
    suitability = predict_crop_suitability(crop, season, soil, water_level)

    # 👉 Get ALL suitable crops
    suitable_crops = get_suitable_crops(season, soil, water_level)

    # 👉 Ensure prediction is from suitable crops
    if result not in suitable_crops and suitable_crops:
        result = suitable_crops[0]

    # -----------------------------
    # 🌾 Recommendation Logic (UPDATED)
    # -----------------------------
    if not suitable_crops:
        suitable_crops = [result]
    if crop == result:
        message = f"{crop} is suitable for this land."
        recommended_crops = suitable_crops

    elif crop in suitable_crops:
        message = f"{crop} can grow, but {result} might perform better ⚠️"
        recommended_crops = suitable_crops

    else:
        message = f"{crop} is not suitable .Recommended crops are:"
        recommended_crops = suitable_crops

    # -----------------------------
    # 🚀 Send to frontend
    # -----------------------------
    return render_template(
        "result.html",
        result=result,
        rainfall=rainfall_level,
        temperature=temperature,
        humidity=humidity,
        water_status=water_level,
        message=message,
        recommended_crops=recommended_crops,
        lat=lat,
        lon=lon,
        distance=distance,
        water_available=(water_level > 1)
    )
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))