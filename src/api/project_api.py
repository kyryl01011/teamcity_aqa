import time
from http import HTTPStatus

import allure

from src.custom_requester.custom_requester import CustomRequester


class ProjectAPI(CustomRequester):

    def get_project_by_locator(self, locator, retries=1):
        with allure.step(f'Check if project with locator: {locator} exists on server with {retries} retries'):
            for attempt in range(retries + 1):
                try:
                    response = self.send_request("GET", f"/app/rest/projects/id:{locator}")
                    return response
                except ValueError as e:
                    if attempt <= retries:
                        time.sleep(1)
                        continue
                    else:
                        raise e
            return None

    def create_project(self, project_data, expected_status_code=HTTPStatus.OK):
        with allure.step(f'Create project with data: {project_data}'):
            return self.send_request('POST', '/app/rest/projects', json=project_data,
                                     expected_status=expected_status_code)

    def create_build_conf(self, build_conf_data, expected_status_code=HTTPStatus.OK):
        with allure.step(f'Create build configuration with data: {build_conf_data}'):
            return self.send_request('POST', '/app/rest/buildTypes', json=build_conf_data,
                                     expected_status=expected_status_code)

    def run_build_conf(self, run_conf_data, expected_status_code=HTTPStatus.OK):
        with allure.step(f'Run build configuration with data: {run_conf_data}'):
            return self.send_request('POST', '/app/rest/buildQueue', json=run_conf_data,
                                     expected_status=expected_status_code)

    def get_projects(self):
        with allure.step(f'Get projects list'):
            return self.send_request('GET', '/app/rest/projects')

    def delete_project(self, project_id):
        with allure.step(f'Delete project with id: "{project_id}"'):
            return self.send_request('DELETE', f'/app/rest/projects/id:{project_id}', expected_status=204)

    def clean_up_project(self, created_project_id):
        with allure.step(f'Clean up projects with id {created_project_id}'):
            self.send_request('DELETE', f'/app/rest/projects/id:{created_project_id}', expected_status=204)
            projects = self.get_projects().json()
            projects_ids = [projects.get('id', {}) for project in projects.get('project', [])]
            assert created_project_id not in projects_ids, f'Project {created_project_id} still exists in projects after removal'
