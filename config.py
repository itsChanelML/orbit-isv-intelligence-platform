import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

# Vercel's filesystem is read-only except /tmp, and /tmp is per-instance and ephemeral.
ON_VERCEL = bool(os.getenv('VERCEL'))
WRITABLE_DATA_DIR = (
    os.path.join(tempfile.gettempdir(), 'orbit_data') if ON_VERCEL
    else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
)

_DEV_SECRET_KEY = 'orbit-dev-secret-key'

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', _DEV_SECRET_KEY)
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    # Access codes (role-based auth V1)
    ISV_ACCESS_CODE = os.getenv('ISV_ACCESS_CODE')
    ADMIN_ACCESS_CODE = os.getenv('ADMIN_ACCESS_CODE')

    # NVIDIA NIM
    NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')
    NVIDIA_BASE_URL = 'https://integrate.api.nvidia.com/v1'

    # NIM Models
    MODEL_PRIMARY = 'nvidia/llama-3.3-nemotron-super-49b-v1'       # Recommendations + chat
    MODEL_INTAKE = 'meta/llama-3.1-8b-instruct'          # Intake processing + learning style
    MODEL_CODEGEN = 'mistralai/mistral-small-4-119b-2603' # Jupyter notebook generation

    # GCP
    GCP_SERVICE_ACCOUNT_KEY = os.getenv('GCP_SERVICE_ACCOUNT_KEY')  # Path to JSON key file
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')

    # SendGrid
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL', 'orbit@nvidia-devrel.com')

    # ipinfo
    IPINFO_TOKEN = os.getenv('IPINFO_TOKEN')

    # Session
    REDIS_URL = os.getenv('REDIS_URL') or os.getenv('KV_URL')
    SESSION_TYPE = 'redis' if REDIS_URL else 'filesystem'
    SESSION_FILE_DIR = os.getenv('SESSION_FILE_DIR', os.path.join(tempfile.gettempdir(), 'orbit_sessions'))
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour


if not Config.DEBUG and Config.SECRET_KEY == _DEV_SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set. Refusing to start with DEBUG=False and the "
        "default development secret key — set SECRET_KEY in the environment."
    )

if not Config.DEBUG:
    _missing = [n for n in ('ISV_ACCESS_CODE', 'ADMIN_ACCESS_CODE') if not getattr(Config, n)]
    if _missing:
        raise RuntimeError(
            "Missing required access codes: " + ", ".join(_missing) +
            " — set them in the environment."
        )
