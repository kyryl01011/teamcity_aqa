import requests
from custom_requester.custom_requester import CustomRequester
from data.project_data import ProjectData, BuildConfData

BASE_URL = 'http://localhost:8111'

class TestCreateProject:
    project_data = None
    @classmethod
    def setup_class(cls):
        cls.project_data = ProjectData.create_project_data()
        cls.project_id = cls.project_data['id']
        cls.build_data = BuildConfData.create_build_conf_data(cls.project_id)

    def test_project_create(self):
        custom_requester = CustomRequester(requests.Session())
        custom_requester.session.auth = ('admin', 'admin')
        token = custom_requester.send_request('GET', '/authenticationTest.html?csrf').text
        custom_requester._update_session_headers(**{'X-TC-CSRF-Token': token})
        create_response = custom_requester.send_request('POST', '/app/rest/projects', self.project_data)

    def test_build_create(self):
        custom_requester = CustomRequester(requests.Session())
        custom_requester.session.auth = ('admin', 'admin')
        token = custom_requester.send_request('GET', '/authenticationTest.html?csrf').text
        custom_requester._update_session_headers(**{'X-TC-CSRF-Token': token})
        create_build_response = custom_requester.send_request('POST', '/app/rest/buildTypes', self.build_data)

