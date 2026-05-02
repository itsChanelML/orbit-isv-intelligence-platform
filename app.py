from flask import Flask
from config import Config
from routes.auth import auth_bp
from routes.intake import intake_bp
from routes.output import output_bp
from routes.portal import portal_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(intake_bp)
    app.register_blueprint(output_bp)
    app.register_blueprint(portal_bp)
    app.register_blueprint(admin_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
