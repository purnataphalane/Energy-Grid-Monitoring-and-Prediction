import pandas as pd
import requests
from io import BytesIO
from datetime import datetime, timedelta


def find_latest_dgr(max_days_back=30):
    BASE_URL = "https://npp.gov.in/public-reports/cea/daily/dgr/{folder}/dgr2-{file}.xls"
    date = datetime.today()

    for _ in range(max_days_back):
        folder = date.strftime("%d-%m-%Y")
        file = date.strftime("%Y-%m-%d")

        url = BASE_URL.format(folder=folder, file=file)
        r = requests.get(url, timeout=30)

        if r.status_code == 200 and len(r.content) > 1000:
            return date, r


        date -= timedelta(days=1)


def fetch():
    date, response = find_latest_dgr()
    data = pd.read_excel(BytesIO(response.content), engine="xlrd")  
    mask1 = (
        data["Unnamed: 0"]
        .astype(str)
        .str.upper()
        .str.contains("MAHARASHTRA", na=False)
    )
    mask2 = (
        data["Unnamed: 0"]
        .astype(str)
        .str.upper()
        .str.contains("SOUTHERN", na=False)
    )
    data = data[data.index[mask1][0]:data.index[mask2][0]]
    cols = ["Unnamed: 4", "Unnamed: 7", "Unnamed: 8", "Unnamed: 9", "Unnamed: 13"]
    rows = (
        data["Unnamed: 0"]
        .astype(str)
        .str.contains(r"\b(Sector|Type)\b", case=False, na=False)
    )
    cleaned = data.loc[rows, cols]
    cleaned.columns = ["Type", "Capacity", "Expected", "Production", "Unavailable Capacity"]
    cleaned = cleaned.where(pd.notnull(cleaned), None)
    json_data = cleaned.to_dict(orient="records")
    json_data.append({"date": date.strftime("%d-%m-%Y")})
    return json_data
