import mysql.connector
mydb = mysql.connector.connect(user='root', password='147258369',
                              host='127.0.0.1',
                              database='netflux')
cursor = mydb.cursor()



mycursor = mydb.cursor()
mycursor.execute(f"SELECT * FROM user ")

myresult = mycursor.fetchmany(2)
print(myresult)
# email=str(input("Enter Email: "))
# if myresult == None:
#      print("wrong email")




