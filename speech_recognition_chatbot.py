import speech_recognition as sr
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Initialize the recognizer
r = sr.Recognizer()

# Define the chat prompt template
template = """ Question: {question} 

Answer: """

prompt = ChatPromptTemplate.from_template(template)

# Initialize the language model
model = OllamaLLM(model="llama3.1")

# Create the chat chain
chain = prompt | model

def chat():
    context = ""
    print("Ask your question.")
    
    while True:
        try:
            with sr.Microphone() as m:
                r.adjust_for_ambient_noise(m, duration=1)
                print("Listening...")
                audio = r.listen(m)
                user_input = r.recognize_google(audio)
                print(f"You: {user_input}")

                # Check if the user wants to exit
                if user_input in ("exit", "bye", "stop", "finish", "quit"):
                    print("Goodbye!")
                    break

                # Generate the response from the chatbot
                result = chain.invoke({"context": context, "question": user_input})
                response = f"Bot: {result}"
                print(response)

                # Update the context
                context += f"User: {user_input}\nBot: {result}\n"

        except sr.UnknownValueError:
            print("Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    chat()
