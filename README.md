# Registration Assistant Chatbot

This project is a simple registration assistant chatbot that helps users create accounts. It uses LangChain and OllamaLLM to collect the necessary information from the user and organize it in JSON format.

## Features

- Collects information such as name, date of birth, country, phone number and email address from the user.
- Organizes the information in JSON format.
- Provides an interactive chat experience with the user.

## Requirements

The following components must be installed to run this project:
Llama3.1

## Installation
Install the necessary libraries for the project to work:
Langchain langchain-ollama

## Code Description

system_contact: Defines the role of the assistant and specifies the steps required to collect information from the user.
assistant_content: Initial message that the assistant asks the user.
user_content: Communication message that the user will initiate with the assistant.
ChatPromptTemplate: Used to organize the interactions between the user and the assistant.
OllamaLLM: Defines the language model using LangChain.
