import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Column, Float, Date, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

load_dotenv()

DB_URL = "postgresql://postgres:peanutbutt@localhost:5432/tzs_platform"

engine = create_engine(DB_URL)
Base = declarative_base()

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    
    date = Column(Date, primary_key=True)
    usd_tzs = Column(Float, nullable=False)
    source = Column(String, default="fawazahmed0")
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
print("Tables created successfully")