import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import pickle
from similar_recommendation.main_recommendation import process_find_and_display


class TestMainRecommendation(unittest.TestCase):

    @patch('similar_recommendation.main_recommendation.sqlite3.connect')
    @patch('similar_recommendation.main_recommendation.SentenceTransformer')
    def test_process_find_and_display(self, mock_sentence_transformer, mock_connect):
        mock_model = MagicMock()
        mock_sentence_transformer.return_value = mock_model
        mock_model.encode.return_value = np.array([[0.5]])

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        item_id = 1
        item_desc = "Test shirt description"
        item_embedding = pickle.dumps(np.array([0.5]))
        mock_cursor.fetchall.return_value = [(item_id, item_desc, item_embedding)]

        with patch('similar_recommendation.main_recommendation.cosine_similarity', return_value=np.array([[0.99]])):
            description = "Shirt: A description of a shirt."
            top_items = process_find_and_display(description, "Shirt", mock_model, db_path=":memory:", images_folder='images')

            self.assertEqual(len(top_items), 1)
            self.assertEqual(top_items[0]['id'], item_id)
            self.assertEqual(top_items[0]['description'], item_desc)
            self.assertAlmostEqual(top_items[0]['similarity'], 0.99)

            mock_model.encode.assert_called_once_with([description.split(": ")[1]])
            mock_connect.assert_called_once_with(":memory:")
            mock_cursor.execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()
