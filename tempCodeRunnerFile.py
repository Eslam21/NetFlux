# for quick testing 

import mysql.connector
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time



connection = mysql.connector.connect(
    user="SWE", password="123456789000", host="localhost", database="netflux"
)

cursor = connection.cursor()


cursor.execute("SELECT title FROM movies")

# result=list(map(lambda movies: movies[0],cursor.fetchall()))
# print(result)

# similar=process.extract("space",choices=result,limit=None)
# similar.sort(reverse = True, key = lambda t: t[1])
# movies=[movie[0] for movie in similar]
# print(len(movies))


# --