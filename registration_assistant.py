import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Define the roles and their initial messages
system_contact = "You are a simple registration assistant that helps users create an account by full name, date of birth, phone number, and e-mail address. Do not ask different questions and accept the given answers."
assistant_content = "To help you create an account, I shall need some information. I will ask you step by step."
user_content = "I want to create an account."

# Define the prompt template to include the role system
template = """System: {system_message}

User: {user_message}

Assistant: {assistant_message}
"""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1")

chain = prompt | model

def save_to_json(data, filename="user_info.json"):
    """Saves the provided data to a JSON file."""
    print("Your registration is completed!")
    # Save the user information to a JSON file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=5)
        

def chatbot():
    context = system_contact
    print("Hello! How can I help you?")
    
    # Initialize information storage
    user_info = {"full_name": None, "dob": None, "phone_number": None, "email_address": None}
    
    # Flag to check if the initial input is to start registration
    registration_started = False

    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ("exit", "bye", "stop", "finish", "quit"):
            print("Goodbye!")
            if any(user_info.values()):  # Save if any information has been collected
                save_to_json(user_info)
            break

        if not registration_started:
            if any(phrase in user_input for phrase in ["create", "sign up", "register", "want", "have an account"]):
                registration_started = True
                # Prepare the input for the model
                response = chain.invoke({
                    "system_message": context,
                    "user_message": user_input,
                    "assistant_message": assistant_content
                })
                # Print the response from the assistant
                assistant_reply = response.strip()
                print(f"Bot: {assistant_reply}")
                context += f"\nUser: {user_input}\nAssistant: {assistant_reply}"
            else:
                print("Please indicate that you want to create an account.")
            continue
        
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
        
        # Process user input to update user_info based on specific responses

        if "full name" in assistant_reply.lower() and user_info["full_name"] is None:
            user_info["full_name"] = user_input

        elif "date of birth" in assistant_reply.lower() and user_info["dob"] is None:
            user_info["dob"] = user_input

        elif "phone number" in assistant_reply.lower() and user_info["phone_number"] is None:
            user_info["phone_number"] = user_input
            
        elif "email address" in assistant_reply.lower() and user_info["email_address"] is None:
            user_info["email_address"] = user_input  
            save_to_json(user_info)  
            break 
        
if __name__ == "__main__":
    chatbot()
