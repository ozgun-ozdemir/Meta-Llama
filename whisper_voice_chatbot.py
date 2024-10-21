import whisper
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from gtts import gTTS
import os
import tempfile
import pyaudio
import wave
import numpy as np

# Load the Whisper model
model_whisper = whisper.load_model("large")

# Define the chat prompt template
template = """Question: {question}

Answer:  """

prompt = ChatPromptTemplate.from_template(template)

# Initialize the language model
model = OllamaLLM(model="llama3.1")

# Create the chat chain
chain = prompt | model

def speak(text, speed=1.25):
    tts = gTTS(text=text, lang='en')
    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_file:
        tts.save(temp_file.name)
        # Play the audio file
        try:
            if os.name == 'posix':  # Linux, macOS
                os.system(f"afplay -r {speed} {temp_file.name}")  # macOS
        except Exception as e:
            print(f"Error playing audio: {e}")

def generate_unique_filename(base="record", extension=".wav"):
    i = 1
    while True:
        filename = f"{base}{i}{extension}"
        if not os.path.exists(filename):
            return filename
        i += 1

def record_audio_with_silence_detection(filename, fs=44100, silence_threshold=500, silence_duration=4.0):
    """Record audio and stop when silence is detected."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)

    print("Listening...")
    frames = []
    silent_chunks = 0
    required_silent_chunks = int(fs / 1024 * silence_duration)

    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
            audio_data = np.frombuffer(data, dtype=np.int16)
            # Check if the audio contains sound above the silence threshold
            if np.abs(audio_data).mean() < silence_threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            # Stop recording if silence is detected for enough chunks
            if silent_chunks > required_silent_chunks:
                print("Silence detected, stopping recording...")
                break
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))

def transcribe_audio_with_whisper(audio_path):
    # Use Whisper to transcribe the audio
    result = model_whisper.transcribe(audio_path, language="en", fp16=False)
    return result['text']

def listen_and_transcribe_with_whisper():
    """Listen continuously, save with a unique filename, and transcribe using Whisper."""
    audio_filename = generate_unique_filename()  # Get a unique filename
    record_audio_with_silence_detection(audio_filename)  # Listen and stop when silence is detected
    transcription = transcribe_audio_with_whisper(audio_filename)
    # The file remains saved, no need to delete it now
    return transcription, audio_filename

def chat():
    context = ""
    speak("Ask your question.")

    exit_commands = {"exit", "bye", "stop", "finish", "quit"}
    
    while True:
        try:
            # Listen, save with a unique filename, and transcribe with Whisper
            user_input, audio_filename = listen_and_transcribe_with_whisper()

            if not user_input:
                speak("Please try again.")
                continue

            print(f"You: {user_input} ({audio_filename})")

            # Normalize user input for consistent exit command handling
            normalized_input = user_input.strip().lower()

           # Check if the user wants to exit
            if any(exit_command in normalized_input for exit_command in exit_commands):
                speak("Goodbye!")
                break

            # Generate the response from the chatbot
            result = chain.invoke({"context": context, "question": user_input})
            response = f"Bot: {result}"
            print(response)

            # Speak the response
            speak(result)
            
            # Update the context
            context += f"User: {user_input}\nBot: {result}\n"

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    chat()