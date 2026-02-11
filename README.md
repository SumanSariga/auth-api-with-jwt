# **JWT Authentication API with FastAPI and SQLAlchemy**

This project implements a **JWT-based authentication system** using **FastAPI** and **SQLAlchemy**. It provides secure user registration, login, profile management, and password management features through a RESTful API.

## **Table of Contents**
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Swagger UI](#swagger-ui)
- [API Endpoints](#api-endpoints)


## **Project Overview**
This project allows you to create a secure authentication API using **JWT** tokens for **user management**. Built with **FastAPI**, this application supports features like:
- User registration
- User login and token generation
- Profile viewing and updating
- Password change

This is ideal for applications where user authentication is a crucial feature and can be easily integrated into larger web applications.

## **Features**
- **User Registration**: Allows new users to register by providing email, name, and password.
- **Login**: Allows users to log in using their credentials and obtain a **JWT token**.
- **Profile Management**: Users can view and update their profile (name, email, password).
- **Password Change**: Allows users to change their password by validating the old one.

## **Technology Stack**
- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: JSON Web Tokens (JWT)
- **Password Hashing**: [Passlib](https://passlib.readthedocs.io/en/stable/)
- **Database**: PostgreSQL (can be replaced with any supported DB)
- **Environment Management**: Python v3.7+

## **Installation**

Follow these steps to install and run the project:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/auth-api-with-jwt.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd auth-api-with-jwt
    ```

3. **Set up a virtual environment**:
     ```bash
   uv venv
    ```
    - On **Linux/macOS**:
      ```bash
      source .venv/bin/activate

      ```
    - On **Windows**:
      ```bash
      .venv\Scripts\activate
      ```
  4. **Install dependencies**:
     ```bash
      uv add -r requirements.txt
     ```
     ```bash
      uv sync
     ```

  5. **Run the Application**:
    ```Start the FastAPI application:
     uvicorn app.main:app --reload
    ```

## Usage

### Swagger UI

Once the server is running, you can interact with the API using the Swagger UI at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

The Swagger UI provides a convenient interface for testing the API endpoints. You can register a user, log in, and access protected routes directly from the interface.

### API Endpoints

- **POST /register**: Register a new user by providing email, name, and password.

- **POST /token**: Log in with the email and password to obtain a JWT token.

- **GET /profile**: Retrieve the current user profile. Requires a valid JWT token in the Authorization header.

- **POST /update-profile**: Update the user's name, email, or password.

- **POST /change-password**: Change the user’s password by providing the old and new passwords.

## Swagger UI Screenshot
Below is an image of the Swagger UI showing the available endpoints
<img width="1920" height="1080" alt="Screenshot from 2026-02-11 19-35-27" src="https://github.com/user-attachments/assets/407c5c0b-d565-41bf-8f7b-8d82a84125e4" />


