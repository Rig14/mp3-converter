"""Everything that has to do with the database."""

import os
from pathlib import Path
import shutil
import sqlite3
import sys

# Database location is in the home directory.
DATABASE_FILE_DIR = os.path.join(str(Path.home()), ".database")
DATABASE_FILE_PATH = os.path.join(DATABASE_FILE_DIR, "database.db")
MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")


def update():
    """
    Apply all migrations in the migrations folder.

    Creates the database if it is not already created.

    Should be run every time code is pushed to production.
    """
    # Create the database directory if it doesn't exist.
    if not os.path.exists(DATABASE_FILE_DIR):
        os.makedirs(DATABASE_FILE_DIR)

    # get migrations files list
    migrations = [x for x in os.listdir(MIGRATIONS_DIR) if x.endswith(".sql")]

    # sort the list by the migration number
    migrations.sort(key=lambda x: int(x.split(".")[0]))

    # add the migrations dir path to the migrations file names
    migrations = [os.path.join(MIGRATIONS_DIR, x) for x in migrations]

    # connect to the database (will also create the database if it does not exist)
    with sqlite3.connect(DATABASE_FILE_PATH) as connection:
        # cursor enables traversal over the records in the database
        cursor = connection.cursor()

        # execute all migrations
        for migration in migrations:
            with open(migration, "r", encoding="UTF-8") as migration_file:
                cursor.executescript(migration_file.read())

        connection.commit()


def execute(query: str, parametes: tuple = ()):
    """
    Execute a query on the database. Returns the result of the query.
    If the query does not return anything (e.g. INSERT), returns [].
    """
    os.chdir(DATABASE_FILE_DIR)
    with sqlite3.connect(DATABASE_FILE_PATH) as connection:
        cursor = connection.cursor()
        res = cursor.execute(query, parametes).fetchall()
        connection.commit()
        return res


def erase_database():
    """
    Delete sql database file.
    """
    if os.path.exists(DATABASE_FILE_DIR):
        shutil.rmtree(DATABASE_FILE_DIR)


if __name__ == "__main__":
    # allow running functions of this file from the command line
    globals()[sys.argv[1]]()
