import os
import requests
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.db_setup import ExchangeRate

load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def fetch_worldbank_tzs():
    url = "https://api.worldbank.org/v2/country/TZ/indicator/PA.NUS.FCRF"
    params = {"format": "json", "per_page": 100}
    response = requests.get(url, params=params)
    data = response.json()
    return data[1]

def collect_historical():
    session = Session()
    observations = fetch_worldbank_tzs()
    success = 0

    for obs in observations:
        if obs["value"] is None:
            continue
        year = int(obs["date"])
        if year < 2000:
            continue
        record_date = date(year, 6, 15)
        existing = session.query(ExchangeRate).filter_by(date=record_date).first()
        if not existing:
            record = ExchangeRate(
                date=record_date,
                usd_tzs=obs["value"],
                source="WorldBank_PA.NUS.FCRF"
            )
            session.add(record)
            success += 1
            print(f"{record_date}: {obs['value']}")

    session.commit()
    session.close()
    print(f"\nDone. Inserted: {success}")

collect_historical()

def collect_today():
    session = Session()
    url = "https://latest.currency-api.pages.dev/v1/currencies/usd.json"
    response = requests.get(url, timeout=10)
    data = response.json()
    rate = data["usd"]["tzs"]
    today = date.fromisoformat(data["date"])
    existing = session.query(ExchangeRate).filter_by(date=today).first()
    if not existing:
        record = ExchangeRate(date=today, usd_tzs=rate, source="fawazahmed0")
        session.add(record)
        session.commit()
        print(f"Today {today}: {rate}")
    else:
        print(f"Today already exists")
    session.close()

collect_today()