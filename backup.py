import sqlite3
import csv
import os

# Path to your chat.db - adjust as needed
db_path = '~/Library/Messages/chat.db'
# Ensure the path is correctly expanded
db_path = os.path.expanduser(db_path)

# Directory to store the exported files
output_dir = 'messages_exports'
os.makedirs(output_dir, exist_ok=True)

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to get all contacts
    contacts_query = "SELECT DISTINCT handle.id FROM handle;"
    cursor.execute(contacts_query)
    contacts = cursor.fetchall()
    
    for contact in contacts:
        contact_id = contact[0]
        if contact_id:  # Ensure contact ID is not null
            # File to save messages for the current contact
            output_file = os.path.join(output_dir, f'{contact_id}.csv')

            # Query to select messages for the current contact, including sender information
            messages_query = f"""
            SELECT
                message.rowid,
                datetime(message.date/1000000000 + strftime('%s', '2001-01-01'), 'unixepoch', 'localtime') as date,
                message.text,
                case message.is_from_me when 1 then 'Me' else 'Them' end as sender
            FROM message
            LEFT JOIN handle on message.handle_id = handle.rowid
            WHERE handle.id = '{contact_id}'
            ORDER BY message.date;
            """
            
            cursor.execute(messages_query)
            messages = cursor.fetchall()
            
            # Write messages to a file for the current contact
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Row ID', 'Date', 'Text', 'Sent By'])  # Writing headers
                writer.writerows(messages)
            
            print(f"Messages for contact {contact_id} have been exported to {output_file}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if conn:
        conn.close()
