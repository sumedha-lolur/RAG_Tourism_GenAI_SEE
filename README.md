# RAG Enhanced Travel Assistant Chatbot

This project is a chatbot that uses OpenAI's GPT-3.5-turbo model to answer user's questions based on multiple contexts. It is enhanced with RAG (Retrieval-Augmented Generation) and integrated with Streamlit for a user-friendly interface.

- For the front-end : `app2.py`
- PDF parsing and indexing : `brain.py`
- API keys are maintained over databutton secret management
- Indexed are stored over session state 

Oversimplified explanation : (**Retrieval**) Fetch the top N similar contexts via similarity search from the indexed PDF files -> concatanate those to the prompt (**Prompt Augumentation**) -> Pass it to the LLM -> which further generates response (**Generation**) like any LLM does. **More in the blog!**

Blog - [here](https://medium.com/@avra42/how-to-build-a-personalized-pdf-chat-bot-with-conversational-memory-965280c160f8)

## Features

- **RAG+OpenAI Integration**: The chatbot can interact and retrieve information from OpenAI.
- **PDF Context**: The chatbot can answer questions based on the context of uploaded PDF files.
- **Recommended Prompts**: The chatbot provides recommended prompts for the user.
- **Custom Queries**: The user can type their own question for the chatbot to answer.

## Setup

1. Clone this repository.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory and add your OpenAI API key as `OPENAI_API_KEY=<Your-API-Key>`.
4. Run the Streamlit app by executing `streamlit run app2.py`.

## Usage

1. Run the Streamlit app.
2. Upload the PDF files you want the chatbot to use as context.
3. Enable the RAG+OpenAI integration if desired.
4. Choose a recommended prompt or type your own question.
5. The chatbot will answer your question based on the context of the uploaded PDF files.

## Note

This project uses the OpenAI API, which is a paid service. Please ensure you have the necessary permissions and credits before using this service.













