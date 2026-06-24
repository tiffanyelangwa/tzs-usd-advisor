import os
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

df = pd.read_sql("SELECT * FROM exchange_rates ORDER BY date", engine)

print(df.head())
print(f"\nShape: {df.shape}")
print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nBasic stats:\n{df['usd_tzs'].describe()}")

fig = px.line(df, x="date", y="usd_tzs", title="USD/TZS Exchange Rate (2000-2024)")
fig.show()