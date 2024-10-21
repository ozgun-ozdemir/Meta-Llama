from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Define the roles and their initial messages
system_contact = "You are a simple registration assistant that helps users create an account. First, ask how you can assist them. For creating an account, you need to collect full name, date of birth, country, phone number, and e-mail address. Then make a JSON format with this information."
assistant_content = "How can I help you today? To create an account, I'll need to gather some information from you step by step."
user_content = "I want to create an account."

# Define the prompt template to include the role system
template = """System: {system_message}

User: {user_message}

Assistant: {assistant_message}
"""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1")

chain = prompt | model

def chatbot():
    context = system_contact
    print("Hello!")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "bye", "stop", "finish", "quit"):
            print("Goodbye!")
        
        # Prepare the input for the model
        response = chain.invoke({
            "system_message": context,
            "user_message": user_input,
            "assistant_message": assistant_content
        })
        
        # Print the response from the assistant
        assistant_reply = response.strip()
        print(f"Bot: {assistant_reply}")

        # Update the context with the new conversation
        context += f"\nUser: {user_input}\nAssistant: {assistant_reply}"

if __name__ == "__main__":
    chatbot()
