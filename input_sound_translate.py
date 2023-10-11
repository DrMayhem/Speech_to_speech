from playsound import playsound 
import speech_recognition as sr 
from googletrans import Translator 
from gtts import gTTS 
import os 
import pygame

# A dictionary containing language names and their codes
language_codes = {
    'english': 'en',
    'hindi': 'hi',
    'tamil': 'ta',
    'telugu': 'te',
}

# Capture Voice 
# takes command through microphone 
def take_command(): 
    r = sr.Recognizer() 
    with sr.Microphone() as source: 
        print("Say something:")
        audio = r.listen(source) 

    try: 
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in') 
        print(f"The User said: {query}\n") 
    except Exception as e: 
        print("Speech Recognition could not understand the audio")
        return "None"
    return query 

# Input from user 
# Make input to lowercase 
query = take_command() 
while query == "None": 
    query = take_command() 

# Input destination language
print("Say the language in which you want to convert:")
to_lang = take_command()
while to_lang == "None":
    to_lang = take_command()

# Extract only the language name
to_lang = to_lang.split()[0].lower()

# Check if the destination language is available
to_lang_code = language_codes.get(to_lang)
if not to_lang_code:
    print("Language not available for translation.")
else:
    # Translate using googletrans
    translator = Translator()
    translated_text = translator.translate(query, dest=to_lang_code).text

    # Print translated text
    print(f"Translated text to {to_lang_code}: {translated_text.encode('utf-8', 'ignore').decode('ascii', 'ignore')}")

    # Translating from source to destination using gTTS
    tts = gTTS(text=translated_text, lang=to_lang_code, slow=False)
    tts.save("translated_audio.mp3")

    # Using pygame to play the audio
    pygame.mixer.init()
    pygame.mixer.music.load("translated_audio.mp3")
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Close the pygame mixer
    pygame.mixer.quit()

    # Remove the temporary audio file
    os.remove("translated_audio.mp3")

    # Provide information about playing the audio
    print("Audio played locally.")