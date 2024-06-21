from fastapi.responses import FileResponse
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import uvicorn
import shutil

import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)
images_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "images")

from gptvision import describe_clothes_with_text
from main_recommendation import process_find_and_display, model, prompt1
from quizdescription import generate_prompt2,describe_clothes_with_preferences
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import subprocess


app = FastAPI()
global_quiz_started = 0
latest_quiz_answers = {}
app.mount("/images", StaticFiles(directory=images_directory), name="images")

#MY FIRST DEPLOYMENT
@app.get("/")
async def main():
    html_file_path = os.path.join(os.path.dirname(__file__), 'upload_form.html')
    with open(html_file_path, 'r') as html_file:
        content = html_file.read()
    return HTMLResponse(content=content)


@app.get("/quiz")
async def get_quiz():
    global global_quiz_started
    global_quiz_started = 1
    html_file_path2 = os.path.join(os.path.dirname(__file__), 'quiz.html')
    with open(html_file_path2, 'r') as html_file:
        content = html_file.read()
    return HTMLResponse(content=content)


@app.post("/submit-quiz/")
async def submit_quiz(season: str = Form(...), occasion: str = Form(...), color: str = Form(...),
                      style: str = Form(...)):
    global latest_quiz_answers
    latest_quiz_answers = {
        "season": season,
        "occasion": occasion,
        "color": color,
        "style": style
    }

    return {"message": "Quiz answers received successfully!", "season": season, "occasion": occasion, "color": color,
            "style": style}


@app.post("/uploadfile/", response_class=HTMLResponse)
async def create_upload_file(file: UploadFile = File(...)):
    global global_quiz_started
    global global_quiz_started, latest_quiz_answers
    try:

        # Clear the recommendation directories before new use, ensuring they exist
        clear_directory(os.path.join(current_dir, 'Shirts_recommendation'))
        clear_directory(os.path.join(current_dir, 'Pants_recommendation'))
        clear_directory(os.path.join(current_dir, 'Shoes_recommendation'))
        clear_directory(os.path.join(current_dir, '.temp'))


        temp_dir = os.path.join(current_dir, '.temp')
        os.makedirs(temp_dir, exist_ok=True)  # Ensure the temp directory exists
        temp_image_path = os.path.join(temp_dir, "temp_image.jpg")
        with open(temp_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Choose the prompt based on the global flag
        if global_quiz_started == 1 and latest_quiz_answers:
            prompt2 = generate_prompt2(**latest_quiz_answers)
            description = describe_clothes_with_preferences(model="gpt-3.5-turbo", prompt=prompt2)
            global_quiz_started = 0  # Reset the quiz started flag
        else:
            description = describe_clothes_with_text(temp_image_path, prompt1)

        if not description:
            raise Exception("Failed to generate description for the image.")

        results_html = f"<div><h2>Description</h2><p>{description}</p></div>"

        # Process, find, and display similar items for each clothing type
        for item_type in ["Shirt", "Pants", "Shoes"]:
            similar_items = process_find_and_display(description, item_type, model)
            results_html += f"<div><h3>Similar {item_type}</h3><ul>"
            for item in similar_items:
                image_basename = os.path.basename(item['image_path'])
                web_image_url = f"/images/{image_basename}"

                if item_type == "Shirt":
                    target_directory = os.path.join(current_dir, 'Shirts_recommendation')
                elif item_type == "Pants":
                    target_directory = os.path.join(current_dir, 'Pants_recommendation')
                elif item_type == "Shoes":
                    target_directory = os.path.join(current_dir, 'Shoes_recommendation')
                else:
                    continue

                os.makedirs(target_directory, exist_ok=True)
                source_path = os.path.join(images_directory, image_basename)
                target_path = os.path.join(target_directory, image_basename)
                shutil.copy(source_path, target_path)

                results_html += f"""
                <div>
                    <p>Item ID: {item['id']}</p>
                    <p>Description: {item['description']}</p>
                    <p>Similarity: {item['similarity']}</p>
                    <img src='{web_image_url}' alt='Similar Item' style='width: 200px; height: auto;'>
                </div>
                """

        template_file_path = os.path.join(os.path.dirname(__file__), 'results_page.html')
        with open(template_file_path, 'r') as template_file:
            content = template_file.read()

        content = content.replace("<!-- Placeholder for dynamic content -->", results_html)
        return HTMLResponse(content=content)
    except Exception as e:
        error_message = str(e)
        return HTMLResponse(f"<html><body><h2>Error: {error_message}</h2><a href='/'>Try again</a></body></html>", status_code=500)


@app.get("/execute_try_all/")
async def execute_try_all():
    try:
        subprocess.run(["python", "../try_all.py"], check=True)
        return {"message": "video executed successfully, now you can download it !"}
    except subprocess.CalledProcessError:
        return "Please refresh the page and try again."


@app.get("/download_video/")
async def download_video():
    video_path = os.path.join(current_dir, "", "output_video.mp4")
    if os.path.exists(video_path):
        return FileResponse(path=video_path, filename="output_video.mp4")
    else:
        raise HTTPException(status_code=404, detail="Video not found")


def clear_directory(directory_path):
    """Removes all files in the specified directory and ensures the directory exists."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        return

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)