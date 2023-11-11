# API documentation

This part contains instructions on how to use the API.

## API endpoints

### Sign up
`/api/signup?username=<username>&password=<password>&password_confirm=<password>`
- **Method:** POST
- **Description:** Creates a new user
- **Returns:** Error message when values are invalid. Otherwise returns JWT.

### Login
`/api/login?username=<username>&password=<password>`
- **Method:** POST
- **Description:** Logs in a user
- **Returns:** Error message when values are invalid. Otherwise returns JWT.


# SQL database access

To access the SQL database you can use the execute function from *db.py* file

For example to create a new user: 
```python
from backend.db import execute

execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("username", "password"))
```