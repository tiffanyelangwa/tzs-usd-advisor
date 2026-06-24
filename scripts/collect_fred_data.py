import os
import requests
from datetime import date
from sqlalchemy import create_engine, Column, Float, Date, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")
FRED_API_KEY = os.getenv("FRED_API_KEY")

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class MacroVariable(Base):
    __tablename__ = "macro_variables"
    date = Column(Date, primary_key=True)
    variable_name = Column(String, primary_key=True)
    value = Column(Float, nullable=False)
    source = Column(String)

Base.metadata.create_all(engine)

def fetch_fred_series(series_id):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": "2000-01-01"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["observations"]

def save_observations(observations, variable_name, source):
    session = Session()
    success = 0
    for obs in observations:
        if obs["value"] == ".":
            continue
        record_date = date.fromisoformat(obs["date"])
        value = float(obs["value"])
        existing = session.query(MacroVariable).filter_by(
            date=record_date, variable_name=variable_name
        ).first()
        if not existing:
            record = MacroVariable(
                date=record_date,
                variable_name=variable_name,
                value=value,
                source=source
            )
            session.add(record)
            success += 1
    session.commit()
    session.close()
    print(f"{variable_name}: inserted {success} new records")

def collect_fed_funds():
    obs = fetch_fred_series("FEDFUNDS")
    save_observations(obs, "fed_funds_rate", "FRED_FEDFUNDS")

def collect_oil():
    obs = fetch_fred_series("DCOILWTICO")
    save_observations(obs, "oil_price_wti", "FRED_DCOILWTICO")

def collect_gold():
    response = requests.get("https://freegoldapi.com/data/latest.json")
    data = response.json()
    session = Session()
    success = 0
    for entry in data:
        record_date = date.fromisoformat(entry["date"])
        if record_date.year < 2000:
            continue
        existing = session.query(MacroVariable).filter_by(
            date=record_date, variable_name="gold_price"
        ).first()
        if not existing:
            record = MacroVariable(
                date=record_date,
                variable_name="gold_price",
                value=entry["price"],
                source="freegoldapi"
            )
            session.add(record)
            success += 1
    session.commit()
    session.close()
    print(f"gold_price: inserted {success} new records")

if __name__ == "__main__":
    collect_fed_funds()
    collect_oil()
    collect_gold()