from datetime import datetime

from models.my_model import MyModel, MyModelRequest, MyModelResponse, MyModelSchema


def test_my_model_creation():
    obj = MyModel(field1="Test 1", field2=True)

    assert obj.field1 == "Test 1"
    assert obj.field2 == True
    assert obj.id is None


def test_my_model_schema_from_orm():
    obj = MyModel(field1="Test Field 1", field2=False)
    obj.id = 1
    obj.created_at = datetime(2023, 1, 1, 12, 0, 0)
    obj.updated_at = datetime(2023, 1, 1, 12, 0, 0)

    schema = MyModelSchema.model_validate(obj)

    assert schema.id == 1
    assert schema.field1 == "Test Field 1"
    assert schema.field2 == False
    assert schema.created_at == datetime(2023, 1, 1, 12, 0, 0)
    assert schema.updated_at == datetime(2023, 1, 1, 12, 0, 0)


def test_my_model_response_with_none():
    response = MyModelResponse(message="Test message", model=None)

    data = response.model_dump()

    assert data["message"] == "Test message"
    assert data["model"] is None


def test_my_model_response_with_valid_model():
    obj = MyModel(field1="Test Field 1", field2=False)
    obj.id = 1
    obj.created_at = datetime(2023, 1, 1, 12, 0, 0)
    obj.updated_at = datetime(2023, 1, 1, 12, 0, 0)

    response = MyModelResponse(message="Test message", model=obj)

    data = response.model_dump()

    assert data["message"] == "Test message"
    assert data["model"] is not None
    assert data["model"]["id"] == 1
    assert data["model"]["field1"] == "Test Field 1"
    assert data["model"]["field2"] == False
    assert data["model"]["created_at"] == datetime(2023, 1, 1, 12, 0, 0)
    assert data["model"]["updated_at"] == datetime(2023, 1, 1, 12, 0, 0)


def test_my_model_request_validation():
    request = MyModelRequest(field1="Test Field", field2=True)

    assert request.field1 == "Test Field"
    assert request.field2 == True

    data = request.model_dump()
    assert data["field1"] == "Test Field"
    assert data["field2"] == True
