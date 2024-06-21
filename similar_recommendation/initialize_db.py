import io
import os
import sqlite3
import pickle
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import shutil

current_file_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_file_directory)
images_dir = os.path.join(parent_directory, 'images')

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

dataset = load_dataset("wbensvage/clothes_desc", split='train')
model = SentenceTransformer('all-MiniLM-L6-v2')

conn = sqlite3.connect('clothes.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clothes (
    id INTEGER PRIMARY KEY,
    image_path TEXT,
    description TEXT,
    embedding BLOB
    )
''')
conn.commit()

#save images locally
for i, item in enumerate(dataset):
    image_bytes = io.BytesIO()
    item['image'].save(image_bytes, format='JPEG')
    image_path = os.path.join(images_dir, f"{i}.jpg")
    with open(image_path, 'wb') as img_file:
        img_file.write(image_bytes.getvalue())

    description = item['text']
    embedding = model.encode(description)
    embedding_blob = pickle.dumps(embedding)

    cursor.execute('''INSERT INTO clothes (image_path, description, embedding) VALUES (?, ?, ?)''', (image_path, description, embedding_blob))
    conn.commit()

    if i % 100 == 0:
        print(f"Processed {i} items")

conn.close()

clean_images_dir = os.path.join(parent_directory, 'cleaned_images')

if not os.path.exists(clean_images_dir):
    print(f"The directory {clean_images_dir} does not exist.")
else:
    images_dir = os.path.join(parent_directory, 'images')

    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)

    shutil.copytree(clean_images_dir, images_dir, dirs_exist_ok=True)

