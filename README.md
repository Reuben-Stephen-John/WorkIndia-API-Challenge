# Dining Place Booking System

## Overview

This Django application is designed to manage dining place bookings. It includes functionalities for user registration, login, dining place management, and booking. The project uses Django's REST framework for API endpoints and includes encryption for stored notes.

## Features

- User account registration and login
- Create and manage dining places
- Check availability of dining places
- Make bookings for dining places
- Search for dining places by name

## Requirements

- Python 3.8+
- Django 4.0+
- Django REST framework
- `phonenumber_field` library

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Reuben-Stephen-John/WorkIndia-API-Challenge.git
```

### 2. Install Poetry

If you don't have Poetry installed, you can install it by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

### 3. Install Dependencies

```bash
poetry install
```

### 4. Apply Migrations

```bash
poetry run python manage.py migrate
```

### 5. Create Superuser (For Admin Panel)

```bash
poetry run python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
poetry run python manage.py runserver
```

## API Endpoints

### User Registration

- **POST** `/api/user/register/`

  **Request Data:**

  ```json
  {
    "username": "example_user",
    "password": "example_password"
  }
  ```

  **Response Data:**

  ```json
  {
    "status": "account created"
  }
  ```

### User Login

- **POST** `/api/user/login/`

  **Request Data:**

  ```json
  {
    "username": "example_user",
    "password": "example_password"
  }
  ```

  **Response Data:**

  ```json
  {
    "status": "Login successful",
    "status_code": 200,
    "user_id": "12345",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
  }
  ```

### List Saved Notes

- **GET** `/api/notes/list/?user={userId}`

  **Request Data:** None

  **Response Data:**

  ```json
  [
    {
      "note_id": 1,
      "note": "Sample note text"
    }
  ]
  ```

### Save a New Note

- **POST** `/api/notes/`

  **Request Data:**

  ```json
  {
    "user_id": "12345",
    "note": "Sample note text"
  }
  ```

  **Response Data:**

  ```json
  {
    "status": "success"
  }
  ```

### Search Dining Places by Name

- **GET** `/api/dining-place?name={search_query}`

  **Params:**

  - `search_query` (str): The keyword to search for in dining place names.

  **Response Data:**

  ```json
  [
    {
      "place_id": "12345",
      "name": "Gatsby",
      "address": "HSR Layout",
      "phone_no": "+9999999999",
      "website": "http://workindia.in/",
      "operational_hours": {
        "open_time": "08:00:00",
        "close_time": "23:00:00"
      }
    }
  ]
  ```

### Check Dining Place Availability

- **GET** `/api/dining-place/availability`

  **Params:**

  - `place_id` (str): The ID of the dining place.
  - `start_time` (datetime): The start time of the requested slot.
  - `end_time` (datetime): The end time of the requested slot.

  **Response Data:**

  ```json
  {
    "place_id": "12345",
    "name": "Gatsby",
    "phone_no": "+9999999999",
    "available": false,
    "next_available_slot": "2024-01-01T17:00:00Z"
  }
  ```

### Make a Booking

- **POST** `/api/dining-place/booking/`

  **Request Data:**

  ```json
  {
    "place_id": "12345",
    "start_time": "2024-01-01T16:00:00Z",
    "end_time": "2024-01-01T17:00:00Z"
  }
  ```

  **Response Data:**

  ```json
  {
    "status": "Booking successful",
    "booking_id": 1
  }
  ```

## Notes

- Ensure to handle authentication by including the `Authorization` header with the token for endpoints that require it.
- Admin endpoints are protected by an API key. Make sure to include the key in the request headers when accessing these endpoints.
