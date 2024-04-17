# plants_api

## Project overview

REST API project built using the FastAPI and SQLAlchemy frameworks with a Postgres database. 

The aim of this project is to provide an efficient and easy-to-use solution for managing home plants - keeping track of watering times, gathering statistics, and generally not making them die.

## Project structure

The main application logic is contained in the `app` directory, with the main entry point being `main.py`. Each resource is managed by a separate module defined in the `app.resources` directory. Each module consists of:

+ `router.py` - Resource endpoints
+ `crud.py` - CRUD operations
+ `models.py` - SQLAlchemy ORM Model definitions
+ `schemas.py` - Pydantic models for request/response validation

## Solutions used

Even though the project is quite simple, it uses a few solutions that are worth mentioning:

+ Containerization with Docker - the project is containerized with Docker, including FastAPI service itself and a test environment database. Whole thing can be run using a single docker-compose command.
+ SQLAlchemy ORM model definitions are implemented using features like relationships, properties, hybrid properties and validations, enabling optimized and clean database operations. (See Plant / Watering models).
+ Pydantic models are used for request/response validation, serialization and deserialization, and are used in the FastAPI endpoints.
+ Object-oriented, dynamic CRUD operations.
+ Tests are written using Pytest and FastAPI's TestClient, with a separate test environment database for isolation. (Although the tests are not yet covering all aspects of the application.)

## To be implemented and/or improved

+ More advanced CRUD operations, including filtering, sorting and pagination for all resources.
+ More tests, including integration tests.
+ Full containerization of the project, including the database. The project should be possible to run with a single command.
+ Database migrations (Alembic).
+ More interactions between users and resources - like sharing plants or watering schedules between users.

