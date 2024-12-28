import streamlit as st
import time
import backend

st.set_page_config(page_title="Nutrition Chatbot", layout="wide")
# Sidebar for API key input
if "api_key_entered" not in st.session_state:
    st.session_state.api_key_entered = False

# Set the expected API key length (e.g., 40 characters for example)
expected_api_key_length = 39

# Automatically handle API key entry and clear the sidebar when entered
if not st.session_state.api_key_entered:
    api_key = st.sidebar.text_input("Enter Google AI Studio API Key", type="password")
    st.sidebar.markdown("[Get an API key](https://aistudio.google.com/apikey)")
    
    # Check if the API key has been entered and is of the correct length
    if api_key:
        if len(api_key) == expected_api_key_length:
            st.session_state.api_key = api_key
            st.session_state.api_key_entered = True
            # Clear the sidebar to simulate collapse after API key entry
            st.sidebar.empty()
        else:
            st.sidebar.error(f"API Key must be {expected_api_key_length} characters long. Please enter a valid key.")
else:
    api_key = st.session_state.api_key

# Streamed response emulator
def response_generator(prompt):
    response = backend.GenerateResponse(prompt, api_key)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("Nutrition ChatBot 🥗")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if not st.session_state.api_key_entered:
    with st.chat_message("assistant"):
        st.markdown("Please enter the API key to start chatting.")
else:

    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # Fetch structured response from the backend
            response = backend.GenerateResponse(prompt, api_key)
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
