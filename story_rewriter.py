import openai

def rewrite_story(title, body, config):
    client = openai.OpenAI(
        api_key=config["openai"]["api_key"],
        organization=config["openai"]["organization"]
    )
    prompt = f"Rewrite this Reddit story dramatically for TikTok:\nTitle: {title}\n\n{body}"
    resp = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.8
    )
    return resp.choices[0].message.content.strip()
