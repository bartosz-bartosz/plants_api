# plants_api

## Project overview

REST API project built using the FastAPI and SQLAlchemy frameworks with a Postgres database. 

The aim of this project is to provide an efficient and easy-to-use solution for managing home plants - keeping track of watering times, gathering statistics, and generally not making them die.

## Project structure

The main application logic is contained in the `app` directory, with the main entry point being `main.py`. Each resource is defined in a separate module in the `app.routers` directory. Each module consists of:

+ `router.py` - Resource endpoints
+ `crud.py` - CRUD operations
+ `models.py` - SQLAlchemy ORM Model definitions
+ `schemas.py` - Pydantic models for request/response validation

