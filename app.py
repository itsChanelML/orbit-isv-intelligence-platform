import os
from flask import Flask
from flask_session import Session
from config import Config
from routes.auth import auth_bp
from routes.intake import intake_bp
from routes.output import output_bp
from routes.portal import portal_bp
from routes.admin import admin_bp
from routes.documents import documents_bp
from routes.community import community_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
    Session(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(intake_bp)
    app.register_blueprint(output_bp)
    app.register_blueprint(portal_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(community_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG, port=5000)