import os
from flask import Flask
from App.routes.validate import validation_bp as card
from App.routes.lookup import bin_lookup_bp as lookup
from dotenv import load_dotenv
from flasgger import Swagger


# Load environment variables
load_dotenv()

# Create a Flask application instance
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(os.environ.get('APP_SETTINGS'))
    swagger = Swagger(app)

    # Register the validation blueprint
    app.register_blueprint(card)
    app.register_blueprint(lookup)


    return app
