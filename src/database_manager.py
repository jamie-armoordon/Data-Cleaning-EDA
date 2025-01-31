# Importing libraries
import requests
import os
from dotenv import load_dotenv
import sqlite3

def connect_to_db():
    # Create the 'data' directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Construct the path to the database file within the 'data' directory
    db_path = os.path.join(data_dir, 'covid_data.db')

    # Setting up database connection
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Creating table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS covid_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT,
        region TEXT,
        date TEXT,
        total_cases INTEGER,
        new_cases INTEGER
    )''')

    return connection, cursor

def close_db_connection(connection, cursor):            
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    except sqlite3.Error as e:
        print(f"Error closing database connection: {e}")

def load_data_from_api(country):
    try:
        load_dotenv()
        api_url = 'https://api.api-ninjas.com/v1/covid19'
        api_key = os.getenv('ninja_api_key')
        if not api_key:
            raise ValueError("API key not found or empty.")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading API configuration: {e}")
        return None

    headers = {'X-Api-Key': api_key}
    params = {'country': country}

    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == requests.codes.ok:
        data = response.json()
        return data

    print(f"API request failed: Status Code: {response.status_code}, Response: {response.text}")
    return None

def insert_data_into_db(data):
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_db()
        for item in data:
            country = item['country']
            region = item['region']
            cases = item['cases']
            for date, case_data in cases.items():
                total_cases = case_data['total']
                new_cases = case_data['new']
                cursor.execute('INSERT INTO covid_data (country, region, date, total_cases, new_cases) VALUES (?, ?, ?, ?, ?)',
                               (country, region, date, total_cases, new_cases))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        if connection:
            close_db_connection(connection, cursor)

def update_data_in_db(data):
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_db()
        for item in data:
            cursor.execute('UPDATE covid_data SET total_cases = ?, new_cases = ? WHERE id = ?', (item['total_cases'], item['new_cases'], item['id']))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error updating data: {e}")
    finally:
        if connection:
            close_db_connection(connection, cursor)

def fetch_data_from_db(query, params=()):
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_db()
        cursor.execute(query, params)
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return None
    finally:
        if connection:
            close_db_connection(connection, cursor)
    
def get_data_by_country(country):
    query = "SELECT * FROM covid_data WHERE country = ?"
    return fetch_data_from_db(query, (country,))

def delete_data_from_db(query):
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_db()
        cursor.execute(query)
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error deleting data: {e}")
    finally:
        if connection:
            close_db_connection(connection, cursor)

def delete_all_data_from_db():
    delete_data_from_db('DELETE FROM covid_data')