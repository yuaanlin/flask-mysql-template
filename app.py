import os
from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

def get_mysql_connection():
    """
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: The MySQL database connection object.
    """
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
    )

def get_mysql_databases():
    """
    Retrieves a list of MySQL databases.

    Returns:
        list: A list of databases available in the MySQL server.

    Raises:
        Error: If there is an error connecting to the MySQL server.
    """
    try:
        connection = get_mysql_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            cursor.close()
            connection.close()
            return databases
    except Error as e:
        return f"Error: {str(e)}"

def get_mysql_tables(database):
    """
    Retrieves a list of tables from a MySQL database.

    Args:
        database (str): The name of the database.

    Returns:
        list: A list of tables in the specified database.

    Raises:
        Error: If there is an error connecting to the MySQL database.
    """
    try:
        connection = get_mysql_connection()
        connection.database = database
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            cursor.close()
            connection.close()
            return tables
    except Error as e:
        return f"Error: {str(e)}"

@app.route('/')
def list_databases():
    dbs = get_mysql_databases()
    if isinstance(dbs, str):  # Error message
        return dbs
    else:
        # Generate clickable links for each database
        links = ['<a href="/{0}">{0}</a>'.format(db[0]) for db in dbs]
        return '<br>'.join(links)

@app.route('/<database>')
def list_tables(database):
    tables = get_mysql_tables(database)
    if isinstance(tables, str):  # Error message
        return tables
    else:
        # Display tables in the selected database
        return '<br>'.join([table[0] for table in tables])

if __name__ == '__main__':
    app.run(debug=True)
