# -*- coding: utf-8 -*-

from gtts import gTTS

def text_to_speech(text, lang='ta'):  # Setting the language code for Tamil ('ta')
    tts = gTTS(text=text, lang=lang)
    return tts

def save_to_mp3(tts, filename):
    tts.save(filename)

if __name__ == "__main__":
    tamil_text = "உங்கள் அறிகுறியைத் தேர்ந்தெடுத்த பிறகு, அதன் தீவிரத்தை தேர்வு செய்யவும்: லேசான, மிதமான அல்லது கடுமையான."
    mp3_filename = "TAM_SEV_1.mp3"
    tts = text_to_speech(tamil_text)
    save_to_mp3(tts, mp3_filename)
    print("Tamil text converted to MP3 successfully!")


