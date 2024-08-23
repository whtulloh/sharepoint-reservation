# Importing the necessary modules and libraries
import logging
import sys
import os
from flask import Flask
from flask_cors import CORS
from src.routes.reservationRoutes import reservationBlueprint

def create_app():
    
    app = Flask(__name__)  # flask app object
    app.config.from_object('config')  # Configuring from Python Files
    CORS(app) # Enabling CORS

    # Set up logging
    logging.basicConfig(filename="/var/www/rsvdemo/app.log", level=logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    # Registering the blueprint
    app.register_blueprint(reservationBlueprint, url_prefix='/reservation')

    return app

# Creating the app
app = create_app()  