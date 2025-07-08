# Member registration system
A simple flask web application that allows users to register, log in, view a smart homepage and log out. All with secure password handling using hasing. Built as part of my software development journey.

## Features
- User registration with email, username and password
- passwords are hashed using "werkzeug.sercurity"
- "confirm password" field to prevent mistyped entries
- flash messaging for feedback (errors)
- session management for log in and log out
- prevents duplicate registrations
- '/users' route to view all users (for dev/admin purposes)
- styled using a custom CSS file

  # Technologies used
  - python
  - flask
  - SQLite
  - HTML5
  - CSS3
  - Git & GitHub

  # How to run this app locally
  1. **Clone this repository**
     '''bash
     git clone https://github.com/astong2/member-registration-system.git
     cd member-registration-system
     '''
  2. **Set up virtual environment**
     '''bash
     python -m venv venv
     # for windows
     venv/Scripts/activate
     # for mac/linux
     source venv/bin/activate
     #
     
  4. **install dependencies**
     '''bash
     pip install -r requirements.txt
     '''
  5. **initialize the SQLite database**
     '''bash
     python init_db.py
     '''
  6. **Run the application**
     '''bash
     python app.py
     '''
     Once running, open your browser and go to: https://127.0.0.5000

     # Author
     Created by Aston Grant, as part of my journey into full-stack software development
