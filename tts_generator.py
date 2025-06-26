import requests

def generate_voiceover(script_text, config):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{config['elevenlabs']['voice_id']}"
    headers = {
        "xi-api-key": config['elevenlabs']['api_key'],
        "Content-Type": "application/json"
    }
    data = {
        "text": script_text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception("Voiceover generation failed.")
    audio_path = "voiceover.mp3"
    with open(audio_path, "wb") as f:
        f.write(response.content)
    return audio_path
