import allure
from src.data.build_conf_data import BuildConfDataResponseModel
from src.data.project_data import ProjectResponseModel
from src.data.rub_build_data import RunBuildDataResponse
from src.enums.roles import Roles


class TestProjectManagement:

    # Created for myself
    @allure.title('Clean up projects before tests')
    @allure.description('Sends GET request to receive all existing projects and delete it by their ids')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature('Tests setup')
    def test_delete_all_projects(self, super_admin):
        projects_ids = [project.get('id', {}) for project in
                        super_admin.api_manager.project_api.get_projects().json().get('project', [])]
        for project_id in projects_ids:
            if project_id != '_Root':
                super_admin.api_manager.project_api.delete_project(project_id)

    @allure.title('Test project creation as super-admin')
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
        with allure.step(
                f'Check if project {fake_project_data.parentProject['locator']} == {project_response.parentProjectId}'):
            assert project_response.parentProjectId == fake_project_data.parentProject[
                'locator'], f'Expected {fake_project_data.parentProject['locator']} but got {project_response.parentProjectId}'

    @allure.title('Create project as generated user')
    @allure.description('Super-admin creates new user, new user creates project and verify it exists')
    @allure.story('As project admin create project')
    @allure.feature('Manage projects')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://www.jetbrains.com/help/teamcity/rest/create-and-delete-projects.html', name='documentation')
    def test_successfully_create_project_as_user(self, super_admin, user_create, project_data):
        with allure.step('Create test user with fake user-data, generate fake project data'):
            new_user = user_create(Roles.PROJECT_ADMIN.value)
            new_user.api_manager.auth_api.auth_and_get_csrf_token(new_user.creds)
            fake_project_data = project_data()
        with allure.step('Send request to create new project'):
            create_project_response = new_user.api_manager.project_api.create_project(
                fake_project_data.model_dump()).text
            project_response = ProjectResponseModel.model_validate_json(create_project_response)
        with allure.step(
                f'Check if generated fake project ID: "{project_response.id}" equals ID from respond "{fake_project_data.id}"'):
            assert project_response.id == fake_project_data.id, f'Expected {fake_project_data.id} but got {project_response.id}'
        return project_response, new_user

    @allure.title('Create project build configuration as generated user')
    @allure.description('Super-admin creates new user, new user creates project, project build configuration')
    @allure.story('As project admin create build configuration')
    @allure.feature('Manage projects')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://www.jetbrains.com/help/teamcity/rest/create-and-delete-build-configurations.html',
                 name='documentation')
    def test_successfully_create_build_conf_as_user(self, super_admin, user_create, project_data, build_conf_data):
        project_response, new_user = self.test_successfully_create_project_as_user(super_admin, user_create,
                                                                                   project_data)
        with allure.step(f'Create build conf for created project {project_response.id}'):
            fake_build_conf_data = build_conf_data(project_response.id)
            create_build_conf_response = new_user.api_manager.project_api.create_build_conf(
                fake_build_conf_data.model_dump()).text
            build_conf_response = BuildConfDataResponseModel.model_validate_json(create_build_conf_response)
        with allure.step(
                f'Check if created fake build conf ID: "{fake_build_conf_data.id}" equals ID from respond "{build_conf_response.id}"'):
            assert fake_build_conf_data.id == build_conf_response.id, f'Generated build conf id: {fake_build_conf_data.id} not equals to responded build conf id: {build_conf_response.id}'
        return build_conf_response, new_user

    @allure.title('Run build configuration as generated user')
    @allure.description(
        'Super-admin creates new user, new user creates project, project build configuration and runs it')
    @allure.story('As project admin run build configuration')
    @allure.feature('Manage projects')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://www.jetbrains.com/help/teamcity/rest/start-and-cancel-builds.html', name='documentation')
    def test_successfully_run_build_as_user(self, super_admin, user_create, project_data, run_build_data,
                                            build_conf_data):
        build_conf_response, new_user = self.test_successfully_create_build_conf_as_user(super_admin, user_create,
                                                                                         project_data, build_conf_data)
        with allure.step(f'Test run created project build configuration with id: {build_conf_response.id}'):
            fake_run_build_data = run_build_data(build_conf_response.id)
            run_build_conf_response = new_user.api_manager.project_api.run_build_conf(
                fake_run_build_data.model_dump()).text
            run_build_response = RunBuildDataResponse.model_validate_json(run_build_conf_response)
        with allure.step(
                f'Verify that build with create fake id: "{build_conf_response.id}" equals to build conf that was launched: "{run_build_response.buildTypeId}"'):
            assert run_build_response.buildTypeId == fake_run_build_data.buildType.id, f'Build conf id {fake_run_build_data.buildType.id} not equals {run_build_response.buildTypeId}'
