# Backend layout
The backend is written in python and uses the flask framework.

The backend is split into many parts separated into different folders.

## `db`
All code that is related to the database is in this folder.

For example the `db.py` file contains the `execute` function that is used to execute SQL queries.

To alter the structure of the database you can write into the migrations folder.

## `downloader`
All code that is related to downloading files is in this folder and mainly in the main.py file.


## `user`
All code that is related to user management is in this folder.

That means JWT token generation and verification, user creation and login. User data (history, name, email, etc.) managment is also stored here.

## static folder
The static folder contains all static files that are served by the backend. For this project it is only used for user profile pictures.

# SQL database access

To access the SQL database you can use the execute function from `db`

For example to create a new user: 
```python
from backend.db import execute

# returns the id of the user that has the email address
email = execute("SELECT id FROM users WHERE email = ?", (email,))

print(email[0][0])
```

# API routes
All api routes are described in the [API_ROUTES.md](API_ROUTES.md) file.
