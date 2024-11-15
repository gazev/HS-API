import os
import secrets

from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__)) + "/.." # the repository folder 

def _get_env_or_default(env: str, default: str, cast=None):
    val = os.environ.get(env, "")
    if not val:
        return default

    return cast(val) if cast is not None else val

def _get_int_env_or_default(env: str, default: int) -> int:
    try:
        return _get_env_or_default(env, default, int)
    except ValueError:
        return default

class Config:
    SECRET_KEY = _get_env_or_default("SECRET_KEY", secrets.token_hex(256))

    SESSION_TYPE                 = "filesystem"
    PERMANENT_SESSION            = True 
    SESSION_REFRESH_EACH_REQUEST = False
    PERMANENT_SESSION_LIFETIME   = _get_int_env_or_default("SESSION_LIFETIME", 12 * 60 * 60)
    SESSION_KEY_PREFIX           = _get_env_or_default("SESSION_KEY_PREFIX", "hs_session_")
    SESSION_FILE_DIR             = os.path.join(basedir, _get_env_or_default("SESSION_DIR", "data/flask_sessions/")).rstrip("/")

    ROLES_PATH = os.path.join(basedir, _get_env_or_default("ROLES_PATH", "data/roles.json"))

    DATABASE_PATH           = os.path.join(basedir, _get_env_or_default("DATABASE_PATH", "data/hackerschool.sqlite3"))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

    PHOTOS_DIR         = os.path.join(basedir, _get_env_or_default("PHOTOS_DIR", "data/photos/")).rstrip("/")
    MAX_CONTENT_LENGTH = _get_int_env_or_default("MAX_PHOTO_SIZE", 16 * 1000 * 1000) ## max pohto size

    print(_get_env_or_default("LOGS_PATH", ""))
    LOGS_PATH = os.path.join(basedir, _get_env_or_default("LOGS_PATH", ""))
    print(LOGS_PATH)
    LOG_LEVEL = _get_env_or_default("LOG_LEVEL", "INFO")

    ADMIN_USERNAME = _get_env_or_default("ADMIN_USERNAME", "")
    ADMIN_PASSWORD = _get_env_or_default("ADMIN_PASSWORD", "")