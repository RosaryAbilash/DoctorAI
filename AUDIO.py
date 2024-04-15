from gtts import gTTS
import os

def play_audio(text):
    # tts = gTTS(text=text, lang='ta')
    # tts.save("output.mp3")
    os.system("output.mp3")  # or any other audio player command

welcome_message = "வரவேற்கின்றோம் டாக்டர் எய் ஐ மருத்துவ அமைப்பின் படிமமாக. நாம் உங்களுக்கு வழங்கும் தனிப்பட்ட மருத்துவ உதவியாளர்களாக இருக்கிறோம். எங்கள் சேவைகளை ஆராய்க்க மற்றும் உங்கள் டயாக்னோசிஸ் பயணத்தை தொடங்க சுதந்திரமாக உள்ளிடவும்."

play_audio(welcome_message)
