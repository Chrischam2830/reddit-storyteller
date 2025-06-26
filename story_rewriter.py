# story_rewriter.py
from openai import OpenAI

def rewrite_story(title, body, config):
    client = OpenAI(api_key=config["openai"]["api_key"])
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user", "content": f"{title}\n\n{body}"}],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()
