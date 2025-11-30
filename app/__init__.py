from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.context_processor
    def inject_year():
        return {"current_year": datetime.now().year}

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        from . import models
        db.create_all()

    return app
