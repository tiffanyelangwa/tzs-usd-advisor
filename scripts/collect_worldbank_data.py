import os
import requests
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.collect_fred_data import MacroVariable

load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

WORLDBANK_INDICATORS = {
    "inflation": "FP.CPI.TOTL.ZG",
    "foreign_reserves": "FI.RES.TOTL.CD",
    "trade_balance": "BN.CAB.XOKA.CD",
    "remittances": "BX.TRF.PWKR.CD.DT",
    "tourism_receipts": "ST.INT.RCPT.CD"
}

def fetch_worldbank_indicator(indicator_code):
    url = f"https://api.worldbank.org/v2/country/TZ/indicator/{indicator_code}"
    params = {"format": "json", "per_page": 100}
    response = requests.get(url, params=params)
    data = response.json()
    return data[1]

def save_indicator(variable_name, indicator_code):
    session = Session()
    observations = fetch_worldbank_indicator(indicator_code)
    success = 0
    skipped_null = 0

    for obs in observations:
        if obs["value"] is None:
            skipped_null += 1
            continue
        year = int(obs["date"])
        if year < 2000:
            continue
        record_date = date(year, 6, 15)
        existing = session.query(MacroVariable).filter_by(
            date=record_date, variable_name=variable_name
        ).first()
        if not existing:
            record = MacroVariable(
                date=record_date,
                variable_name=variable_name,
                value=obs["value"],
                source=f"WorldBank_{indicator_code}"
            )
            session.add(record)
            success += 1

    session.commit()
    session.close()
    print(f"{variable_name}: inserted {success}, skipped {skipped_null} nulls")

if __name__ == "__main__":
    for variable_name, indicator_code in WORLDBANK_INDICATORS.items():
        save_indicator(variable_name, indicator_code)