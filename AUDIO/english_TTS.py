from gtts import gTTS

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    return tts

def save_to_mp3(tts, filename):
    tts.save(filename)

if __name__ == "__main__":
    english_text = "After selecting your symptom, choose its severity: Mild, Moderate, or Severe."
    mp3_filename = "ENG_SEV_1.mp3"
    tts = text_to_speech(english_text)
    save_to_mp3(tts, mp3_filename)
    print("English text converted to MP3 successfully!")
