from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "beeb729ffffb25428e39687d507ea476f105a5ab523b1db753f0830df3893cf4"

    # Registrar blueprints
    from app.routes import main_bp # type: ignore
    app.register_blueprint(main_bp)

    return app