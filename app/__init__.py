from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import routes  # ye niche hona chahiye, app ke baad
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career.db'
    app = Flask(__name__, static_folder='static', template_folder='templates')

    db.init_app(app)
    
    from .routes import main
    app.register_blueprint(main)
    
    with app.app_context():
        db.create_all()

    return app
