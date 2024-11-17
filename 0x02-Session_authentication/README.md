# Sessions Authentication - Project 0x02

Task 0: Et moi et moi et moi!
Project Setup
Copy all your work from the 0x06. Basic authentication project into this new folder.
This version implements Basic Authentication to give access to all User endpoints:
GET /api/v1/users
POST /api/v1/users

GET /api/v1/users/<user_id>

PUT /api/v1/users/<user_id>

DELETE /api/v1/users/<user_id>


Additionally, a new endpoint is added:

GET /users/me — Retrieves the authenticated User object.


Make sure that all mandatory tasks from the previous 0x06 project are completed, as this project builds on that foundation.

Folder Structure

Copy the models and api folders from the previous project (0x06) into this project directory.

Update @app.before_request

In api/v1/app.py, update the following:

Assign the result of auth.current_user(request) to request.current_user.


Update Route for /api/v1/users/<user_id>

In api/v1/views/users.py, modify the GET route for /api/v1/users/<user_id>:

1. If <user_id> is "me" and request.current_user is None, abort with a 404.


2. If <user_id> is "me" and request.current_user is not None, return the authenticated User in a JSON response.


3. For other user IDs, maintain the previous behavior.




```

Example Commands

Terminal 1: Create a User

bob@dylan:~$ cat main_0.py
#!/usr/bin/env python3
""" Main 0 """
import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

""" Create a user test """
user_email = "bob@hbtn.io"
user_clear_pwd = "H0lbertonSchool98!"

user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user: {}".format(user.id))
user.save()

basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Base64: {}".format(base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")))
```
Terminal 2: Run Server
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Terminal 3: Test API Endpoints

```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}

bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Basic Ym9iQGhidG4uaW86SDBsYmVydG9uU2Nob29sOTgh"
[
  {
    "created_at": "2017-09-25 01:55:17", 
    "email": "bob@hbtn.io", 
    "first_name": null, 
    "id": "9375973a-68c7-46aa-b135-29f79e837495", 
    "last_name": null, 
 "updated_at": "2017-09-25 01:55:17"
  }
]

bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users/me" -H "Authorization: Basic Ym9iQGhidG4uaW86SDBsYmVydG9uU2Nob29sOTgh"
{
  "created_at": "2017-09-25 01:55:17", 
  "email": "bob@hbtn.io", 
  "first_name": null, 
  "id": "9375973a-68c7-46aa-b135-29f79e837495", 
  "last_name": null, 
  "updated_at": "2017-09-25 01:55:17"
}
```

Task 1: Empty Session

1. Create a SessionAuth class that inherits from Auth.

2. Ensure the class doesn't overload any methods for now.

3. Update api/v1/app.py to select the authentication method based on AUTH_TYPE.



Example:
```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```


Task 2: Create a Session

1. Update the SessionAuth class with a method create_session(self, user_id: str = None) -> str:
Generate a Session ID and store it with user_id in a dictionary.


```
bob@dylan:~$ cat main_1.py 
#!/usr/bin/env python3
""" Main 1 """
from api.v1.auth.session_auth import SessionAuth

sa = SessionAuth()

print("{}: {}".format(type(sa.user_id_by_session_id), sa.user_id_by_session_id))

user_id = None
session = sa.create_session(user_id)
print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

```

Task 3: User ID for Session ID

1. Update SessionAuth to add user_id_for_session_id(self, session_id: str = None) -> str.
2. This method will allow retrieval of user_id based on a given session_id.


Example:
```
bob@dylan:~$ cat main_2.py 
#!/usr/bin/env python3
""" Main 2 """
from api.v1.auth.session_auth import SessionAuth

sa = SessionAuth()

user_id_1 = "abcde"
session_1 = sa.create_session(user_id_1)
print("{} => {}: {}".format(user_id_1, session_1, sa.user_id_by_session_id))
```
