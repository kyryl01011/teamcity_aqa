from enums.hosts import BASE_URL


class TestAuthorizeAgent:

    def test_authorize_agent(self, super_admin):
        agents_list = super_admin.api_manager.agents_api.get_all_agents().json()['agent']
        assert len(agents_list) > 0, f'List of agents is empty: {agents_list}'
        first_agent_id_locator = agents_list[0]['id']
        authorize_response = super_admin.api_manager.agents_api.authorize_agent_by_id(first_agent_id_locator)
        print(authorize_response.text)