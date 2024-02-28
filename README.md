# FastApi-Minimal-Boilerplate #

This repository contains a template project using FastApi framework for Python

### How do I get set up? ###

1. First, set up a Python virtual environment and activate it.
2. Then run the following command to setup the dependencies:
`
pip install -r requirements.txt
`
3. Run `main.py` to start the server (`python -m app.main`)
4. Run `python -m unittest` to run tests

### Rest Endpoints and routers ###
The REST endpoints available for this project are:

1. http://localhost:8080/calculator

For more info about request methods and sub-routes, check the Swagger URL below.

The `router` package has all the FastApi routers for this project. Please refer to them when creating new endpoints.

### Adding Routers
To add a router, create a router in the `router` package. Then add the router in the list in `__init__.py` of `router` package. `main.py` automatically adds the routers to FastApi `app` from this list.

### Exception Handling ###
The `exception` package has all needed classes for Exception Handling. The `ApplicationException` class is a custom `Exception` that is thrown in the application. The class `ExceptionResponseFactory` creates a response for the error that occurs. 

If an exception is thrown in multiple places in the application, please add a handler for the exception in `ExceptionHandler` class. 

### API Documentation with Swagger ###
FastApi has swagger built in.

Link to Swagger UI: http://localhost:8080/docs
