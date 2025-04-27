from typing import List, Optional, Dict
from pydantic import BaseModel

from utils.data_generator import GenerateData

class ProjectDataModel(BaseModel):
    parentProject: dict
    name: str
    id: str
    copyAllAssociatedSettings: bool

class ParentProjectModel(BaseModel):
    id: str
    name: str
    description: str
    href: str
    webUrl: str

class BuildTypes(BaseModel):
    count: int
    buildType: list = []

class Templates(BaseModel):
    count: int
    buildType: list[BuildTypes] = []

class ParametersModel(BaseModel):
    property: list = []
    count: int
    href: str

class ProjectResponseModel(BaseModel):
    id: str
    name: str
    parentProjectId: str
    virtual: bool
    description: Optional[str] = None
    href: str
    webUrl: str
    parentProject: ParentProjectModel
    buildTypes: Optional[BuildTypes] = None
    templates: Optional[Templates] = None
    deploymentDashboards: Optional[dict[str, int]] = None
    parameters: Optional[ParametersModel] = None
    vcsRoots: dict
    projectFeatures: dict
    projects: dict

    class Config:
        extra = "allow"

class ProjectData:
    @staticmethod
    def create_project_data() -> ProjectDataModel:
        return ProjectDataModel(
               parentProject = {"locator": "_Root"},
               name = GenerateData.fake_name(),
               id = GenerateData.fake_project_id(),
               copyAllAssociatedSettings = True
        )


# class BuildConfData:
#     def __init__(self, project_id):
#         pass

#     @staticmethod
#     def create_build_conf_data(project_id):
#         return {
#                 "id": GenerateData.fake_project_id(),
#                 "name": GenerateData.fake_name(),
#                 "project": {
#                     "id": project_id
#                 },
#                 "steps": {
#                     "step": [
#                         {
#                             "name": "myCommandLineStep",
#                             "type": "simpleRunner",
#                             "properties": {
#                                 "property": [
#                                     {
#                                         "name": "script.content",
#                                         "value": "echo 'Hello World!'"
#                                     },
#                                     {
#                                         "name": "teamcity.step.mode",
#                                         "value": "default"
#                                     },
#                                     {
#                                         "name": "use.custom.script",
#                                         "value": "true"
#                                     }
#                                 ]
#                             }
#                         }
#                     ]
#                 }
#             }
    

### Pydantic Rub Build Data Block

class BuildTypeModel(BaseModel):
    id: str

class RunBuildDataModel(BaseModel):
    buildType: BuildTypeModel

class RunBuildData:
    def __init__(self, build_id):
        pass

    @staticmethod
    def run_build_data(build_id):
        return {"buildType": {"id": build_id}}