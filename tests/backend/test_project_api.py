import allure
from api.api_manager import APIManager
from data.project_data import ProjectResponseModel

BASE_URL = 'http://localhost:8111'

class TestCreateProject:
    # project_data = None
    # @classmethod
    # def setup_class(cls):
    #     cls.project_data = ProjectData.create_project_data()
    #     cls.project_id = cls.project_data.id
    #     cls.build_data = BuildConfData.create_build_conf_data(cls.project_id)
    #     cls.run_build_data = RunBuildData.run_build_data(cls.build_data['id'])

    def test_delete_all_projects(self, super_admin):
        projects_ids = [project.get('id', {}) for project in super_admin.api_manager.project_api.get_projects().json().get('project', [])]
        for project_id in projects_ids:
            if project_id != '_Root':
                super_admin.api_manager.project_api.delete_project(project_id)

    @allure.title('Test project creation')
    @allure.description('Test project creation and if it appears in projects list')
    @allure.feature('Manage projects')
    @allure.story('Project creation')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://www.jetbrains.com/help/teamcity/rest/create-and-delete-projects.html', name='Documentation')
    def test_create_project_as_super_admin(self, super_admin, project_data):
        with allure.step('Set up project data'):
            fake_project_data = project_data()
        with allure.step('Send request to create project'):
            response = super_admin.api_manager.project_api.create_project(fake_project_data.model_dump()).text
            project_response = ProjectResponseModel.model_validate_json(response)
        with allure.step(f'Check if project {project_response.id} == {fake_project_data.id}'):
            assert project_response.id == fake_project_data.id, f'Expected {fake_project_data.id} but got {project_response.id}'
        with allure.step(f'Check if project {fake_project_data.parentProject['locator']} == {project_response.parentProjectId}'):
            assert project_response.parentProjectId == fake_project_data.parentProject['locator'], f'Expected {fake_project_data.parentProject['locator']} but got {project_response.parentProjectId}'

