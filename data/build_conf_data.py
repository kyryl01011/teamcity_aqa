from pydantic import BaseModel, Field
from typing import Any, Optional, List, Dict

from utils.data_generator import GenerateData


### Pydantic Build Conf Data Block

class Property(BaseModel):
    name: str
    value: str

class BuildConfPropertyList(BaseModel):
    property: List[Property]

class BuildConfStep(BaseModel):
    name: str
    type: str
    properties: BuildConfPropertyList

class BuildConfProject(BaseModel):
    id: str

class BuildConfDataModel(BaseModel):
    id: str
    name: str
    project: BuildConfProject
    steps: BuildConfStep

class BuildConfData:
    @staticmethod
    def create_build_conf_data(project_id) -> BuildConfDataModel:
        return BuildConfDataModel(
            id = GenerateData.fake_project_id(),
            name = GenerateData.fake_name(),
            project = BuildConfProject(id = project_id),
            steps = BuildConfStep(
                name = GenerateData.fake_name(),
                type = GenerateData.fake_name(),
                properties = BuildConfPropertyList(
                    property = [Property(
                        name = 'script.content',
                        value = "echo 'Hello World!'"
                    ), Property(
                        name = 'teamcity.step.mode',
                        value = "default"
                    ), Property(
                        name = 'use.custom.script',
                        value = "true"
                    )]
                )
            )
        )
    

### Build Conf Data Response Model - Pydantic



class ProjectModel(BaseModel):
    id: str
    name: str
    parentProjectId: str
    href: str
    webUrl: str

class SettingsProperty(BaseModel):
    name: str
    value: str

class SettingsModel(BaseModel):
    count: int
    property: List[SettingsProperty]

class ParametersModel(BaseModel):
    href: str
    count: int
    property: List = []

class BuildConfDataResponseModel(BaseModel):
    id: str
    name: str
    projectName: str
    projectId: str
    href: str
    webUrl: str
    project: ProjectModel
    templates: Dict[str, Any] = None
    vcs_root_entries: Dict[str, Any] = Field(None, alias='vcs-root-entries')
    settings: SettingsModel
    parameters: Optional[ParametersModel] = None
    output_parameters: Optional[ParametersModel] = None
    steps: dict = None
    features: dict = None
    triggers: dict = None
    snapshot_dependencies: dict = Field(None, alias='snapshot-dependencies')
    artifact_dependencies: dict = Field(None, alias='artifact-dependencies')
    agent_requirements: dict = Field(None, alias='agent-requirements')
    builds: Dict[str, str]
    investigations: Dict[str, str]
    compatibleAgents: Dict[str, str]
    compatibleCloudImages: Optional[dict] = None
