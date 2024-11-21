# URL Shortener

This is a Django-based web application for shrinking URLs, developed as part of a project task. It allows users to enter long URLs and receive shortened links, making it easier to share them across different platforms. 

## Features

- **URL Shrinking**: Users can input long URLs and generate shorter versions.
- **Dashboard**: View all saved shortened URLs.
- **Search**: Search for specific shortened URLs in the database.
- **Edit & Delete**: Modify or delete saved URLs from the database.
- **Admin Panel**: Access Django's admin panel for managing the app (for staff users).
- **Logout**: Users can log out from the application.

## Project Overview

- **About**: This project is designed to simplify URL sharing by shortening long URLs. It is built using Django for the backend, and it stores the data (URLs and titles) in the database.
- **Project Info**: This project was developed by **R Arjun Krishna** as part of a Django project task.

## How It Works

1. **Enter URL & Title**: 
   - Provide a URL to shorten and give it a title that will be saved in the database.
   
2. **Submit**: 
   - Click the **Submit** button to generate the shortened URL.
   
3. **Shortened URL**: 
   - The shortened URL will appear on the screen.

4. **Reset**: 
   - Click the **Reset** button to input a new URL and title.

5. **View Saved URLs**:
   - Access the **Dashboard** in the navigation bar to view all saved shortened URLs.

6. **Edit/Delete URLs**:
   - The **Edit** and **Delete** buttons allow users to modify or remove URLs from the database.

7. **Search**:
   - Use the **Search** functionality to find a specific URL stored in the database.

8. **Logout**:
   - To log out, click on the **Profile** option in the navigation bar.

## Requirements

- Python 3.x
- Django 3.x or higher

## Installation

1. Clone the repository:
   git clone https://github.com/yourusername/url-shrinking-django.git
   cd url-shrinking-django

2. Install dependencies:
    pip install -r requirements.txt

3. Run migrations to set up the database:
    python manage.py migrate

4. Start the development server:
    python manage.py runserver

5. Visit the app in your browser at http://127.0.0.1:8000/.
