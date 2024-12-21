import streamlit as st
import requests

# Streamlit UI layout
st.title("Peachy Chatbot")
st.markdown("Welcome to Peachy, your friendly chatbot! Ask me anything.")

# Input box for user query
user_input = st.text_input("Enter your question here:")

# Button to submit query
if st.button("Ask"):
    if user_input:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask", json={"prompt": user_input}
            )
            if response.status_code == 200:
                response_data = response.json()
                st.success(f"Peachy says: {response_data['response']}")
            else:
                st.error("Error: Failed to get response from server.")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")

# Display introductory message
st.subheader("Introduction")
st.markdown(
    "Peachy is here to assist you with your questions. Feel free to ask anything!"
)
