from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Define the roles and their initial messages
roles = ['system', ' assistant', "user"]
system_contant = "You are an assistant that speaks like Shakespeare."
assistant_contant = "Why did the chicken cross the road? To get to the other side, but verily, the other side was full of peril and danger, so it quickly returned from whence it came, forsooth!'"
user_contant = "Tell me a joke"

# Define the prompt template to include the role system
template = """System: {system_message}

User: {user_message}

Assistant: {assistant_message}
"""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1")

chain = prompt | model

def chatbot():
    context = system_contant
    print("Ask your question or type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "bye", "stop", "finish", "quit"):
            print("Goodbye!")
            break
        
        # Prepare the input for the model
        message = chain.invoke({
            "system_message": context,
            "user_message": user_input,
            "assistant_message": assistant_contant
        })
        
        # Print the response from the assistant
        assistant_reply = message.strip()  
        print(f"Bot: {assistant_reply}")
        
        # Update the context with the new conversation
        context += f"\nUser: {user_input}\nAssistant: {assistant_reply}"
    
if __name__ == "__main__":
    chatbot()
