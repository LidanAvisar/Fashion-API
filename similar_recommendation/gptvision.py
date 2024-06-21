import base64
import requests
import os

api_key1 = os.environ.get('API_KEY1') #Lidan
api_key2 = os.environ.get('API_KEY2') #Neta
api_key3 = os.environ.get('API_KEY3') #Ran
api_key = api_key2


def describe_clothes_with_text(image_path, prompt_text):

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
          return base64.b64encode(image_file.read()).decode("utf-8")

    base64_image = encode_image(image_path)

    # Set headers and payload for the API request
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt_text
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    # Make the API request
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Process the response
    if response.status_code == 200:
      response_data = response.json()
      chat_responses = response_data.get("choices", [])[0].get("message", {}).get("content", "")
      return chat_responses
    else:
      return f"Failed to get a response, status code: {response.status_code}"
