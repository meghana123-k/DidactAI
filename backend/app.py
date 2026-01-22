from flask import Flask
from routes.summarize import summarize_bp
from routes.quiz import quiz_bp
from routes.analytics import analytics_bp
from routes.certificate import certificate_bp
from db.database import engine, Base
from db import models
from db import SessionLocal
Base.metadata.create_all(bind=engine)

def create_app():
    print("CREATING FLASK APP")

    app = Flask(__name__)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        SessionLocal.remove()
    print("BLUEPRINTS REGISTERED")
    app.register_blueprint(summarize_bp, url_prefix="/api/summarize")
    app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(certificate_bp, url_prefix="/api/certificate")
    return app


app = create_app()

if __name__ == "__main__":
    print("FLASK STARTING")
    app.run(debug=True)
