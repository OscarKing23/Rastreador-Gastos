import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuración base de la aplicación."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
    DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'expenses.db'))
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo."""
    DEBUG = True

class TestingConfig(Config):
    """Configuración para entorno de pruebas unitarias e integración."""
    TESTING = True
    DATABASE_PATH = os.path.join(BASE_DIR, 'test_expenses.db')

class ProductionConfig(Config):
    """Configuración para entorno de producción."""
    DEBUG = False
    DATABASE_PATH = os.environ.get('DATABASE_PATH', '/tmp/expenses.db')


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
