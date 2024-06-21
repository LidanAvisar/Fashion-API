import os
import pickle
import sqlite3
import re
import numpy as np
from sentence_transformers import SentenceTransformer

current_file_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.dirname(current_file_directory)
images_directory = os.path.join(project_directory, 'images')
model = SentenceTransformer('all-MiniLM-L6-v2')

prompt1 = '''Describe the clothing in the image, focusing on the shirt, pants, and shoes.
            Mention the color and any distinctive features for each item, using the format 
            "shirt: [description], pants: [description], shoes: [description]."'''

#for testing locally
#description = '''Shirt: The person is wearing a black shirt.
#Pants: They are wearing light blue, high-waisted jeans with a slightly distressed hem at the ankles.
#Shoes: The shoes are white sneakers with a simple, classic design. '''
#print(description)

# Function to process, find, and display similar items for a clothing item
clothes_db_path = "./clothes.db"


def process_find_and_display(description, item_type, model, db_path=clothes_db_path, images_folder='images'):
    item_match = re.search(rf"{item_type}\s*:\s*(.+?)\s*(?:\n|$)", description, re.DOTALL | re.IGNORECASE)
    item_desc = item_match.group(1).strip() if item_match else None

    if item_desc:
        item_vector = model.encode([item_desc])[0]

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, description, embedding FROM clothes")
        items = cursor.fetchall()

        similarities = []
        for item in items:
            item_id, item_desc, item_embedding = item
            item_vector_db = pickle.loads(item_embedding)
            similarity = cosine_similarity([item_vector], [item_vector_db])[0][0]
            similarities.append((item_id, item_desc, similarity))

        similarities.sort(key=lambda x: x[2], reverse=True)
        top_similar_items = similarities[:3]

        top_items_data = []
        for item in top_similar_items:
            image_file_path = os.path.join(images_directory, f"{int(item[0]) - 1}.jpg")
            item_data = {
                'id': item[0],
                'description': item[1],
                'similarity': item[2],
                'image_path': image_file_path
            }
            top_items_data.append(item_data)

        return top_items_data
    else:
        print(f"\nNo {item_type} description found in the input.")
        return []


def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    dot_product = np.dot(v1, v2.T)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)
