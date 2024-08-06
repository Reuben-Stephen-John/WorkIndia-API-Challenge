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

- python = "^3.10"
- django = "^5.0.7"
- djangorestframework = "^3.15.2"
- djangorestframework-simplejwt = "^5.3.1"
- django-phonenumber-field = "^8.0.0"
- phonenumbers = "^8.13.42"
- poetry


## Setup

### 1. Clone the Repository

git clone https://github.com/Reuben-Stephen-John/WorkIndia-API-Challenge

3. Install Dependencies
poetry install
4. Apply Migrations
poetry run python manage.py migrate
5. Create Superuser (For Admin Panel)
poetry run python manage.py createsuperuser
6. Run the Development Server
poetry run python manage.py runserver