import mysql.connector
mydb = mysql.connector.connect(user='SWE', password='123456789',
                              host='127.0.0.1',
                          database='world')

cursor = mydb.cursor()

mycursor = mydb.cursor()
mycursor.execute(f"SELECT * FROM city ")

myresult = mycursor.fetchall()
print(myresult)
# email=str(input("Enter Email: "))
# if myresult == None:
#      print("wrong email")




