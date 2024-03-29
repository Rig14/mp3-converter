"""Everything that has to do with the database."""

import os
import sqlite3
import sys
import bcrypt

from dotenv import load_dotenv

# Database location is in the home directory.
DATABASE_FILE_DIR = os.path.dirname(__file__)
DATABASE_FILE_PATH = os.path.join(DATABASE_FILE_DIR, "database.db")
MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")


def create():
    """
    Sets up the database by running all the migrations one by one
    in correct order.
    """
    # Get all the migration file names in the migrations directory.
    migration_files = [x for x in os.listdir(MIGRATIONS_DIR) if x.endswith(".sql")]

    # Sort the migration files by their number.
    migration_files.sort(key=lambda x: int(x.split(".")[0]))

    # Create a connection to the database.
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        # Create a cursor to execute SQL commands.
        cursor = conn.cursor()

        # Run all the migrations one by one.
        for migration_file in migration_files:
            # Get the migration file path.
            migration_file_path = os.path.join(MIGRATIONS_DIR, migration_file)

            # Read the migration file.
            with open(migration_file_path, "r", encoding="UTF-8") as f:
                migration = f.read()
                # Execute the migration.
                cursor.executescript(migration)

        # Commit the changes.
        conn.commit()


def delete():
    """
    Deletes the database file.
    """
    if os.path.exists(DATABASE_FILE_PATH):
        os.remove(DATABASE_FILE_PATH)


def reset():
    """
    Deletes the database file and creates a new one.
    """
    delete()
    create()


def update():
    """
    Only runs the latest migration.
    """
    # Get all the migration file names in the migrations directory.
    migration_files = [x for x in os.listdir(MIGRATIONS_DIR) if x.endswith(".sql")]

    # Sort the migration files by their number.
    migration_files.sort(key=lambda x: int(x.split(".")[0]))

    # Get the latest migration file.
    latest_migration_file = migration_files[-1]

    # Create a connection to the database.
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        # Create a cursor to execute SQL commands.
        cursor = conn.cursor()

        # Get the latest migration file path.
        latest_migration_file_path = os.path.join(MIGRATIONS_DIR, latest_migration_file)

        # Read the latest migration file.
        with open(latest_migration_file_path, "r", encoding="UTF-8") as f:
            migration = f.read()
            # Execute the migration.
            cursor.executescript(migration)

        # Commit the changes.
        conn.commit()


def execute(query, params=None):
    """
    Execute a sql query on the database.
    returns a list of the query results if there are any. else returns a empty list.
    """
    # change dir to backend/db
    os.chdir(DATABASE_FILE_DIR)

    # Create a connection to the database.
    with sqlite3.connect(DATABASE_FILE_PATH) as conn:
        # Create a cursor to execute SQL commands.
        cursor = conn.cursor()

        # Execute the query.
        cursor.execute(query, params)

        # Get the results.
        results = cursor.fetchall()

        # Return the results.
        return results


def add_admin():
    """Adds admin user to the database."""
    # aquire the admin password from the environment variables
    load_dotenv()
    password = os.getenv("ADMIN_PASSWORD")
    if not password:
        password = "admin"
    # hash the password
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    execute(
        "INSERT INTO users (name, email, password, admin) VALUES (?, ?, ?, ?)",
        ("admin", "admin", hashed_pw, True),
    )


if __name__ == "__main__":
    # run the function with the name passed as the first argument
    globals()[sys.argv[1]]()
