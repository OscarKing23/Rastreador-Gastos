import os
from flask import Flask
from config import config_by_name
from app.database import init_db
from app.routes import main_bp, expenses_bp

def create_app(config_name=None):
    """Application Factory para instanciar y configurar la aplicación Flask."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.abspath(os.path.join(base_dir, '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(base_dir, '..', 'static'))

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )

    # Cargar configuración
    config_class = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config_class)

    # Inicializar Base de Datos
    with app.app_context():
        init_db(app.config['DATABASE_PATH'])

    # Registrar Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(expenses_bp)

    return app
