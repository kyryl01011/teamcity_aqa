from src.custom_requester.custom_requester import CustomRequester


class AgentsApi(CustomRequester):

    def get_unauthorized_agents(self):
        response = self.send_request('GET', '/app/rest/agents?locator=connected:true,authorized:false')
        return response

    def get_all_agents(self):
        response = self.send_request('GET', '/app/rest/agents?locator=authorized:any')
        return response

    def authorize_agent_by_id(self, locator: str):
        self._update_session_headers(**{'Content-Type': 'text/plain', 'Accept': 'text/plain'})
        response = self.send_request('PUT', f'/app/rest/agents/id:{locator}/authorized', json=True)
        self._update_session_headers()
        return response
