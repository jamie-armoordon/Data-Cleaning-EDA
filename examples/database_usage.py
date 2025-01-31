import sys
import os

# Get the absolute path of the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (Data-Cleaning-EDA) and add it to sys.path
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import the functions from the database_manager module
from src.database_manager import load_data_from_api, insert_data_into_db, get_data_by_country, delete_all_data_from_db

# Main function to execute the database operations
if __name__ == "__main__":
    data = load_data_from_api("United Kingdom")
    if data:
        insert_data_into_db(data)
        uk_data = get_data_by_country("United Kingdom")
        print("Data inserted successfully")
        
