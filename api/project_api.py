from http import HTTPStatus

from custom_requester.custom_requester import CustomRequester


class ProjectAPI(CustomRequester):
    def get_project_by_locator(self, locator):
        return self.send_request("GET", f"/app/rest/projects/{locator}")

    def create_project(self, project_data, expected_status_code=HTTPStatus.OK):
        return self.send_request('POST', '/app/rest/projects', project_data, expected_status_code)

    def get_projects(self):
        return self.send_request('GET', '/app/rest/projects')

    def delete_project(self, project_id):
        return self.send_request('DELETE', f'/app/rest/projects/id:{project_id}', expected_status=204)

    def clean_up_project(self, created_project_id):
        self.send_request('DELETE', f'/app/rest/projects/id:{created_project_id}', expected_status=204)
        projects = self.get_projects().json()
        projects_ids = [projects.get('id', {}) for project in projects.get('project', [])]
        assert created_project_id not in projects_ids, f'Project {created_project_id} still exists in projects after removal'