from gtts import gTTS

def generate_voiceover(text, config=None, output_path="voiceover.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(output_path)
    return output_path
