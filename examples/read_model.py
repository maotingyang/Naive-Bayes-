import sqlite3

try:
    conn = sqlite3.connect("../model/model.db")
except Error as e:
    print(e)
 
cur = conn.cursor()
# cur.execute("SELECT * FROM sentiment_positive_word")
cur.execute("SELECT * FROM sentiment_negative_word")
# cur.execute("SELECT * FROM sentiment_baseline")
 
rows = cur.fetchall()
 
print(rows)    