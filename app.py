# main app

from flask import Flask
from models import db
from routes import routes_bp
from flask_jwt_extended import JWTManager
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(debug = True)