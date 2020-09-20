import sqlite3

con = sqlite3.connect('users.db')

def sql_fetch(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT name FROM sqlite_master WHERE type="table"')

    data = cursorObj.fetchall()
    for i in data:
        print(i[0])
        l = ("DROP table IF EXISTS {}").format(i[0])
        cursorObj.execute(l)
        con.commit()

sql_fetch(con)