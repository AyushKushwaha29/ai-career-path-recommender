from flask import Flask
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from app import routes  # ye niche hona chahiye, app ke baad
=======
from datetime import datetime

# ---- GLOBAL DB OBJECT (yahaan zaroor hona chahiye) ----
>>>>>>> ae39b29 (Update files)
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
<<<<<<< HEAD
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career.db'
    app = Flask(__name__, static_folder='static', template_folder='templates')

=======
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///career.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ---- DB ko app ke saath init karo ----
>>>>>>> ae39b29 (Update files)
    db.init_app(app)

    # ---- Global context (footer ke year ke liye) ----
    @app.context_processor
    def inject_year():
        return {"current_year": datetime.now().year}

    # ---- Routes / Blueprints register karo ----
    from .routes import main
    app.register_blueprint(main)

    # ---- Models import + tables create ----
    with app.app_context():
        from . import models  # ensure models registered
        db.create_all()

    return app
