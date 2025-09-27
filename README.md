# Task-Management---RESTFUL-API
This is a simple  Task Management API built with Flask, which lets users to register and log in. Once logged in they can create, view, update, and delete their tasks securely.  The API uses tokens (JWT) to keep user data safe and ensures each user can only manage their own tasks. The user can also filter tasks by their completion status.

Features
 * User registration and login with password hashing
 * JWT-based authentication and authorization
 * Create, read, update, and delete tasks
 * Query tasks by completion status
 * Task ownership enforced — users only access their own tasks

Tech Stack
  * Python 3.x
  * Flask
  * Flask-JWT-Extended
  * SQLAlchemy ORM
  * Flask-Migrate for database migrations
  * SQLite as the database (configurable)
