import sqlite3

email_to_delete = input("Enter the email of the user to delete: ")
conn = sqlite3.connect('members.db')
c = conn.cursor()

c.execute('DELETE FROM users WHERE email = ?', (email_to_delete,))
conn.commit()
conn.close()
print(f"User with email {email_to_delete} has been deleted.")