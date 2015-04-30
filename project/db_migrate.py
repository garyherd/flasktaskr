from views import db
from _config import DATABASE_PATH

import sqlite3
# from datetime import datetime

# with sqlite3.connect(DATABASE_PATH) as connection:
#     c = connection.cursor()
#     c.execute("ALTER TABLE tasks RENAME TO old_tasks")
#
#     db.create_all()
#
#     c.execute("""SELECT name, due_date, priority, status
#                 FROM old_tasks ORDER BY task_id ASC""")
#
#     data = [(row[0], row[1], row[2], row[3],
#              datetime.now(), 1) for row in c.fetchall()]
#
#     c.executemany("""INSERT INTO tasks (name, due_date, priority, status,
#                     posted_date, user_id) VALUES (?, ?, ?, ?, ?, ?)""", data)
#
#     c.execute("DROP TABLE old_tasks")

with sqlite3.connect(DATABASE_PATH) as connection:
    # get a cursor object to execute SQL commands
    c = connection.cursor()

    # temporarily change the name of  users table
    c.execute("""ALTER TABLE users RENAME TO old_users""")

    # recreate a new users table with updated schema
    db.create_all()

    # retrieve data from old_users_table
    c.execute("""SELECT name, email,
    password FROM old_users ORDER BY id ASC""")

    # save all rows as a list of tuples: set role to 'user'
    data = [(row[0], row[1], row[2], 'user') for row in c.fetchall()]

    # insert data to users table
    c.executemany("""INSERT INTO users (name, email, password,
                    role) VALUES (?, ?, ?, ?)""", data)

    # delete old_users_table
    c.execute("DROP TABLE old_users")
