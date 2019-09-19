import os


VECTOR_SEPARATOR = ','
CHANGE_STEP = 1
RANGE = (1, 100)
API_TOKEN = "f8d95800c8c24a5f980bf6865f9cf405"
API_URL = "https://api.dandelion.eu/datatxt/nex/v1/"
REQUIRE_REBUILD_CONST = 0.1


class DataBaseConfiguration:
    @classmethod
    def build_connection_string(cls):
        return "{PROVIDER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{NAME}"\
                .format(**cls.__dict__)


class PSQLConfiguration(DataBaseConfiguration):
    PROVIDER = 'postgresql'
    USERNAME = 'postgres'
    PASSWORD = 'postgres'
    HOST = 'localhost'
    PORT = '5432'
    NAME = 'annochatty_analyze'


class Config:
    SQL_DB_PATH = '%s/db.sqlite3' % os.path.abspath(os.pardir)
    SQLALCHEMY_DATABASE_URI = 'sqlite:////%s' % SQL_DB_PATH


class DevConfig(Config):
    _DB_CONFIG = PSQLConfiguration
    SQLALCHEMY_DATABASE_URI = _DB_CONFIG.build_connection_string()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
