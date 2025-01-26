# Snake_Game_Python
This Python-based web application, built with Flask, implements a game management system with user authentication, game score tracking, and database integration. 
It uses SQLAlchemy as the ORM for database interactions and integrates HTML templates for dynamic rendering of web pages.

# Compilation

  - Set Up the Database by creating the 'user' and 'games' tables in MySQL
  - Configure Database Credentials --> app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/gamedb'
  - install the required packages --> pip install flask flask_sqlalchemy mysql-connector-python

# Run the Application
  - Use IntelliJ IDEA or a terminal to execute the python main.py file 
  - Access it by opening a browser and going to http://localhost:5000/
