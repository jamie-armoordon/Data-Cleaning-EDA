#Importing libraries
import requests
import os
from dotenv import load_dotenv
import sqlite3

def connect_to_db():    
    #Setting up database connection
    connection = sqlite3.connect('covid_data.db')
    cursor = connection.cursor()

    #Creating table if it doesnt exist
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
        connection.close()
        cursor.close() 
    except sqlite3.Error as e:
        print(f"Error closing database connection: {e}")

def load_data_from_api():
    try:
        load_dotenv()
        api_url = 'https://api.api-ninjas.com/v1/covid19'
        api_key = os.getenv('ninja_api_key')
    except Exception as e:
        print("Error loading environment variables or API key")
        return None

    headers = {
        'X-Api-Key': api_key
    }

    params = {
        'country': 'United Kingdom'  
    }

    #Sending request to API
    response = requests.get(api_url, headers=headers, params=params)

    #Checking if request was successful
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None

def insert_data_into_db(data):
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_db()
        for item in data:
            cursor.execute('INSERT INTO covid_data (country, region, date, total_cases, new_cases) VALUES (?, ?, ?, ?, ?)', (item['country'], item['region'], item['date'], item['total_cases'], item['new_cases']))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
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
        close_db_connection(connection, cursor)


def fetch_data_from_db(query):
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_db()
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
    finally:
        close_db_connection(connection, cursor)
    

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
        close_db_connection(connection, cursor)

def delete_all_data_from_db():
    delete_data_from_db('DELETE FROM covid_data')   

