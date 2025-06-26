import openai

def rewrite_story(title, body, config):
    openai.api_key = config['openai']['api_key']
    prompt = f"Rewrite the following Reddit post as a dramatic storytelling script for TikTok:\n\nTitle: {title}\n\nPost: {body}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message['content']
