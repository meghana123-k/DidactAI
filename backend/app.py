from flask import Flask

# Routes
from routes.summarize import summarize_bp
from routes.quiz import quiz_bp
from routes.analytics import analytics_bp
from routes.certificate import certificate_bp

# DB
from db.database import engine, Base, SessionLocal

# IMPORTANT: ensure all models are imported
from models import quiz_attempt, certificate  # noqa: F401


def create_app():
    print("CREATING FLASK APP")

    app = Flask(__name__)

    # --------------------------------------------------
    # Database initialization (ONE TIME)
    # --------------------------------------------------
    Base.metadata.create_all(bind=engine)

    # --------------------------------------------------
    # Session cleanup
    # --------------------------------------------------
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        try:
            SessionLocal.remove()
        except AttributeError:
            pass

    # --------------------------------------------------
    # Register Blueprints
    # --------------------------------------------------
    app.register_blueprint(summarize_bp, url_prefix="/api/summarize")
    app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(certificate_bp, url_prefix="/api/certificate")

    print("BLUEPRINTS REGISTERED")

    return app


app = create_app()

if __name__ == "__main__":
    print("FLASK STARTING")
    app.run(
        debug=True  # OK for now; later switch to env-based config
    )
