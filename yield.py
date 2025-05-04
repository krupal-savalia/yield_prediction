from flask import Flask, request, jsonify
import joblib 
import requests  
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

df = pd.read_csv("data_fi;es\Dataset.csv")
df = df.drop(columns=["Unnamed: 0", "State", "Season", "N", "P", "K", "Area", "Production", "Crop_code"])
df = df.dropna()
model = joblib.load("random_forest.pkl")
model2 = joblib.load("random_forest_recommend.pkl")
model_columns = model2.feature_names_in_
model_columns = model_columns.tolist()


OPENWEATHER_API_KEY = "29911d2bc1432cefd2b2a35c15c7129f"


def get_weather_data(state, season):
   
    season_months = {
        "rabi": [11, 12, 1, 2],
        "summer": [3, 4, 5, 6],
        "kharif": [7, 8, 9, 10],
        "whole year":  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }
    
    if season.lower() not in season_months:
        return None
    
    avg_temperature = 0
    avg_humidity = 0
    avg_rainfall = 0
    count = 0
    
    for month in season_months[season.lower()]:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={state}&month={month}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            avg_temperature += data["main"]["temp"]
            avg_humidity += data["main"]["humidity"]
            avg_rainfall += data.get("rain", {}).get("year", 0)  
            count += 1
    
    if count == 0:
        return None
    
    return {
        "temperature": avg_temperature / count,
        "humidity": avg_humidity / count,
        "rainfall": avg_rainfall / count
    }

@app.route("/predict", methods=["POST"])
def predict_yield():
    try:

        user_input = request.json
        state = user_input.get("state")
        season = user_input.get("season")
        crop_type = user_input.get("crop_type")
        nitrogen = float(user_input.get("nitrogen"))
        phosphorus = float(user_input.get("phosphorus"))
        potassium = float(user_input.get("potassium"))
        ph = float(user_input.get("ph"))
        area = float(user_input.get("area"))


        weather = get_weather_data(state, season)
        if not weather:
            return jsonify({"error": "Weather data not found for the given state and season"}), 400
        print(weather)
        temperature = weather["temperature"]
        humidity = weather["humidity"]
        rainfall = weather["rainfall"]
        

        data = {
            "Nitrogen (N)": [nitrogen],
            "Phosphorus (P)": [phosphorus],
            "Potassium (K)": [potassium],
            "pH": [ph],
            "Rainfall (mm)": [rainfall],
            "Temperature (°C)": [temperature],
            "Humidity (%)": [humidity],
            "Crop_l": [crop_type]
        }
        features = pd.DataFrame(data)
        predicted_yield = model.predict(features)
        print(predicted_yield)

        crop_mapping = {
            4: "Rice",
            6: "Wheat",
            10: "Maize",
            7: "Barley",
            8: "Sorghum",
            2: "Pearl Millet",
            3: "Chickpea",
            11: "Lentil",
            1: "Pigeon Pea",
            12: "Peanut",
            14: "Mustard",
            15: "Soyabean",
            16: "Sunflower",
            5: "Sugarcane",
            9: "Cotton",
            0: "Potato",
            17: "Tomato",
            13: "Onion"
        }
        crop_type = crop_mapping.get(crop_type)
        crop_data = get_data(crop_type)
        if crop_data:
            print(True)

        return jsonify({
            "predicted_yield": predicted_yield[0],
            "chart_data": crop_data
        })

    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({"error": str(e)})

@app.route('/recommend_crop', methods=['POST'])
def recommend_crop():
    try:
        user_input = request.json
        state = user_input.get("state")
        season = user_input.get("season")
        crop_type = user_input.get("crop_type")
        nitrogen = float(user_input.get("nitrogen"))
        phosphorus = float(user_input.get("phosphorus"))
        potassium = float(user_input.get("potassium"))
        ph = float(user_input.get("ph"))
        area = float(user_input.get("area"))
     
        data = {
            "State": state,
            "Season": season,
            "N": nitrogen,
            "P": phosphorus,
            "K": potassium,
            "pH": ph            
        }
        def prepare_input(user_input_dict):

            input_df = pd.DataFrame([user_input_dict])
            input_df = pd.get_dummies(input_df)
            input_df = input_df.reindex(columns=model_columns, fill_value=0)
            
            return input_df
        
        features = prepare_input(data)
        pred_crop = model2.predict(features)
        crop_mapping = {
            15: "cotton",
            20: "horsegram",
            22: "jowar",
            25: "maize",
            27: "moong",
            34: "ragi",
            36: "rice",
            39: "sunflower",
            44: "wheat",
            37: "sesamum",
            38: "soyabean",
            35: "rapeseed",
            23: "jute",
            0: "arecanut",
            28: "onion",
            32: "potato",
            40: "sweetpotato",
            41: "tapioca",
            43: "turmeric",
            2: "barley",
            1: "banana",
            14: "coriander",
            17: "garlic",
            5: "blackpepper",
            9: "cardamom",
            11: "cashewnuts",
            4: "blackgram",
            13: "coffee",
            24: "ladyfinger",
            7: "brinjal",
            19: "grapes",
            26: "mango",
            29: "orange",
            30: "papaya",
            42: "tomato",
            31: "pineapple",
            10: "carrot",
            33: "radish",
            16: "drumstick",
            21: "jackfruit",
            8: "cabbage",
            12: "cauliflower",
            3: "bittergourd",
            6: "bottlegourd",
            18: "ginger"
        }
        predicted_crop = crop_mapping.get(pred_crop[0])
        print(predicted_crop)

        crop_data = get_data(predicted_crop)

        return jsonify({
            "predicted_crop": predicted_crop,
            "chart_data": crop_data
        })

    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({"error": str(e)})

def get_data(crop_type):
    try:
        if crop_type:
            filtered_df = df[df["Crop"] == crop_type.lower()]
            filtered_df = filtered_df.drop(columns=["Crop"])
        else:
            filtered_df = df
        
        data = filtered_df.to_dict(orient="split")
        return data
    except Exception as e:
        print("Error fetching data:", str(e))
        return []
        
if __name__ == "__main__":
    app.run(debug=True)

