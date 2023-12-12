# API routes

All api routes that are available in the backend are listed here.
Also all usage examples are listed here.

## Sign up user
creates a new user in the database and returns a JWT token that is used for authentication

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
signs in a user and returns a JWT token that is used for authentication

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
returns the user data of the user that is currently logged in

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


## Download to server
downloads a file from a url to the server using yt-dlp. Returns the file identifier to later access the file

#### route: `/api/download`

#### method: `POST`

#### request body:
```json
{
    "url": "url to the video",
    "format": "format of the video",
}
```
#### response body:
```json
{
    "identifier": "file identifier",

    or 

    "error": "Some error message"
}
```

## Send file to client
sends the file to the client when the identifier is provided

#### route: `/api/file?identifier=<identifier>&file_name=<file_name>&get_name_only=<get_name_only>`

NB! if get_name_only is true then the file will not be sent to the client, only the file data will be returned

#### method: `GET`

#### response body:
```json
{
    "file": "file",

    or
        {
            "file_name": "file_name",
            "file_extention": "file_extention",
            "file_size": "file_size",
        }
    
    or

    "error": "Some error message"
}
```


## Change user data
changes the user data of the user that is currently logged in

#### route: `/api/change_user_data`

#### method: `POST`

#### **Token must be provided in the header of the request!!**

#### request body:
```json
{
    "name": "name of user",
    "motd": "the message that is displayed next to the user profile",
    "password": "password",
    "email": "email of user",
}
```

## Change profile picture
changes the profile picture of the user that is currently logged in

#### route: `/api/change_profile_picture`

#### method: `POST`

#### **Token must be provided in the header of the request!!**



## Add history entry
adds a history entry to the user that is currently logged in

#### route: `/api/add_history`

#### method: `POST`

#### **Token must be provided in the header of the request!!**

#### request body:
```json
{
    "content_title": "title of the content",
    "content_url": "url to the content",
    "content_format": "format of the content",
}
```


## Get history
returns the history of the user that is currently logged in

#### route: `/api/get_history`

#### method: `GET`

#### **Token must be provided in the header of the request!!**

#### response body:
```json
{
    "history": [
        {
            "content_title": "title of the content",
            "content_url": "url to the content",
            "content_format": "format of the content",
        },
        {
            "content_title": "title of the content",
            "content_url": "url to the content",
            "content_format": "format of the content",
        },
        {
            "content_title": "title of the content",
            "content_url": "url to the content",
            "content_format": "format of the content",
        },
    ]
}
```

## Blacklist
Everything that is in the blacklist will not be downloaded.

#### route: `/api/blacklist`

#### Token must be provided in the header of the request!!


#### method: `GET`
Will return the blacklist
#### response:
```json
{
    "items": [
        ["id", "url", "date added"],
        ["id", "url", "date added"],
        ["id", "url", "date added"],
    ]
}
```


#### method: `POST`
Will add the url to the blacklist
#### request body:
```json
{
    "content_url": "url to add to blacklist"
}
```

#### method: `PATCH`
Will remove the url from the blacklist
#### request body:
```json
{
    "content_id": "id if item to remove from blacklist"
}
```