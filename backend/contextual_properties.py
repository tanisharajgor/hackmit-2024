import requests

MODEL_ID = "8w6yyp2q"
BASETEN_API_KEY = "YMKFudUr.FcjOTi13DlaR3ZtCbBIumoXeqFJy25yx"

def get_part_of_speech(word):
    messages = [
        {"role": "system", "content": "You are a dictionary for different languages."},
        {"role": "user", "content": f"Give me just the part of speech of {word}. No greeting."},
    ]

    return request_response(messages)

def get_usages(word):
    messages = [
        {"role": "system", "content": "You are a dictionary for different languages."},
        {"role": "user", "content": f"Give me just 3 simple ways to use the literal definition of {word} in a sentence. Return only the sentences as bullet points, without any additional text or introduction."},
    ]

    return request_response(messages)

def request_response(messages):
    payload = {
        "messages": messages,
        "stream": False,
        "max_tokens": 2048,
        "temperature": 0.9
    }

    # Call model endpoint
    res = requests.post(
        f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
        json=payload,
        stream=False
    )
    
    # Extract and format the response
    return format_response(res.text)

def format_response(response_text):
    # Remove surrounding quotes if present
    if response_text.startswith('"') and response_text.endswith('"'):
        response_text = response_text[1:-1]
    return response_text