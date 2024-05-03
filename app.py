import streamlit as st
import openai
from brain import get_index_for_pdf
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the title for the Streamlit app
st.title("RAG enhanced Chatbot")

# Cached function to create a vectordb for the provided PDF files
@st.cache_resource
def create_vectordb(files, filenames):
    # Show a spinner while creating the vectordb
    with st.spinner("Vector database"):
        vectordb = get_index_for_pdf(
            [file.getvalue() for file in files], filenames, openai.api_key
        )
    return vectordb

# Define example prompts
example_prompts = [
    "Can you summarize the main points from the 'Introduction' section of the PDF?",
    "What is the conclusion of the document 'Report2023'?",
    "I need a brief explanation of the 'Methods' section in the 'ResearchPaper' PDF.",
]

# Upload PDF files using Streamlit's file uploader
pdf_files = st.file_uploader("", type="pdf", accept_multiple_files=True)

# If PDF files are uploaded, create the vectordb and store it in the session state
if pdf_files:
    pdf_file_names = [file.name for file in pdf_files]
    st.session_state["vectordb"] = create_vectordb(pdf_files, pdf_file_names)
    # Display example prompts for the user to select
    st.subheader("Select an example prompt:")
    selected_prompt_index = st.selectbox("", example_prompts)

    # If a prompt is selected, use it as the actual prompt and update session state
    if selected_prompt_index:
        st.session_state["prompt"] = [{"role": "system", "content": selected_prompt_index}]
        # Add the selected prompt to the conversation
        prompt = st.session_state["prompt"]
        with st.chat_message("system"):
            st.write(selected_prompt_index)
        st.session_state["prompt"] = prompt

# Get the current prompt from the session state or set a default value
prompt = st.session_state.get("prompt", [{"role": "system", "content": "none"}])

# Display previous chat messages
for message in prompt:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Get the user's question using Streamlit's chat input
question = st.chat_input("Ask anything")
# Handle the user's question
if question:
    vectordb = st.session_state.get("vectordb", None)
    if not vectordb:
        with st.message("assistant"):
            st.write("You need to provide a PDF")
            st.stop()

    # Search the vectordb for similar content to the user's question
    search_results = vectordb.similarity_search(question, k=3)
    pdf_extract = "/n ".join([result.page_content for result in search_results])

    # Update the prompt with the pdf extract
    prompt[0] = {
        "role": "system",
        "content": prompt_template.format(pdf_extract=pdf_extract),
    }

    # Add the user's question to the prompt and display it
    prompt.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # Display an empty assistant message while waiting for the response
    with st.chat_message("assistant"):
        botmsg = st.empty()

    # Call ChatGPT with streaming and display the response as it comes
    response = []
    result = ""
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=prompt, stream=True):
        text = chunk.choices[0].get("delta", {}).get("content")
        if text is not None:
            response.append(text)
            result = "".join(response).strip()
            botmsg.write(result)

    if result == "Not applicable.":
        response = []
        result=""
        print(question)
        # Send the prompt directly to OpenAI and get the reply
        for chunk in openai.ChatCompletion.create(
        model="gpt-4", messages=[
                      {
                        "role": "user",
                       "content": f"Answer this from what your trained on and not from my pdf question is {question} and append that 'this message is from openAI and not from pdf you provided' ",
                      }
              ], stream=True):
            text = chunk.choices[0].get("delta", {}).get("content")
            if text is not None:
                response.append(text)
                result = "".join(response).strip()
                botmsg.write(result)

    # Add the assistant's response to the prompt
    prompt.append({"role": "assistant", "content": result})

    # Store the updated prompt in the session state
    st.session_state["prompt"] = prompt
