from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from miknassa.config import Config




db = SQLAlchemy()

bcrypt = Bcrypt()

migrate = Migrate(db)

loginManager = LoginManager()
loginManager.login_view = 'users.login'
loginManager.login_message_category = 'info'


mail = Mail()




def createApp(config_class=Config):
    app = Flask(__name__)
    app.app_context().push()
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app)
    loginManager.init_app(app)
    mail.init_app(app)

    from miknassa.main.routes import mainBp
    from miknassa.users.routes import usersBp
    from miknassa.application.routes import appBp

    app.register_blueprint(mainBp)
    app.register_blueprint(usersBp)
    app.register_blueprint(appBp)

    return app