import pandas as pd
from sqlalchemy import create_engine
import sys
import os

def process_and_store(file_path, db_file="weather.db"):
    if not os.path.exists(file_path):
        print(f"❌ File {file_path} does not exist.")
        return

    # Load file
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file_path)
    else:
        print("❌ Unsupported file type. Use CSV or Excel.")
        return

    # Clean columns
    df.columns = df.columns.str.strip()
    df = df[['datetime_utc', '_tempm', '_hum', '_pressurem', '_heatindexm']]

    # Convert datetime
    df['datetime_utc'] = pd.to_datetime(df['datetime_utc'], errors='coerce')
    df = df.dropna(subset=['datetime_utc'])

    # Rename columns
    df.rename(columns={
        'datetime_utc': 'date',
        '_tempm': 'temperature',
        '_hum': 'humidity',
        '_pressurem': 'pressure',
        '_heatindexm': 'heat_index'
    }, inplace=True)

    # Store in SQLite
    engine = create_engine(f'sqlite:///{db_file}')
    df.to_sql('weather', engine, index=False, if_exists='replace')
    print(f"✅ Data successfully processed and stored in {db_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python processing.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    process_and_store(file_path)
