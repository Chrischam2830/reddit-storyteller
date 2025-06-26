# story_rewriter.py
import openai

def rewrite_story(title, body, config):
    prompt = f"Rewrite this Reddit story to be more dramatic and engaging for a TikTok video:\n\nTitle: {title}\n\nStory:\n{body}"
    
    client = openai.OpenAI(api_key=config['openai']['api_key'])

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a dramatic TikTok scriptwriter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    return response.choices[0].message.content.strip()
