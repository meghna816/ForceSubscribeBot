#Config.py
import os

# Check if the environment is set to production or development
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

# Common configuration values
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', None)
BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
DATABASE_URL = os.environ.get('DATABASE_URL', None)

# For channels/groups to be joined using IDs (comma-separated IDs)
MUST_JOIN = os.environ.get('MUST_JOIN', "").split(',')  # Channel IDs

# For private channels/groups using IDs (comma-separated IDs)
PRIVATE_GROUPS = os.environ.get('PRIVATE_GROUPS', "").split(',')  # Private Group IDs

# Validate critical variables
if ENVIRONMENT == 'production':
    if not API_ID or not API_HASH or not BOT_TOKEN or not DATABASE_URL:
        raise Exception("Missing critical environment variables for production environment!")

    # Adjust database URL if required
    if DATABASE_URL and "postgres" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")

else:
    # Default development values
    API_ID = 0
    API_HASH = ""
    BOT_TOKEN = ""
    DATABASE_URL = ""
    MUST_JOIN = ["123456", "654321"]  # Default chat to join (use IDs)
    PRIVATE_GROUPS = ["234567", "876543"]  # Example private group IDs

# Developer list (can be expanded in production)
DEVS = [1744109441, 1946995626]
