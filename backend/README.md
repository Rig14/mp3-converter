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