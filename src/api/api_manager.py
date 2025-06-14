from src.api.agents_api import AgentsApi
from src.api.auth_api import AuthAPI
from src.api.project_api import ProjectAPI
from src.api.user_api import UserAPI
from requests import Session


class APIManager:
    def __init__(self, session: Session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.project_api = ProjectAPI(session)
        self.user_api = UserAPI(session)
        self.agents_api = AgentsApi(session)
                                
    def close_session(self):
        self.session.close()

    