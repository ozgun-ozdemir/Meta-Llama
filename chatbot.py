from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """ Question: {question}

Answer:  """

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.1")

chain = prompt | model

def chatbot():
    context = ""
    print("Ask your question.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "bye", "stop", "finish", "quit"):
            print("Goodbye!")
            break

        result = chain.invoke({"answer": {context}, "question": user_input})
        print(f"Bot: ", {result})
        context += f"User: {user_input}\nBot: {result}\n" 

if __name__ == "__main__":
    chatbot()
