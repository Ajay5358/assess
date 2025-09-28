from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import pandas as pd
import os

app = Flask(__name__)
DB_FILE = "weather.db"

def get_engine():
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError("❌ Database not found. Please run the data processing script first.")
    return create_engine(f'sqlite:///{DB_FILE}')

@app.route("/")
def home():
    return ("✅ Weather API is running!\n"
            "Usage:\n"
            "/weather/<year>\n"
            "/weather/<year>/<month>\n"
            "/weather/<year>/<month>/<day>\n"
            "Add ?page=X&limit=Y for pagination\n"
            "Stats:\n"
            "/weather/stats/<year>/<month>/<day>")

def validate_date(year, month=None, day=None):
    if month and (month < 1 or month > 12):
        return False, "❌ Month must be between 1 and 12."
    if day and (day < 1 or day > 31):
        return False, "❌ Day must be between 1 and 31."
    return True, ""

@app.route("/weather/<int:year>", defaults={'month': None, 'day': None})
@app.route("/weather/<int:year>/<int:month>", defaults={'day': None})
@app.route("/weather/<int:year>/<int:month>/<int:day>")
def get_weather(year, month, day):
    valid, msg = validate_date(year, month, day)
    if not valid:
        return jsonify({"error": msg}), 400

    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    offset = (page - 1) * limit

    query = "SELECT * FROM weather WHERE strftime('%Y', date)=:year"
    params = {'year': str(year)}
    if month:
        query += " AND strftime('%m', date)=:month"
        params['month'] = f"{month:02d}"
    if day:
        query += " AND strftime('%d', date)=:day"
        params['day'] = f"{day:02d}"

    engine = get_engine()
    df = pd.read_sql(query, engine, params=params)

    if df.empty:
        return jsonify({"error": "No data found"}), 404

    df_paginated = df.iloc[offset:offset+limit]
    return jsonify(df_paginated.to_dict(orient="records"))

@app.route("/weather/stats/<int:year>", defaults={'month': None, 'day': None})
@app.route("/weather/stats/<int:year>/<int:month>", defaults={'day': None})
@app.route("/weather/stats/<int:year>/<int:month>/<int:day>")
def get_stats(year, month, day):
    valid, msg = validate_date(year, month, day)
    if not valid:
        return jsonify({"error": msg}), 400

    query = "SELECT temperature, humidity, pressure, heat_index FROM weather WHERE strftime('%Y', date)=:year"
    params = {'year': str(year)}
    if month:
        query += " AND strftime('%m', date)=:month"
        params['month'] = f"{month:02d}"
    if day:
        query += " AND strftime('%d', date)=:day"
        params['day'] = f"{day:02d}"

    engine = get_engine()
    df = pd.read_sql(query, engine, params=params)

    if df.empty:
        return jsonify({"error": "No data found"}), 404

    stats = {
        "max_temp": df['temperature'].max(),
        "min_temp": df['temperature'].min(),
        "median_temp": float(df['temperature'].median()),
        "max_humidity": df['humidity'].max(),
        "min_humidity": df['humidity'].min(),
        "median_humidity": float(df['humidity'].median()),
        "max_pressure": df['pressure'].max(),
        "min_pressure": df['pressure'].min(),
        "median_pressure": float(df['pressure'].median()),
        "max_heat_index": df['heat_index'].max(),
        "min_heat_index": df['heat_index'].min(),
        "median_heat_index": float(df['heat_index'].median())
    }
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
