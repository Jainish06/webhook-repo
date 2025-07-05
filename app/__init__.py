# from flask import Flask
#
# from app.webhook.routes import webhook
#
#
# # Creating our flask app
# def create_app():
#
#     app = Flask(__name__)
#
#     # registering all the blueprints
#     app.register_blueprint(webhook)
#
#     return app
#

from flask import Flask
from app.extensions import mongo
from app.webhook.routes import main


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize MongoDB
    mongo.init_app(app)
    print("DB connected")

    # Register routes
    app.register_blueprint(main)

    return app