import requests
import requests_mock
import pytest

BASE_URL = "http://127.0.0.1:8000/users"


@pytest.fixture
def mock_server():
    with requests_mock.Mocker() as mocker:
        # Mock for invalid credentials (401 Unauthorized)
        mocker.get(
            BASE_URL,
            additional_matcher=lambda request: request.qs == {"username": ["admin"], "password": ["admin"]},
            text="",
            status_code=401,
        )

        # Mock for valid credentials (200 OK)
        mocker.get(
            BASE_URL,
            additional_matcher=lambda request: request.qs == {"username": ["admin"], "password": ["qwerty"]},
            text="",
            status_code=200,
        )

        yield mocker


def test_invalid_user_credentials(mock_server):
    params = {
        "username": "admin",
        "password": "admin",
    }

    # Make GET request with invalid credentials
    response = requests.get(BASE_URL, params=params)

    # Assert that the response is 401 Unauthorized
    assert response.status_code == 401, f"Expected 401 but got {response.status_code}"

    # Assert that the response body is empty
    expected_text = ""  # Empty response expected
    assert response.text.strip() == expected_text, f"Expected '{expected_text}' but got: '{response.text.strip()}'"


def test_valid_user_credentials(mock_server):
    params = {
        "username": "admin",
        "password": "qwerty",
    }

    # Make GET request with valid credentials
    response = requests.get(BASE_URL, params=params)

    # Assert that the response is 200 OK
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    # Assert that the response body is empty
    expected_text = ""  # Empty response expected
    assert response.text.strip() == expected_text, f"Expected '{expected_text}' but got: '{response.text.strip()}'"
