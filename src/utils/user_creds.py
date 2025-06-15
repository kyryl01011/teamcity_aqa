import os
from dotenv import load_dotenv

load_dotenv()

class SuperAdminCreds:
    """
    Class to control super admin creds. Leave username blank and get super user token from docker logs
    """
    USERNAME = ''
    PASSWORD = os.getenv('SUPER_USER_TOKEN')