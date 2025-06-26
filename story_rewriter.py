# story_rewriter.py
from openai import OpenAI

def rewrite_story(title, body, config):
    prompt = (
        f"Rewrite the following Reddit story to be more dramatic, engaging, and concise. "
        f"Include dialogue and suspenseful tone. Keep it under 2 minutes when read aloud.\n\n"
        f"Title: {title}\n\n{body}"
    )

    client = OpenAI(api_key=config["openai"]["api_key"])

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return response.choices[0].message.content.strip()
