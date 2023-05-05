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


#Q: Buddy c, why I am i getting a unicode escape codec error?
#A: you need to use a raw string
#Q: what's a raw string?
#A: a raw string is a string prefixed with an r
#Q: so what's the syntax for that?
#Q:Why isn't it executing it to the sql dataabase?
#A: you need to commit the changes
#Q: how do I do that?
#A: you need to call the commit() method on the cursor object
#Q: So would it just be cursor.commit()?
#Q: Should I put that in the main function?

#Q: Do I have to enable a setting in SQLlite to allow the code to run into the database?
#A: No, you don't need to enable any settings
#Q: So why isn't it working?
#Q: Buddy, I have the commit in there, but it's still not working
#A: you need to call the commit() method on the connection object
#Q: So would it be connection.commit()?
#Q: So it would be cursor.connection.commit()?
#Q: so what am I doing wrong buddy c?
#A: you need to call the commit() method on the connection object
#Q: I have that that on line 28
#Q: sp on the createConnection function? Or on the con variable?
#Q: so I get an error now?
#Q: So how would that look like?
#A: you need to call the commit() method on the connection object
#Q: So would it be connection.commit()?
#A: so would it be CON.connection.commit()?
#Q: So is this the correct part: CON = lite.connect('test.db').commit()
#Q: buddy, you're speaking riddles here?
#Q:is the path to the databaase file correct?
#A: yes, it is
#Q: so what am I doing wrong?
#Q: so what am I doing wrong?
#A
#Q: 





  