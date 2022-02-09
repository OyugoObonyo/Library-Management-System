# Library-Management-System

## Introduction

## Key Concepts 

## API Documentation
### Use cases
The LMS API is a RESTful API that returns data in JSON format. The API supports HTTP and HTTPS and can be used by users to retrieve book(s) available in the library and by the admin to retireve, add , update or delete book(s) from the library.
A summary of the available actions for the API is as follows:

| Action | HTTP Method | Endpoint | Required parameters | Token authentication required | Restricted to admin user only |
| --- | --- | --- | --- | --- | --- |
| Get details of all books in the library | GET | /books | None | No | No |
| Get number of books in the library | GET | /books/count | None | No | No |
| Get all books by a particular author | GET | /books/{author} | {author} | No | No |
| Get list of book(s) borrowed by current user | GET | /books/mine | None | Yes | No |
| Get book with particular title | GET | /books/{title} | {title} | No | No |
| Update a book's details | PUT | /books/update/{title} | {title} | Yes | Yes |
| Delete a particular book | DELETE | /books/delete/{title} | {title} | Yes | Yes |
| Get details of all library users | GET | /users | None | Yes | Yes |
| Get number of all library users | GET | /users/count | None | Yes | Yes |
| Get details of paticular user | GET | /user/{id} | {id} | Yes | Yes |
| Add a user | POST | /users | {name}, {email}, {password} | No | No |
| Update user's details | PUT | /user/update | None | Yes | No |
| Delete user account| DELETE | /user/{id} | {id} | Yes | Yes |



Live version of the app can be found at https://bruno-lms.herokuapp.com/