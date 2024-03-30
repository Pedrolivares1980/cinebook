Cinebook Project

Introduction

Cinebook is a Django based web application designed for the final assessment on the Full Stack Web Developer course from UCD Professional Academy.

This project is a cinema booking ticket web app called MovieTicket, where the user can filter and book in a range of showtimes, view the movie details and book the seats he prefers, after he confirms the booking the web app sends a confirmation email with the booking information and a QR code to retrieve the ticket at the cinema.The users can register, login, and update the profile, check all his bookings, cancel the bookings or resend the email confirmation. When the user cancels the booking, also receive an email with the booking cancellation. Also the users can go to our blog app where he can post, comment, and like or unlike posts and comments.
The admin or staff members can also go to an admin dashboard, where they can add different cinemas, screening rooms with 3 different sizes and then the system will calculate how many rows the room has with 10 seats each to be rendered in the booking app, showtimes and movies. The Movies have an input with a movie suggestion script where the staff member writes the 3 first letters from the title movie and then can choose from the movies in <https://www.themoviedb.org/> through the api we fetch all movie data to our database. When the showtimes have passed the system doesn't list the showtimes.
This guide will walk you through the steps to get CineBook up and running on your local machine for development and testing purposes, the project is deployed on render.com and on Amazon S3 for the management of the uploaded images.
Getting Started These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Prerequisites Before you begin, ensure you have the following installed:
• Python (version 3.8 or later)
• pip (Python package installer)
• Git (version control system)
Cloning the Repository To clone the CineBook project from GitHub to your local machine, run the following command in your terminal:
 git clone <https://github.com/Pedrolivares1980/cinebook>
Installing Dependencies Navigate to the project directory and install the required Python packages using pip:
 cd CineBook pip install -r requirements.txt

Setting Up the Development Environment Before running the application, you need to set up your development environment. Create a .env file in the project root directory to store your environment variables, such as your secret key, database configurations, email host and admin user.
Running the Application To run the application on your local machine, execute the following command:
 python manage.py runserver

The project is deployed at <https://cinebook.onrender.com>.
Feel free to register and discover all the features and possibilities of the project.

Features

Staff Members

They can:

-Add Movies fetching from through the TMDb API, the system have a script for  a movie suggestion, and delete Movies
-Add Cinemas or delete them.
-Add Screening rooms to the cinemas choosing the capacity between 3 different sizes, the app will calculate how many rows the room will have, and then in the booking app the script goes to render the seats and the rows to be selected for the user.
-Add Showtimes for a movie in the screening room to be listed in the web app for the users to filter, show details and book seats.
-Check the users details, delete the users to change the status to staff.
-Check all the bookings in the system and cancel them.

Users Members

They can:

-Register, Login, logout, reset password if they forgot, and delete the account and all data related.
-Post, comment and like and unlike in our blog.
-Show the showtimes, filter them, show the movie details, and book up to 4 seats for each showtime.
-With the confirmation email, you can go to the cinema and print the tickets after scanning the qr code.
-Go to the profile section and update the user information, check the current bookings, resend the email confirmation or cancel the booking.
