import sqlite3

connection = None
cursor = None

def create_table(table_name, **kwargs):
    query = 'CREATE TABLE IF NOT EXISTS ' + table_name + '('

    for field in kwargs:

        query += f'{field} {kwargs[field]}, '

    query = query[:-2] + ');'

    print(query)

    cursor.execute(query)


def select_data(table_name, db_file_name=None, is_open=False, *select_fields, **where_fields):
    if not is_open:
        db_connection = sqlite3.connect(db_file_name)
        db_cursor = db_connection.cursor()
    else:
        pass

    query = f'SELECT '

    select_added = False
    for field in select_fields:
        query += f'{field}, '
        select_added = True

    if select_added:
        query = f'{query[:-2]} FROM {table_name} WHERE '
    else:
        query += f'* FROM {table_name} WHERE '

    where_added = False
    for key_field in where_fields:
        query += f'{key_field} = {where_fields[key_field]}, '
        where_added = True

    if where_added:
        query = f'{query[:-2]};'
    else:
        query = f'{query[:-7]};'

    print(query)

    results = None

    if not is_open:
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        db_connection.close()
    else:
        cursor.execute(query)
        results = cursor.fetchall()

    return results


def delete_data(table_name, db_file_name=None, is_open=False, **where_fields):
    if not is_open:
        db_connection = sqlite3.connect(db_file_name)
        db_cursor = db_connection.cursor()
    else:
        pass

    query = f'DELETE FROM {table_name} WHERE '

    where_added = False
    for where_key in where_fields:
        query += f'{where_key} = {where_fields[where_key]} AND '
        where_added = True

    if where_added:
        query = f'{query[:-5]};'
    else:
        query = f'{query[:-7]};'

    #print(query)

    if not is_open:
        db_cursor.execute(query)

        db_connection.commit()
        db_connection.close()
    else:
        cursor.execute(query)


def update_data(table_name, db_file_name=None, is_open=False, **set_n_where_fields):
    if not is_open:
        db_connection = sqlite3.connect(db_file_name)
        db_cursor = db_connection.cursor()
    else:
        pass

    query = f'UPDATE {table_name} SET '

    set_added = False
    for set_key in set_n_where_fields['SET']:
        query += f'{set_key} = {set_n_where_fields["SET"][set_key]}, '
        set_added = True

    if set_added:
        query = f'{query[:-2]} WHERE '
    else:
        query = f'{query[:-5]} WHERE '

    where_added = False
    for where_key in set_n_where_fields['WHERE']:
        query += f'{where_key} = {set_n_where_fields["WHERE"][where_key]} AND '
        where_added = True

    if where_added:
        query = f'{query[:-5]};'
    else:
        query = f'{query[:-7]};'

    #print(query)

    if not is_open:
        db_cursor.execute(query)

        db_connection.commit()
        db_connection.close()
    else:
        cursor.execute(query)


def insert_row(table_name, db_file_name=None, is_open=False, **kwargs):
    if not is_open:
        db_connection = sqlite3.connect(db_file_name)
        db_cursor = db_connection.cursor()
    else:
        pass

    query = f'INSERT INTO {table_name} ('

    for field in kwargs:
        query += f'{field}, '

    query = f'{query[:-2]}) VALUES('

    for field in kwargs:
        query += f'{kwargs[field]}, '

    query = f'{query[:-2]});'

    print(query)

    if not is_open:
        db_cursor.execute(query)

        db_connection.commit()
        db_connection.close()
    else:
        cursor.execute(query)


def show_table(table_name):
    query = f'SELECT * FROM {table_name};'

    cursor.execute(query)
    results = cursor.fetchall()

    print(results)


def clean_table(db_file_name, table_name):
    db_connection = sqlite3.connect(db_file_name)
    db_cursor = db_connection.cursor()

    query = 'DELETE FROM ' + table_name
    db_cursor.execute(query)

    db_connection.commit()
    db_connection.close()


def open_db_connection(db_file_name):
    global connection, cursor
    connection = sqlite3.connect(db_file_name)
    cursor = connection.cursor()


def close_db_connection():
    connection.commit()
    connection.close()


def execute_query(query, db_file_name=None):
    if db_file_name is None:
        cursor.execute(query)
        return cursor.fetchall()
    else:
        db_connection = sqlite3.connect(db_file_name)
        db_cursor = db_connection.cursor()
        db_cursor.execute(query)
        return db_cursor.fetchall()








# create_table('AIRPLANES', ICAO24='VARCHAR(8) PRIMARY KEY NOT NULL', BARO_ALTITUDE='DECIMAL(12, 4)',
#              CALLSIGN='VARCHAR(12)', GEO_ALTITUDE='DECIMAL(12, 4)', HEADING='DECIMAL(7, 4)',
#              LAST_CONTACT='DECIMAL(12, 0)', LATITUDE='DECIMAL(8, 4)', LONGITUDE='DECIMAL(8, 4)',
#              ON_GROUND='')

# create_table('AIRPLANES', ICAO24='TEXT PRIMARY KEY NOT NULL', BARO_ALTITUDE='REAL',
#              CALLSIGN='TEXT', GEO_ALTITUDE='REAL', HEADING='REAL',
#              LAST_CONTACT='REAL', LATITUDE='REAL', LONGITUDE='REAL',
#              ON_GROUND='INTEGER', ORIGIN_COUNTRY='TEXT', POSITION_SOURCE='INTEGER', SENSORS='TEXT',
#              SPI='INTEGER', SQUAWK='INTEGER', TIME_POSITION='REAL', VELOCITY='REAL', VERTICAL_RATE='REAL')


# username = 'TEST_USER'
# password = 'Password1'
#
# add_row('USER_CREDENTIALS', USERNAME=F"'{username}'", PASSWORD=f"'{password}'")
#
# open_db_connection(r'AIRCRAFT_COLLISION_FORECAST_SYSTEM.db')
#
# show_table('AIRPLANES')
#
# close_db_connection()


