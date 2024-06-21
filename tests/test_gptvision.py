import unittest
from unittest.mock import patch, MagicMock
from similar_recommendation.gptvision import describe_clothes_with_text


class TestGPTVision(unittest.TestCase):

    @patch('similar_recommendation.gptvision.requests.post')
    @patch("builtins.open", new_callable=unittest.mock.mock_open,
           read_data=b"fake_image_data")
    def test_describe_clothes_with_text_success(self, mock_open, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Test description response."
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        description = "A photo of a red shirt."
        response = describe_clothes_with_text("path/to/test/image.jpg", description)

        self.assertEqual(response, "Test description response.")

        mock_post.assert_called_once()
        mock_open.assert_called_once_with("path/to/test/image.jpg", "rb")
