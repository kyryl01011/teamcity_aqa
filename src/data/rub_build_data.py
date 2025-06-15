from typing import Dict, Optional, List

from pydantic import BaseModel

### Pydantic Rub Build Data Block

class BuildTypeResponse(BaseModel):
    id: str
    name: str
    projectName: str
    projectId: str
    href: str
    webUrl: str

class UserResponse(BaseModel):
    username: str
    id: int
    href: str

class TriggeredResponse(BaseModel):
    type: str
    date: str
    user: UserResponse

class RunBuildDataResponse(BaseModel):
    id: int
    buildTypeId: str
    state: str
    href: str
    webUrl: str
    buildType: BuildTypeResponse
    waitReason: str
    queuedDate: str
    triggered: TriggeredResponse
    changes: Dict[str, str]
    revisions: Optional[Dict[str, int]] = None
    compatibleAgents: Dict[str, str]
    artifacts: Dict[str, str]
    vcsLabels: Optional[List] = None
    customization: Optional[Dict] = None



class BuildType(BaseModel):
    id: str

class RunBuildDataModel(BaseModel):
    buildType: BuildType

class RunBuildData:
    @staticmethod
    def create_run_build_data(build_id) -> RunBuildDataModel:
        return RunBuildDataModel(buildType = BuildType(id = build_id))