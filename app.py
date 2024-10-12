import streamlit as st
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    st.title("Simple Chat App with File Upload")

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file", type=["txt", "pdf", "docx", "xlsx", "xls"]
    )
    if uploaded_file is not None:
        # Display file details
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": uploaded_file.size,
        }
        st.write(file_details)

        # Read and display file contents (for text files and Excel files)
        if uploaded_file.type == "text/plain":
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            st.text_area("File contents", string_data, height=200)
        elif uploaded_file.type in [
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
        ]:
            df = pd.read_excel(uploaded_file)
            st.dataframe(df)

            if st.button("Create Box Plot"):
                create_box_plot_with_summary(df)

    # Chat interface
    st.subheader("Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is your message?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add assistant response to chat history (you can replace this with actual AI response)
        response = f"Echo: {prompt}"
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)


def create_box_plot_with_summary(df):
    try:
        # Check if required columns exist
        required_columns = ["Parental_Involvement", "Exam_Score"]
        if not all(col in df.columns for col in required_columns):
            missing_columns = [col for col in required_columns if col not in df.columns]
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return

        # Create a box plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x="Parental_Involvement", y="Exam_Score", data=df, ax=ax)

        # Customize the chart
        plt.title("Distribution of Exam Scores by Parental Involvement")
        plt.xlabel("Parental Involvement")
        plt.ylabel("Exam Score")
        plt.xticks(rotation=45, ha="right")

        # Add individual data points
        sns.stripplot(
            x="Parental_Involvement",
            y="Exam_Score",
            data=df,
            color="black",
            size=4,
            alpha=0.5,
            ax=ax,
        )

        # Adjust layout
        plt.tight_layout()

        # Display the chart in Streamlit
        st.pyplot(fig)

        # Display summary statistics
        st.write("Summary Statistics:")
        summary = df.groupby("Parental_Involvement")["Exam_Score"].describe()
        st.write(summary)

    except Exception as e:
        st.error(f"An error occurred while creating the chart: {str(e)}")


if __name__ == "__main__":
    main()
