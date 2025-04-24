from api.auth_api import AuthAPI
from api.project_api import ProjectAPI


class APIManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.project_api = ProjectAPI(session)

    