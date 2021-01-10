#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error

CREATE_MEASURE_TABLE = """
CREATE TABLE measure (
    time DOUBLE NOT NULL PRIMARY KEY,
    pressure DOUBLE NOT NULL,
    temperature DOUBLE NOT NULL
);
"""

INSERT_COMMAND = """
INSERT INTO measure(time, pressure, temperature)
VALUES ({}, {}, {});
"""

def createConnection(hostName, userName, dbName, password):
    connection = None
    try:
        connection = mysql.connector.connect(
                host=hostName,
                user=userName,
                database=dbName,
                passwd=password
        )
    except Error as err:
        raise err

    return connection

def executeUpdate(connection, update):
    cursor = connection.cursor()
    try:
        cursor.execute(update)
        connection.commit()
    except Error as err:
        raise err

def executeQuery(connection, q):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(q)
        result = cursor.fetchall()
        return result
    except Error as e:
        raise e
