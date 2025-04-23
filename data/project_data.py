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