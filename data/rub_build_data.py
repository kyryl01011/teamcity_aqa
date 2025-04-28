from pydantic import BaseModel

### Pydantic Rub Build Data Block

class BuildType(BaseModel):
    id: str

class RunBuildDataModel(BaseModel):
    buildType: BuildType

class RunBuildData:
    @staticmethod
    def create_run_build_data(build_id) -> RunBuildDataModel:
        return RunBuildDataModel(buildType = BuildType(id = build_id))