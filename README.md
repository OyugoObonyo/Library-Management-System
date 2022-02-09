# Library-Management-System

# Introduction

# Key Concepts 

# API Documentation
## Use cases
The LMS API is a RESTful API that returns data in JSON format. The API supports HTTP and HTTPS and can be used by users to retrieve book(s) available in the library and by the admin to retireve, add , update or delete book(s) from the library.
A summary of the available actions for the API is as follows:

| Action | HTTP Method | Endpoint | Required parameters | Token authentication required | admin user only |
| --- | --- |
| Get all books in the library | GET | /books | None | No | No |
| Get number of books in the library | GET | /books/count | None | No | No |
| Get all books by a particular author | GET | /books/{author} | {author} | No | No |
| Get list of books borrowed by current user | GET | /books/mine | None | Yes | No |

Live version of the app can be found at https://bruno-lms.herokuapp.com/