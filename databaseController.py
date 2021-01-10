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

def createConnectionSSL(hostName, dbName, username, password, ssl_ca, ssl_cert, ssl_key):
    con = None
    try:
        con = mysql.connector.connect(
                host=hostName,
                database=dbName,
                user=username,
                passwd=password,
                ssl_ca = ssl_ca,
                ssl_cert=ssl_cert,
                ssl_key=ssl_key
                )
    except Error as err:
        raise err

    return con

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

def getDbSecrets(fileName="secrets/db.secret"):
    try:
        secrets = {}
        f = open(fileName)
        text = f.read()
        f.close()

        text = text.split("\n")
        text.pop()

        for line in text:
            (key, value) = line.split(": ")
            secrets[key] = value
        return secrets

    except Exception as e:
        raise e
