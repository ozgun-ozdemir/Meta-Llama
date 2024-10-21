from deep_translator import GoogleTranslator
import speech_recognition as sr
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from gtts import gTTS
import os

# Initialize the recognizer
r = sr.Recognizer()

# Define the chat prompt template in Turkish
template = """ Question: {question} 

Answer: """

prompt = ChatPromptTemplate.from_template(template)

# Initialize the language model
model = OllamaLLM(model="llama3.1")

# Create the chat chain
chain = prompt | model

# Initialize translators
translator_to_en = GoogleTranslator(source='tr', target='en')
translator_to_tr = GoogleTranslator(source='en', target='tr')

def speak(text, lang='tr', speed=1.25):
    tts = gTTS(text=text, lang=lang)
    # Save the audio to a temporary file
    temp_file = "output.mp3"
    tts.save(temp_file)
        # Play the audio file
    try:
        os.system(f"afplay -r {speed} {temp_file}")  # Use "afplay" for macOS
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        os.remove(temp_file)

def chat():
    context = ""
    speak("Merhaba.")
    
    while True:
        try:
            with sr.Microphone() as m:
                r.adjust_for_ambient_noise(m, duration=1)
                print("Dinliyorum...")
                audio = r.listen(m)
                user_input = r.recognize_google(audio, language='tr')  # Recognize Turkish
                print(f"Siz: {user_input}")

                # Check if the user wants to exit
                if user_input.lower() in ("çıkış", "hoşça kal", "bitir", "görüşürüz", "kapat"):
                    speak("Hoşça kal!")
                    break

                # Translate user input to English
                user_input_en = translator_to_en.translate(user_input)

                # Generate the response from the chatbot
                result_en = chain.invoke({"context": context, "question": user_input_en})
                
                # Translate the response to Turkish
                response_tr = translator_to_tr.translate(result_en)
                print(f"{response_tr}")

                # Speak the response
                speak(response_tr, lang='tr')
                
                # Update the context
                context += f"User: {user_input}\nBot: {result_en}\n"

        except sr.UnknownValueError:
            speak("Tekrar deneyin.")
    
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    chat()
