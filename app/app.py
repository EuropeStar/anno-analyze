from app.configs import DevConfig
from flask import Flask
from app.models import db
from app.router import analyzer


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(analyzer)
    return app
