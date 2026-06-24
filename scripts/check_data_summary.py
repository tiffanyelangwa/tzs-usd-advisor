import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DB_URL"))

df = pd.read_sql("SELECT variable_name, COUNT(*) as records, MIN(date) as earliest, MAX(date) as latest FROM macro_variables GROUP BY variable_name", engine)
print(df)