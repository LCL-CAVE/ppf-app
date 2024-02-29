import requests
import pandas as pd
from datetime import datetime
from io import StringIO


def serve_api_callback(url, username, password, payload):
    # Send authenticated request to the API
    response = requests.post(url, auth=(username, password), data=payload)

    # Check if request was successful
    if response.status_code == 200:
        # Convert JSON response to Pandas DataFrame
        df = pd.read_json(StringIO(response.text))

        # Convert 'timestamp' column to Pandas datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Display the DataFrame
        return df

    else:
        print(f"Error: {response.status_code} - {response.text}")
