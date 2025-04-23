import requests
from custom_requester.custom_requester import CustomRequester
from data.project_data import ProjectData

BASE_URL = 'http://localhost:8111'

class TestCreateProject:
    project_data = None
    @classmethod
    def setup_class(cls):
        cls.project_data = ProjectData.create_project_data()
        cls.project_id = cls.project_data['id']

    def test_project_create(self):
        custom_requester = CustomRequester(requests.Session())
        custom_requester.session.auth = ('admin', 'admin')
        token = custom_requester.send_request('GET', '/authenticationTest.html?csrf').text
        custom_requester._update_session_headers(**{'X-TC-CSRF-Token': token})
        create_response = custom_requester.send_request('POST', '/app/rest/projects', self.project_data)

        # assert response_create_project.status_code == 200, f'Error creating project, status code: {str(response_create_project.status_code)}'

        # # Check if project created
        # response_assert_project_exist = requests.get(url=f'{BASE_URL}/app/rest/projects/id:{project_id}', auth=('admin', 'admin'), headers=headers)
        # assert response_assert_project_exist.status_code == 200, f'Project with id {project_id} does not exist'

        # # Delete test project
        # response_delete_test_project = requests.delete(url=f'{BASE_URL}/app/rest/projects/id:{project_id}', auth=('admin', 'admin'), headers=headers)
        # assert response_delete_test_project.status_code == 204, f'Project with id {project_id} was not deleted'
