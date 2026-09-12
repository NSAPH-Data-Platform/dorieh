import os

# ── Metadata database (Superset internal) ─────────────────────────────────────
_db_host = os.environ["DATABASE_HOST"]
_db_port = os.environ.get("DATABASE_PORT", "5432")
_db_user = os.environ["DATABASE_USER"]
_db_pass = os.environ["DATABASE_PASSWORD"]
_db_name = os.environ["DATABASE_DB"]

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{_db_user}:{_db_pass}@{_db_host}:{_db_port}/{_db_name}"
)

# ── Security ───────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ["SECRET_KEY"]

# ── Redis ──────────────────────────────────────────────────────────────────────
_redis_host = os.environ.get("REDIS_HOST", "redis")
_redis_port = os.environ.get("REDIS_PORT", "6379")
_redis_base  = f"redis://{_redis_host}:{_redis_port}"

# ── Cache ──────────────────────────────────────────────────────────────────────
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": _redis_host,
    "CACHE_REDIS_PORT": int(_redis_port),
    "CACHE_REDIS_DB": 1,
}
DATA_CACHE_CONFIG = {**CACHE_CONFIG, "CACHE_KEY_PREFIX": "superset_data_"}

# ── Celery (async queries / alerts / reports) ──────────────────────────────────
class CeleryConfig:
    broker_url     = f"{_redis_base}/0"
    result_backend = f"{_redis_base}/0"
    imports        = ("superset.sql_lab",)
    worker_prefetch_multiplier = 1
    task_acks_late = False

CELERY_CONFIG = CeleryConfig

# ── Feature flags ──────────────────────────────────────────────────────────────
FEATURE_FLAGS = {"ALERT_REPORTS": True}

# Allow connections to internal Docker hostnames
PREVENT_UNSAFE_DB_CONNECTIONS = False