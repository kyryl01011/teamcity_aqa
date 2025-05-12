import allure
from pages.build_conf_creation_page import BuildConfCreationPage
from pages.build_conf_page import BuildConfPage
from pages.create_project_page import CreateProjectPage
from pages.launched_build_page import LaunchedBuildPage
from pages.projects_page import ProjectsPage
from data.project_data import ProjectResponseModel

@allure.title('Test create project | UI')
@allure.description('Create new user, create project as new user | UI')
@allure.story('Create project | UI')
@allure.feature('Manage projects | UI')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://www.jetbrains.com/help/teamcity/rest/teamcity-rest-api-documentation.html', name='documentation')
def test_successfully_create_project_manually(authorized_user, project_data, build_conf_data, super_admin):
    with allure.step('Generate project data'):
        fake_project_data = project_data()
    with allure.step(f'Create project manually with name: {fake_project_data.name}, id: {fake_project_data.id}'):
        authorized_user.header.go_to_projects_page()
        proj_page = ProjectsPage(authorized_user.page)
        proj_page.press_create_project_button()
        create_project_page = CreateProjectPage(authorized_user.page)
        create_project_page.create_project_manually(fake_project_data.name, fake_project_data.id)
    with allure.step(f'Check if project with id: {fake_project_data.id} was created'):
        get_created_project_response = super_admin.api_manager.project_api.get_project_by_locator(fake_project_data.id, retries=5)
        assert get_created_project_response.ok, f'Unexpected status code: {get_created_project_response.status_code}, failed to get new project with id: {fake_project_data.id}'
        return fake_project_data

@allure.title('Test create build configuration for project | UI')
@allure.description('Create new user, project and build configuration | UI')
@allure.story('Create build configuration | UI')
@allure.feature('Manage projects | UI')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://www.jetbrains.com/help/teamcity/rest/teamcity-rest-api-documentation.html', name='documentation')
def test_successfully_create_build_conf_data(authorized_user, project_data, build_conf_data, super_admin):
    fake_project_data = test_successfully_create_project_manually(authorized_user, project_data, build_conf_data, super_admin)
    with allure.step(f'Generate fake build conf data for project with id: {fake_project_data.id}'):
        build_conf_creation_page = BuildConfCreationPage(authorized_user.page, fake_project_data.id)
        fake_build_conf_data = build_conf_data(fake_project_data.id)
    with allure.step(f'Create build configuration for project with id: {fake_project_data.id}'):
        build_conf_creation_page.go_to_build_conf_creation_page()
        build_conf_creation_page.creation_method.create_manually()
        build_conf_creation_page.creation_form.fill_manually_creation_form(fake_build_conf_data.name, fake_build_conf_data.id)
        build_conf_creation_page.creation_form.click_create_build_conf_button()
        build_conf_creation_page.wait_for_successful_build_conf_creation()
    with allure.step(f'Check if build configuration with fake build conf id: {fake_build_conf_data.id} was created'):
        get_created_project_response = super_admin.api_manager.project_api.get_project_by_locator(fake_project_data.id, retries=5).text
        created_project_response = ProjectResponseModel.model_validate_json(get_created_project_response)
        all_project_builds = created_project_response.buildTypes.buildType
        assert [True for build in all_project_builds if build.id == fake_build_conf_data.id]
    return fake_build_conf_data

@allure.title('Test run build configuration | UI')
@allure.description('Create new user, project, build configuration and run it | UI')
@allure.story('Run build configuration')
@allure.feature('Manage projects | UI')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://www.jetbrains.com/help/teamcity/rest/teamcity-rest-api-documentation.html', name='documentation')
def test_successfully_run_build(authorized_user, project_data, build_conf_data, super_admin):
    fake_build_conf_data = test_successfully_create_build_conf_data(authorized_user, project_data, build_conf_data, super_admin)
    with allure.step(f'Run created build with id: {fake_build_conf_data.id}'):
        build_conf_page = BuildConfPage(authorized_user.page, fake_build_conf_data.id)
        build_conf_page.go_to_build_conf_page()
        build_conf_page.click_run_build_button()
    with allure.step(f'Go to last launched build and wait for success'):
        launched_build_id = build_conf_page.go_to_launched_build_url()
        launched_build_page = LaunchedBuildPage(authorized_user.page, fake_build_conf_data.id, launched_build_id)
        launched_build_page.wait_for_success()