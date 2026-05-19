# ⚡ Maharashtra Energy Production Prediction

This project predicts **next-day energy production** for major power plants in Maharashtra using:

* Historical generation data (CEA reports)
* Weather data (OpenWeather API)
* Machine Learning (Linear Regression)

---

## 🚀 Features

* 📊 Fetches daily generation reports from CEA
* 🌦️ Integrates real-time & forecast weather data
* 🤖 Trains a regression model per plant
* 🔮 Predicts **next-day power production**
* 🧠 Handles multiple power plants dynamically

---

## 🗂️ Project Structure

```
.
├── Backend/
│   ├── main.py
│   ├── fetch_data.py
│   └── predict_all.py
│
├── Frontend/
│   ├── index.html
│   └── predict_all.html
│
├── LICENSE
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone <your-repo-url>
cd <your-project-folder>
```

---

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 🔑 API Setup

This project uses OpenWeather API.

1. Get API key from: https://openweathermap.org/api
2. Replace in code:

```
"appid": "YOUR_API_KEY"
```

---

## ▶️ Usage

Run the main script:

```
python Backend/main.py
```
Run Frontend/index.html
---

## 🧠 How It Works

### 1. Data Collection

* Fetches past few days of plant data from CEA
* Extracts:

  * Capacity
  * Expected generation
  * Actual production

### 2. Weather Integration

* Historical weather → used for training
* Forecast weather → used for prediction

### 3. Model Training

* Features:

  * Temperature
  * Humidity
  * Wind speed
  * Capacity
  * Expected generation

* Model:

  * Linear Regression

### 4. Prediction

* Uses **next-day forecast weather**
* Combines with latest plant data
* Outputs production estimate

---

## ⚠️ Known Limitations

* Assumes linear relationships
* Weather impact may be limited for thermal plants
* Depends on external APIs (CEA + OpenWeather)

---

## 🚀 Future Improvements

* Cache API responses (performance boost)
* Try advanced models (Random Forest, XGBoost)
* Add time-series modeling
* Build dashboard for visualization

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Priyank Sharma
Internship Project – Energy Prediction System

---

## ⭐ Support

If you found this useful, consider giving it a star ⭐
