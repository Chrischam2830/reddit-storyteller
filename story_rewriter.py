# story_rewriter.py

from openai import OpenAI

def rewrite_story(title, body, config):
    prompt = f"Rewrite the following Reddit post for a TikTok narration:\n\nTitle: {title}\n\nBody: {body}"
    
    client = OpenAI(api_key=config["openai"]["api_key"])
    
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )
    
    return response.choices[0].message.content.strip()
