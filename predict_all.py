import pandas as pd
import requests
from io import BytesIO
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.preprocessing import StandardScaler

PLANT_LOCATIONS = {
    "BHUSAWAL TPS": {"lat": 21.05, "lon": 75.78},
    "CHANDRAPUR(MAHARASHTRA) STPS": {"lat": 19.95, "lon": 79.30},
    "KHAPARKHEDA TPS": {"lat": 21.28, "lon": 79.10},
    "KORADI TPS": {"lat": 21.17, "lon": 79.12},
    "NASIK TPS": {"lat": 19.98, "lon": 73.73},
    "PARAS TPS": {"lat": 20.70, "lon": 76.83},
    "PARLI TPS": {"lat": 18.85, "lon": 76.53},
    "URAN CCPP": {"lat": 18.88, "lon": 72.93},
    "BHIRA TAIL RACE HPS": {"lat": 18.46, "lon": 73.40},
    "GHATGHAR HPS": {"lat": 19.42, "lon": 73.75},
    "KOYNA DPH HPS": {"lat": 17.40, "lon": 73.75},
    "KOYNA-I&II HPS": {"lat": 17.40, "lon": 73.75},
    "KOYNA-III HPS": {"lat": 17.40, "lon": 73.75},
    "KOYNA-IV HPS": {"lat": 17.40, "lon": 73.75},
    "PENCH HPS": {"lat": 21.65, "lon": 79.25},
    "TILLARI HPS": {"lat": 15.80, "lon": 74.00},
    "VAITARNA HPS": {"lat": 19.63, "lon": 73.35},
    "ADANI POWER LIMITED TIRODA TPP": {"lat": 21.40, "lon": 79.65},
    "AMRAVATI TPS": {"lat": 20.93, "lon": 77.75},
    "BELA TPS": {"lat": 21.18, "lon": 79.05},
    "BUTIBORI TPP": {"lat": 20.93, "lon": 79.00},
    "DAHANU TPS": {"lat": 19.97, "lon": 72.73},
    "DHARIWAL TPP": {"lat": 21.10, "lon": 79.30},
    "GEPL TPP Ph-I": {"lat": 20.95, "lon": 79.00},
    "GMR WARORA TPS": {"lat": 20.23, "lon": 79.00},
    "JSW RATNAGIRI TPP": {"lat": 16.98, "lon": 73.30},
    "LANCO VIDARBHA TPP": {"lat": 20.40, "lon": 78.90},
    "MIHAN TPS": {"lat": 20.85, "lon": 79.05},
    "NASIK (P) TPS": {"lat": 19.98, "lon": 73.73},
    "SHIRPUR TPP": {"lat": 21.35, "lon": 74.90},
    "TROMBAY TPS": {"lat": 19.00, "lon": 72.90},
    "WARDHA WARORA TPP": {"lat": 20.25, "lon": 79.00},
    "MANGAON CCPP": {"lat": 18.20, "lon": 73.25},
    "TROMBAY CCPP": {"lat": 19.00, "lon": 72.90},
    "BHANDARDHARA HPS ST-II": {"lat": 19.53, "lon": 73.75},
    "BHIRA HPS": {"lat": 18.46, "lon": 73.40},
    "BHIRA PSS HPS": {"lat": 18.46, "lon": 73.40},
    "BHIVPURI HPS": {"lat": 18.97, "lon": 73.33},
    "KHOPOLI HPS": {"lat": 18.78, "lon": 73.33},
    "MAUDA TPS": {"lat": 21.18, "lon": 79.05},
    "SOLAPUR STPS": {"lat": 17.65, "lon": 75.90},
    "RATNAGIRI CCPP": {"lat": 16.98, "lon": 73.30},
    "TARAPUR": {"lat": 19.85, "lon": 72.68}
}

API_KEY = "your-api-key"

def fetch_day(date):
    url = f"https://npp.gov.in/public-reports/cea/daily/dgr/{date.strftime('%d-%m-%Y')}/dgr2-{date.strftime('%Y-%m-%d')}.xls"
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            return pd.read_excel(BytesIO(r.content), engine="xlrd")
    except:
        return None


def extract_plants(df):
    df = df.copy()
    mask1 = df["Unnamed: 0"].astype(str).str.contains("MAHARASHTRA", na=False)
    mask2 = df["Unnamed: 0"].astype(str).str.contains("SOUTHERN", na=False)
    if not mask1.any() or not mask2.any():
        return None
    df = df[df.index[mask1][0]:df.index[mask2][0]]
    df = df.rename(columns={"Unnamed: 0": "Plant"})
    df = df[["Plant", "Unnamed: 7", "Unnamed: 8", "Unnamed: 9"]]
    df.columns = ["Plant", "Capacity", "Expected", "Production"]
    df = df.dropna(subset=["Plant"])
    return df


def get_weather(lat, lon):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        r = requests.get(url, params={
            "lat": lat,
            "lon": lon,
            "appid": "8c6a0dc8bc4dedf1be4a3504df8eb372",
            "units": "metric"
        }, timeout=10).json()

        return {
            "temp": r["main"]["temp"],
            "humidity": r["main"]["humidity"],
            "wind": r["wind"]["speed"]
        }
    except:
        return None

def get_weather_forecast(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    r = requests.get(url, params={
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }).json()
    tomorrow = datetime.utcnow() + timedelta(days=1)
    closest = min(
        r["list"],
        key=lambda x: abs(datetime.utcfromtimestamp(x["dt"]) - tomorrow)
    )
    return {
        "temp": closest["main"]["temp"],
        "humidity": closest["main"]["humidity"],
        "wind": closest["wind"]["speed"]
    }


def match_plant(name):
    name = name.lower()
    for plant in PLANT_LOCATIONS:
        if plant.lower() in name:
            return plant
    return None


def build_dataset():
    plant_data = {}
    for i in range(4, 35):
        date = datetime.today() - timedelta(days=i)
        df = fetch_day(date)
        if df is None:
            continue
        plants = extract_plants(df)
        if plants is None:
            continue
        for _, row in plants.iterrows():
            name = str(row["Plant"]).strip()
            if name not in PLANT_LOCATIONS:
                continue
            weather = get_weather(**PLANT_LOCATIONS[name])
            if weather is None:
                continue
            entry = {
                "Capacity": row["Capacity"],
                "Expected": row["Expected"],
                "Production": row["Production"],
                **weather
            }
            plant_data.setdefault(name, []).append(entry)
        print(i-3)
    return plant_data


def predict_all():
    plant_data = build_dataset()
    results = {}
    for plant, records in plant_data.items():
        df = pd.DataFrame(records).dropna()
        if len(df) < 3:
            continue
        X = df[["temp", "humidity", "wind", "Capacity", "Expected"]]
        y = df["Production"]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = LinearRegression()
        model.fit(X_scaled, y)
        weather = get_weather_forecast(**PLANT_LOCATIONS[plant])
        last = df.iloc[-1]
        sample = np.array([[
            weather["temp"],
            weather["humidity"],
            weather["wind"],
            last["Capacity"],
            last["Expected"]
        ]])
        sample_scaled = scaler.transform(sample)
        pred = model.predict(sample_scaled)[0]
        pred = min(max(round(pred, 2), 0), last["Capacity"])
        results[plant] = pred
    return results
