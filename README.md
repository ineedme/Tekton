# Tekton

## Requirements
 
- [X] Create a rest API using Python (use 3.9 or 3.10 version). The use of Flask is prohibited; you can use other microframeworks or pure Python for this.
- [X] Document the API collection using Swagger
- [X] Patterns use (ie. repository pattern, cqrs,etc) make clear what you are
choosing and why.
- [X] Apply SOLID and Clean Code principles.
- [X] The solution should be implemented by using TDD (Test Driven
Development) Tests are mandatory.
- [X] Each request should use good validation patterns and HTTP Status Code
per response.
- [X] You should need to structure the project using N-layers.
- [X] A README.md file should be included with the contain description
(patterns, architecture, setup and startup steps, etc) consider include any
information that could help
- [X] Import the project code to a public repository on Github

## Challenge
Consider the use of a web system that manages different product inventory. You
are asked to create a API service that support the next features:
1. Insert(POST), Update(PUT) and GetbyId(GET) for the products.
Maintain a log file (plaintext) of the elapsed time used per request
2. Maintain a cache (with a minimum of 5 min) for a dictionary that contains the
product status, here a table with the values of this dictionary:
You can use a standard Cache, Lazy Cache or any kind of cache that you
considered fits well.
Status(key) StatusName(value)
   - 1: Active
   - 0: Inactive
3. Record the product information locally using any kind of local storage for the
data persistence. The mandatory fields/attributes to use are:
   - ProductId
   - Name
   - Status // 0 or 1
   - Stock,
   - Description
   - Price

  You are free to add additional fields for the products

4. The GetById method should return a product response with the next fields:

## Brief
Based on the problem description, I must develop a runnable server quickly.
I picked Python 3.10, Django 4.1, and Django REST Framework because they come with a lot of functionality right out of the box.
Django is base on MVT (Model-View-Template) architecture.
Django has an ORM to work with many databases, so I'm using SQLite to share easily.
Created a resource Product and used the HTTP Verbs implementing CRUD functions.
For discount, I created a small Mockaroo API with a single endpoint.
Used Django Cache to keep product status and discount for 5 minutes, status was a requirement of the challenge and I added the discount field to avoid no necessary calls to external APIs.
Log all the API history in the api.log


## Setup
see Install details [here](Install.md)

## Documentation
see Swagger Documentation [http://localhost:8000/api/v1/swagger/](http://localhost:8000/api/v1/product/)