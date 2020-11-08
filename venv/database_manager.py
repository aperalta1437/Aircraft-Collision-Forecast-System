import sqlite3

connection = sqlite3.connect('AIRCRAFT_COLLISION_FORECAST_SYSTEM.db')
cursor = connection.cursor()

def create_table(table_name, **kwargs):
    query = 'CREATE TABLE IF NOT EXISTS ' + table_name + '('

    for field in kwargs:

        query += f'{field} {kwargs[field]}, '

    query = query[:-2] + ');'

    print(query)

    cursor.execute(query)

def add_row(table_name, **kwargs):
    query = f'INSERT INTO {table_name}('

    for field in kwargs:
        query += f'{field}, '

    query = f'{query[:-2]}) VALUES('

    for field in kwargs:
        query += f'{kwargs[field]}, '

    query = f'{query[:-2]});'

    print(query)

    cursor.execute(query)
    connection.commit()


def show_table(table_name):
    query = f'SELECT * FROM {table_name};'

    cursor.execute(query)
    results = cursor.fetchall()

    print(results)

#create_table('USER_CREDENTIALS', USERNAME='CHAR(25) PRIMARY KEY NOT NULL', PASSWORD='CHAR(50)')


username = 'TEST_USER'
password = 'Password1'

add_row('USER_CREDENTIALS', USERNAME=F"'{username}'", PASSWORD=f"'{password}'")

show_table('USER_CREDENTIALS')



cursor.close()
connection.close()


