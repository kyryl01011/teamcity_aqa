from utils.data_generator import GenerateData

class ProjectData:
    @staticmethod
    def create_project_data():
        return {
               "parentProject": {"locator": "_Root"},
               "name": GenerateData.fake_name(),
               "id": GenerateData.fake_project_id(),
               "copyAllAssociatedSettings": True
               }
    
class BuildConfData:
    def __init__(self, project_id):
        pass

    @staticmethod
    def create_build_conf_data(project_id):
        return {
                "id": GenerateData.fake_project_id(),
                "name": GenerateData.fake_name(),
                "project": {
                    "id": project_id
                },
                "steps": {
                    "step": [
                        {
                            "name": "myCommandLineStep",
                            "type": "simpleRunner",
                            "properties": {
                                "property": [
                                    {
                                        "name": "script.content",
                                        "value": "echo 'Hello World!'"
                                    },
                                    {
                                        "name": "teamcity.step.mode",
                                        "value": "default"
                                    },
                                    {
                                        "name": "use.custom.script",
                                        "value": "true"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }