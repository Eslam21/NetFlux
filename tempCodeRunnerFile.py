# for quick testing 

import mysql.connector

connection = mysql.connector.connect(
    user="SWE", password="123456789000", host="localhost", database="netflux"
)

cursor = connection.cursor()