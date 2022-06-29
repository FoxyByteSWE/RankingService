import mysql.connector
from mysql.connector import Error
import pandas as pd


# Functions
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Success")
    except Error as err:
        print(f"Error: '{err}'")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

# Queries
drop_tables = "DROP TABLE IF EXISTS Restaurants"
create_restaurants = """CREATE TABLE IF NOT EXISTS Restaurants(
	Codice_pk INTEGER PRIMARY KEY,
	Nome VARCHAR(50) NOT NULL,
	Categoria  VARCHAR(20),
	Indirizzo VARCHAR(50),
	Sito VARCHAR(70),
	Telefono INTEGER,
	Longitudine FLOAT,
	Latitudine FLOAT
)"""

# Main
def main():
	#connection = create_server_connection("localhost", "root", "root")
	#create_database(connection, "CREATE DATABASE IF NOT EXISTS Restaurants")
	connection = create_db_connection("localhost", "root", "root", "Restaurants")
	execute_query(connection, drop_tables)
	execute_query(connection, create_restaurants)

if __name__ == "__main__":
	main()
