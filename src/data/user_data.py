

from src.enums.roles import Roles
from src.utils.data_generator import GenerateData


class UserData:
    @staticmethod
    def create_user_data(role=Roles.SYSTEM_ADMIN.value, scope='g'):
        return {
            'username': GenerateData.fake_name(),
            'password': GenerateData.fake_project_id(),
            'email': GenerateData.fake_email(),
            'roles': {
                'role': [
                {
                    'roleId': role,
                    'scope': scope
                }
            ]
            }
                
        }