from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import MetaData
from flask_cors import CORS

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(render_as_batch=True)
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    login.login_view = 'login'

    # Import and register blueprints
    from .pot.pot import pot as pot_blueprint
    app.register_blueprint(pot_blueprint)
    
    from .clay.clay import clay as clay_blueprint
    app.register_blueprint(clay_blueprint)
    
    from .glaze.glaze import glaze as glaze_blueprint
    app.register_blueprint(glaze_blueprint)
    
    from .link.link import link as link_blueprint
    app.register_blueprint(link_blueprint)
    
    return app