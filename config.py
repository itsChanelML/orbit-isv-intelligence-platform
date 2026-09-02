import os
from dotenv import load_dotenv

load_dotenv()

_DEV_SECRET_KEY = 'orbit-dev-secret-key'

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', _DEV_SECRET_KEY)
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    # Access codes (role-based auth V1)
    ISV_ACCESS_CODE = os.getenv('ISV_ACCESS_CODE', 'ORBIT-ISV-2025')
    ADMIN_ACCESS_CODE = os.getenv('ADMIN_ACCESS_CODE', 'ORBIT-ADMIN-2025')

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
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour


if not Config.DEBUG and Config.SECRET_KEY == _DEV_SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set. Refusing to start with DEBUG=False and the "
        "default development secret key — set SECRET_KEY in the environment."
    )