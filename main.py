import json
import os
import sqlite3

db_path = os.path.expanduser('~/Library/Messages/chat.db')

conn = sqlite3.connect(db_path)
c = conn.cursor()

query = "SELECT text, is_from_me, datetime(message.date/1000000000 + strftime('%s', '2001-01-01'),'unixepoch','localtime') as date FROM message WHERE handle_id = 1 AND text IS NOT NULL AND cache_has_attachments = 0 ORDER BY date;"

c.execute(query)

messages = []

for row in c.fetchall():
    # print(f"{row[0]}\t{row[1]}\t{row[2]}")
    message = {
        'text': row[0],
        'is_from_me': bool(row[1]),
        'date': row[2]
    }
    messages.append(message)

with open("nikki.json", "w") as f:
    json.dump(messages, f)

conn.close()
