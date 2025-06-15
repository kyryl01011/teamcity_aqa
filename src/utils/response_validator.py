from typing import TypeVar, Type

import pytest
from pydantic import BaseModel
from requests import Response


ModelType = TypeVar('ModelType', bound=BaseModel)


def validate_response(response: Response, model: Type[ModelType] | None, expected_status: int = 200,
                      data_to_compare: ModelType | None = None):
    try:
        response_dict: dict = response.json()
    except Exception as e:
        pytest.fail(f'Failed to parse response JSON:\n'
                    f'Response body: {response.text}\n'
                    f'Error: {e}')

    if model:
        try:
            response_model: ModelType = model(**response_dict)
        except Exception as e:
            pytest.fail(f'Failed to parse response to model {model.__name__}\nError: {e}')

    if expected_status != response.status_code:
        pytest.fail(f'Actual response status code not equals to expected:\n'
                    f'Actual: {response.status_code}\n'
                    f'Expected: {expected_status}')

    if data_to_compare:
        if response_model.model_dump(exclude_unset=True) != data_to_compare.model_dump(exclude_unset=True):
            pytest.fail(f'Response data not equals to expected:\n'
                        f'Response: {response_model.model_dump(exclude_unset=True)}'
                        f'Expected: {data_to_compare.model_dump(exclude_unset=True)}')
