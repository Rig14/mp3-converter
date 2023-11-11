# API documentation

This part contains instructions on how to use the API.

Before you start using the API a ``.env`` file **must be made**. Variables for the .env file can be found in the .env.example file.

## API endpoints

### Sign up
`/api/signup`
- **Method:** POST
- **Description:** Creates a new user
- **Request Body:**
    - email: user's email
    - password: user's password
    - password_confirm: user's password confirmation
- **Returns:** Error message when values are invalid. Otherwise returns JWT.


### Login
`/api/login`
- **Method:** POST
- **Description:** Logs in a user
- **Request Body:**
    - email: user's email
    - password: user's password
- **Returns:** Error message when values are invalid. Otherwise returns JWT.

### User data
`/api/user_data`
- **Method:** GET
- **Description:** Returns small amount of user data
- **Request Body:** None
- **Returns:** Error message when values are invalid. Otherwise returns user data.


# SQL database access

To access the SQL database you can use the execute function from *db.py* file

For example to create a new user: 
```python
from backend.db import execute

execute("INSERT INTO users (email, password) VALUES (%s, %s)", ("legit@email.com", "password"))
```