# Library-Management-System

## Introduction
This is a Library Management System (LMS) that mocks a real-life library and has features such as borrowing a book, adding book to library, removing book from library etc. 

## Key Concepts Learnt 
* Assigning distinct roles to users i.e admin and non-admin users
* Mocking tests
* Integrating CKEditor to application
* Creating a RESTful API

## API Documentation
### Use cases
The LMS API is a RESTful API that returns data in JSON format. The API supports HTTP and HTTPS and can be used by users to retrieve book(s) available in the library and by the admin to retireve, add , update or delete book(s) from the library.
A summary of the available actions for the API is as follows:

| Action | HTTP Method | Endpoint | Required parameters | Token authentication required | Restricted to admin user only |
| --- | --- | --- | --- | --- | --- |
| Get details of all books in the library | GET | /books | None | No | No |
| Get number of books in the library | GET | /books/count | None | No | No |
| Get all books by a particular author | GET | /books/author | None | No | No |
| Get list of book(s) borrowed by current user | GET | /books/mine | None | Yes | No |
| Get book with particular title | GET | /books/{title} | {title} | No | No |
| Update a book's details | PUT | /books/update/{title} | {title} | Yes | Yes |
| Delete a particular book | DELETE | /books/delete/{title} | {title} | Yes | Yes |
| Get details of all library users | GET | /users | None | Yes | Yes |
| Get number of all library users | GET | /users/count | None | Yes | Yes |
| Get details of paticular user | GET | /user/{id} | {id} | Yes | Yes |
| Create a user account | POST | /users | None | No | No |
| Update user's details | PUT | /user/update | None | Yes | No |
| Delete user account| DELETE | /user/{id} | {id} | Yes | Yes |

### Getting a token
Some endpoints, as noted in the table above, require that users are authenticated and have a token. A user (has to be a registered user) can obtain a token as follows:

```
import requests

url = "https://bruno-lms.herokuapp.com/"

username = "<your username>"
password = "<your password>"

token = requests.get(f"{url}api/token", auth=(username, password))
print(token.json())
```

### API in action
#### Endpoints that don't require token authentication
Some API endpoints don't require token authentication. An example of such an endpoint is the '/books/count' endpoint which returns the total number of books in the library and can be accessed as follows: 

```
import requests

url = "https://bruno-lms.herokuapp.com/"

response = requests.get(f"{url}api/books/count")
print(response.json())
```

### Endpoints that require token authentication
Users have to possess a valid token so as to access certain endpoints. In order for such endpoints to return the desired output, users have to pass in their token to the headers.

```
import requests

url = "https://bruno-lms.herokuapp.com/"
token = {
    'x-access-token': '<yourRAndoMLYgenerateddTokenGoeshere>'
}

response = requests.get(f"{url}api/books/mine", headers=token)
print(response.json())
```

Note that some endpoints are only restricted to admin users and will throw an error if a non-admin user tries to access it.

### Endpoints that require data in their request bodies
Some endpoints require data to be passed in their bodies so as to execute user demands.

```
import requests

url = "https://bruno-lms.herokuapp.com/"
details ={
    "name": "username",
    "email": "user@email.com",
    "password": "!uSer@pa55w0rd"
}

response = requests.post(f"{url}api/user", json=details)
print(response.json())
```

Live version of the app can be found at https://bruno-lms.herokuapp.com/