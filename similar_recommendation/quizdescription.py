from openai import OpenAI
import os

api_key1 = os.environ.get('API_KEY1') #Lidan
api_key2 = os.environ.get('API_KEY2') #Neta
api_key3 = os.environ.get('API_KEY3') #Ran
api_key = api_key2


def generate_prompt2(season, occasion, color, style):
    return f'''Imagine you've recently taken a personal style quiz that inquired about your
    preferred shopping season, the type of occasion you're dressing for, your favorite color,
    and the style you lean towards. Let's say your responses were:
    
    - Season: {season}
    - Occasion: {occasion}
    - Favorite Color: {color}
    - Style Preference: {style}
    
    Describe the clothing, focusing on the shirt, pants, and shoes. Mention the color and any
    distinctive features for each item, using the format "shirt: [description],
    pants: [description],
    shoes: [description]'''


client = OpenAI(
        api_key=api_key,
        organization="org-2CwskBzgGP5OnJE5rJP2GrIS"
    )


def describe_clothes_with_preferences(model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content.strip()
    return text
