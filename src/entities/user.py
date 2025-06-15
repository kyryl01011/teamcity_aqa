

from src.api.api_manager import APIManager
from src.enums.roles import Roles


class Role:
    def __init__(self, role_id, scope='g', href=None):
        if role_id not in Roles.__members__:
            raise ValueError(f'{role_id} is not supported role_id')
        self.role_id = role_id
        self.scope = scope
        self.href = href

class User:
    def __init__(self, username: str, password: str, email: str, roles: list, api_manager: APIManager, **kwargs):
        self.username = username
        self.password = password
        self.email = email
        self.roles = roles
        self.api_manager = api_manager # requests.Session (APIManager) object to work with
        self.groups = None

    @property
    def creds(self):
        return self.username, self.password