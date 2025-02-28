from flask import Flask

from models.database import db
from routes.bot_routes import bots_routes
from routes.order_routes import order_routes
from routes.user_routes import user_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(user_routes, url_prefix="/api")
    app.register_blueprint(bots_routes, url_prefix="/bots")
    app.register_blueprint(order_routes, url_prefix="/orders")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000)
