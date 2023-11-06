# API documentation

This part contains instructions on how to use the API.


# SQL database access

To access the SQL database you can use the execute function from *db.py* file

For example to create a new user: 
```python
from backend.db import execute

execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("username", "password"))
```