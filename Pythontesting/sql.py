import sqlite3 as lite
import os
PATH = r'C:\Users\Owner\Desktop\SQL_Databases\f.db'




connection = lite.connect('f.db')
print(connection.execute("PRAGMA database_list").fetchall())
db_file = os.path.join(os.getcwd(), "f.db")
print(db_file)
try:
    query = '''
    CREATE TABLE IF NOT EXISTS movies2 (
    title TEXT
    year INTEGER
    rating REAL
    )'''
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

except lite.Error as e:
    print(f"The error occurred: '{e}")
finally:
    connection.commit()
    connection.close()





  
