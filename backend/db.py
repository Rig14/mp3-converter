import os
import sqlite3


def init_empty_db():
    """
    Initialize empty database
    """
    # if database already exsists - delete it
    if os.path.exists(os.path.join(os.path.dirname(__file__), "database.db")):
        os.remove(os.path.join(os.path.dirname(__file__), "database.db"))

    os.chdir(os.path.dirname(__file__))
    con = sqlite3.connect(os.path.join(os.path.dirname(__file__), "database.db"))
    cur = con.cursor()

    migrations_count = len(os.listdir("migrations"))

    for i in range(migrations_count):
        with open("migrations/{}.sql".format(i)) as f:
            cur.executescript(f.read())

    con.commit()
    con.close()


if __name__ == "__main__":
    init_empty_db()
