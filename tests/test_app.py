import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activity_state():
    # Arrange
    original_activities = copy.deepcopy(app_module.activities)

    yield

    # Cleanup
    app_module.activities.clear()
    app_module.activities.update(original_activities)


def test_get_activities():
    # Arrange
    # No special setup needed for this API call.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data


def test_signup_for_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_duplicate_signup_returns_error():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "remove.student@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
