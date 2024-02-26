from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import os
import json


from datetime import datetime

app = Flask(__name__)

# SQLite DB URL, adjust the path as necessary
DATABASE_URI = 'sqlite:///ppav_main.db'
# Uncomment to use it with the live data
# DATABASE_URI = "mariadb+mariadbconnector://power_admin:Oocheeth9ohmoo8ooc3oXeiy0nicheiZ@localhost:3306/power"


Base = declarative_base()


# Define the 'BiddingZone'
# CHANGE THIS TOA models.py file
class BiddingZone(Base):
    __tablename__ = 'bidding_zones'  # Updated table name

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


# HTTP authentication
# CHANGE IT FOR MORE SECURE


auth = HTTPBasicAuth()

with open(os.path.join(
            os.getcwd(),
            'credential.json'), 'r') as file:
    credential = json.load(file)

user = credential[0]['username']
pw = credential[0]['password']

users = {
    user: generate_password_hash(pw)
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route('/v1/table', methods=['POST'])
@auth.login_required
def load_data():
    try:
        # Extract multipart/form-data
        table = request.form['table']
        bidding_zone = request.form['bidding_zone']
        date_from = request.form['date_from']
        date_to = request.form['date_to']

        tables = ['actual_generation', 'installed_generation', 'crossborder_flows', 'day_ahead_price', 'load_forecast',
                  'system_total_load']

        if table not in tables: return jsonify({"error": "Table name invalid"}), 404

        # Create SQLAlchemy engine
        engine = create_engine(DATABASE_URI)
        Base.metadata.create_all(engine)

        # Create a session to interact with the database
        Session = sessionmaker(bind=engine)
        session = Session()

        zone = session.query(BiddingZone).filter_by(name=bidding_zone).first()

        if not zone:
            return jsonify({"error": "Bidding zone not found."}), 404

        bidding_zone_id = zone.id

        # Query to select relevant data based on the timeslot and bidding zone
        query = f"""
        SELECT * FROM {table}
        WHERE bidding_zone_id = '{bidding_zone_id}'
        AND timestamp BETWEEN '{date_from}' AND '{date_to}'
        """

        # Load data into pandas DataFrame
        df = pd.read_sql_query(query, engine)

        # Check if DataFrame is empty
        if df.empty:
            return jsonify({"error": "No data found for the given parameters."}), 404

        # Convert DataFrame to JSON
        result = df.to_json(orient="records")
        return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
