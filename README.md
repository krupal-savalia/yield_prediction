# Yield Prediction System

This project is a **Crop Yield Prediction System** that predicts the yield of a crop based on various parameters such as pH, rainfall, temperature, and other environmental factors. It also provides recommendations for suitable crops based on the input data.

---

## **Folder Structure**

Yield_prediction/ ├── crop_yield_ui.html # Frontend HTML file for user interaction ├── yield.py # Backend Flask application for predictions ├── data_fi;es/ # Folder containing the dataset │ └── Dataset.csv # Dataset used for training and predictions ├── random_forest.pkl # Trained Random Forest model for yield prediction ├── random_forest_recommend.pkl # Trained Random Forest model for crop recommendation └── README.md # Project documentation

---

## **Features**

1. **Crop Yield Prediction**:
   - Predicts the yield of a crop based on user inputs such as pH, rainfall, temperature, and area.

2. **Crop Recommendation**:
   - Recommends the most suitable crop for the given environmental conditions.

3. **Interactive Graphs**:
   - Displays graphs for pH, rainfall, temperature, and yield to help users visualize the data.

4. **Weather Integration**:
   - Fetches weather data (temperature, humidity, rainfall) using the OpenWeather API.

---

## **Technologies Used**

- **Frontend**: HTML, JavaScript, Chart.js
- **Backend**: Python, Flask
- **Machine Learning**: Random Forest (trained using `scikit-learn`)
- **Dataset**: CSV file containing crop data
- **Visualization**: Chart.js for interactive graphs

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd Yield_prediction
``` 

<h3>2. Install Dependencies</h3>
Install the required Python libraries:
```bash
pip install flask pandas joblib requests flask-cors matplotlib
```
<h3>3. Add the Dataset</h3>
Ensure the Dataset.csv file is placed in the data_fi;es/ folder.

<h3>4. Run the Flask Server</h3>
Start the backend server:
```bash
python [yield.py](http://_vscodecontentref_/4)
```
<h3>5. Open the Frontend</h3>
Open the crop_yield_ui.html file in your browser.

<h2>Usage</h2>
<h3>1. Crop Yield Prediction:</h3>

Enter the required parameters (state, season, crop type, pH, area, etc.).
Click on the "Predict Yield" button to get the predicted yield.
<h3>2.Crop Recommendation:</h3>

Enter the required parameters.
Click on the "Recommend Crop" button to get the recommended crop.
<h3>3.Graph Visualization:</h3>

View the interactive graphs for pH, rainfall, temperature, and yield under the result section.

<h2>Dataset</h2>
The dataset (Dataset.csv) contains the following columns:

Crop: Name of the crop
pH: Soil pH value
Rainfall: Rainfall in mm
Temperature: Temperature in °C
Yield: Crop yield in tons/hectare

<h2>Trained Models</h2>
1.random_forest.pkl:
A Random Forest model trained to predict crop yield.

2.random_forest_recommend.pkl:
A Random Forest model trained to recommend suitable crops.

<h2>Future Enhancements</h2>
Add more machine learning models for better accuracy.
Integrate additional environmental factors like soil type and sunlight.
Improve the frontend UI for better user experience.
