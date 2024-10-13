import streamlit as st
from io import StringIO, BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_agent import PandasAgent
from agent import chat_with_dataframe
import base64


def main():
    st.title("Chat2Chart: Data Analysis Assistant")

    # Initialize session state
    if "df" not in st.session_state:
        st.session_state.df = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pandas_agent" not in st.session_state:
        st.session_state.pandas_agent = None

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls", "csv"])
    if uploaded_file is not None:
        # Display file details
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": uploaded_file.size,
        }
        st.write(file_details)

        # Read and display file contents
        if uploaded_file.type in [
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
        ]:
            st.session_state.df = pd.read_excel(uploaded_file)
        elif uploaded_file.type == "text/csv":
            st.session_state.df = pd.read_csv(uploaded_file)
        
        if st.session_state.df is not None:
            st.dataframe(st.session_state.df)
            st.session_state.pandas_agent = PandasAgent(st.session_state.df)
            st.success("Data loaded successfully! You can now chat with your data.")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], dict) and "image" in message["content"]:
                st.image(message["content"]["image"])
            else:
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about your data"):
        if st.session_state.pandas_agent is None:
            st.error("Please upload a file first.")
        else:
            # Add user message to chat history
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Get response from chat_with_dataframe
            response = chat_with_dataframe(prompt)
            with st.chat_message("assistant"):
                if isinstance(response,dict) and "image" in response:
                    st.image(response["image"])
                else:
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
