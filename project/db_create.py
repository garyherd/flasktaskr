import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()
    c.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, due_date TEXT NOT NULL, priority NOT NULL,
    status INTEGER NOT NULL)""")

    # insert dummy data
    c.execute(
        'INSERT INTO tasks (name, due_date, priority, status)'
        'VALUES("Finish this tutorial", "04/12/2015", 10, 1)'
    )

    c.execute(
        'INSERT INTO tasks (name, due_date, priority, status)'
        'VALUES("Finish Real Python Course 2", "05/25/2015", 10, 1)'
    )