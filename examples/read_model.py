import sqlite3

try:
    conn = sqlite3.connect("../model/key_word_model.db")
except Error as e:
    print(e)
 
cur = conn.cursor()
cur.execute("SELECT * FROM sentiment_negative_word")
# cur.execute("SELECT word, value FROM sentiment_negative_word WHERE word == '咖啡'")
# cur.execute("SELECT * FROM sentiment_baseline")
 
rows = cur.fetchall()
 
print(rows)    