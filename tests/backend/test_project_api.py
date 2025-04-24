from importlib.metadata import pass_none

import requests

from data.project_data import ProjectData, BuildConfData, RunBuildData

BASE_URL = 'http://localhost:8111'

class TestCreateProject:
    project_data = None
    @classmethod
    def setup_class(cls):
        cls.project_data = ProjectData.create_project_data()
        cls.project_id = cls.project_data['id']
        cls.build_data = BuildConfData.create_build_conf_data(cls.project_id)
        cls.run_build_data = RunBuildData.run_build_data(cls.build_data['id'])

    def test_project_create(self, api_manager):
        create_project_response = api_manager.project_api.create_project(self.project_data).json()
        assert create_project_response.get('id', {}) == self.project_id
        current_projects_list = api_manager.project_api.get_projects().json().get('project', [])
        projects_ids = [project.get('id', {}) for project in current_projects_list]
        assert self.project_id in projects_ids
        api_manager.project_api.clean_up_project(self.project_id)

    def test_delete_all_projects(self, api_manager):
        projects_ids = [project.get('id', {}) for project in api_manager.project_api.get_projects().json().get('project', [])]
        for project_id in projects_ids:
            if project_id != '_Root':
                api_manager.project_api.delete_project(project_id)