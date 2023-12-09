# API routes

All api routes that are available in the backend are listed here.
Also all usage examples are listed here.

## Sign up user

#### route: `/api/signup`
#### method: `POST`
#### request body:
```json
{
    "email": "email",
    // password must be at least 8 characters long and password_confirm must match password
    "password": "password",
    "password_confirm": "password"
}
```
#### response body:

if user creation was successful returns the JWT token:
```json
{
    "token": "akcijpoa19r8oij09u120ij0921"
}
```
if user creation failed returns an error message:
```json
{
    "error": "Some error message"
}
```

## Sign in user

#### route: `/api/login`
#### method: `POST`
#### request body:
```json
{
    "email": "email",
    "password": "password"
}
```
#### response body:
```json
{
    "token": "akcijpoa19r8oij09u120ij0921"

    or 

    "error": "Some error message"
}
```

## Get user data

#### route: `/api/user_data`

#### method: `GET`

#### **Token must be provided in the header of the request!!**

#### response body:
```json
{
    "id": "user unique id",
    "name": "name of user",
    "motd": "the message that is displayed next to the user profile",
    "profile_picture": "url to the profile picture",
    "email": "email of user",
}
```

