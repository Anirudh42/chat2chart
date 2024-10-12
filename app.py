import streamlit as st
from io import StringIO, BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    st.title("Simple Chat App with File Upload and Chart")

    # Initialize session state for storing the DataFrame
    if "df" not in st.session_state:
        st.session_state.df = None

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
            st.session_state.df = pd.read_excel(uploaded_file)
            st.dataframe(st.session_state.df)

    # Create Box Plot button
    if st.button("Create Box Plot") and st.session_state.df is not None:
        chart = create_box_plot_with_summary(
            st.session_state.df, "Parental_Involvement", "Exam_Score"
        )
        if isinstance(chart, dict):
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Here's the box plot you requested:",
                    "chart": chart,
                }
            )
        else:
            st.session_state.messages.append(
                {"role": "assistant", "content": f"Error creating chart: {chart}"}
            )

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "chart" in message:
                st.image(message["chart"]["plot"])
                st.write(message["chart"]["summary"], unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("What is your message?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Add assistant response to chat history (you can replace this with actual AI response)
        response = f"Echo: {prompt}"
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Force a rerun to display the new messages immediately
        st.rerun()


def create_box_plot_with_summary(df, category_column, value_column):
    try:
        # Check if required columns exist
        if category_column not in df.columns or value_column not in df.columns:
            missing_columns = [
                col for col in [category_column, value_column] if col not in df.columns
            ]
            return f"Error: Missing required columns: {', '.join(missing_columns)}"

        # Create a box plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x=category_column, y=value_column, data=df, ax=ax)

        # Customize the chart
        plt.title(f"Distribution of {value_column} by {category_column}")
        plt.xlabel(category_column)
        plt.ylabel(value_column)
        plt.xticks(rotation=45, ha="right")

        # Add individual data points
        sns.stripplot(
            x=category_column,
            y=value_column,
            data=df,
            color="black",
            size=4,
            alpha=0.5,
            ax=ax,
        )

        # Adjust layout
        plt.tight_layout()

        # Save the plot to a buffer
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Clear the current figure
        plt.clf()

        # Generate summary statistics
        summary = df.groupby(category_column)[value_column].describe()
        summary_html = summary.to_html()

        return {"plot": buf, "summary": summary_html}

    except Exception as e:
        return f"An error occurred while creating the chart: {str(e)}"


if __name__ == "__main__":
    main()
