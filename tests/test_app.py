from fastapi.testclient import TestClient
from similar_recommendation.app import app
import pytest
from unittest.mock import patch

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']


def test_submit_quiz():
    quiz_data = {
        "season": "summer",
        "occasion": "casual",
        "color": "blue",
        "style": "sporty"
    }

    response = client.post("/submit-quiz/", data=quiz_data)

    assert response.status_code == 200

    response_json = response.json()

    assert response_json["message"] == "Quiz answers received successfully!"
    assert response_json["season"] == "summer"
    assert response_json["occasion"] == "casual"
    assert response_json["color"] == "blue"
    assert response_json["style"] == "sporty"


@pytest.mark.asyncio
async def test_execute_try_all():
    with patch("subprocess.run") as mock_run:
        response = client.get("/execute_try_all/")
        assert response.status_code == 200
        mock_run.assert_called_once_with(["python", "../try_all.py"], check=True)
