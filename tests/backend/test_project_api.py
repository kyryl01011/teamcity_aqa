import allure
from api.api_manager import APIManager
from data.build_conf_data import BuildConfDataResponseModel
from data.project_data import ProjectResponseModel
from enums.roles import Roles

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

    @allure.title('Create Build Conf')
    @allure.description('Create build conf and verify it exists')
    @allure.story('Build Conf creation')
    @allure.feature('Manage projects')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://www.jetbrains.com/help/teamcity/rest/create-and-delete-build-configurations.html', name='documentation')
    def test_create_project_build_conf_as_user(self, super_admin, user_create, project_data, build_conf_data):
        ### Create new project with freshly generated user and fake project data
        with allure.step('Create new test user, project data, build conf data and build run data'):
            new_user = user_create(Roles.PROJECT_ADMIN.value)
            new_user.api_manager.auth_api.auth_and_get_csrf_token(new_user.creds)
            fake_project_data = project_data()
        with allure.step('Send request to create new project'):
            create_project_response = new_user.api_manager.project_api.create_project(fake_project_data.model_dump()).text
            project_response = ProjectResponseModel.model_validate_json(create_project_response)
        with allure.step(f'Check if project {project_response.id} == {fake_project_data.id}'):
            assert project_response.id == fake_project_data.id, f'Expected {fake_project_data.id} but got {project_response.id}'
        ### Create build configuration for created project
        with allure.step(f'Create build conf for created project {project_response.id}'):
            fake_build_conf_data = build_conf_data(fake_project_data.id)
            create_build_conf_response = new_user.api_manager.project_api.create_build_conf(fake_build_conf_data.model_dump()).text
            build_conf_response = BuildConfDataResponseModel.model_validate_json(create_build_conf_response)
        with allure.step(f'Check if {fake_build_conf_data.id} equals {build_conf_response.id}'):
            assert fake_build_conf_data.id == build_conf_response.id, f'Generated build conf id: {fake_build_conf_data.id} not equals to responded build conf id: {build_conf_response.id}'
        ### Run created build configuration
        with allure.step(f'Test run created project build configuration with id: {build_conf_response.id}'):
            pass