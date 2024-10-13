# Chat2Chart

Chat2Chart is a data analysis assistant that allows users to interact with their data through natural language queries. It combines the power of large language models with data manipulation and visualization tools to provide an intuitive interface for data exploration and analysis.

## Features

- Upload Excel (.xlsx, .xls) or CSV files
- Interactive chat interface for data queries
- Automatic data visualization based on user queries
- Pandas-powered data manipulation
- Integration with OpenAI's GPT models for natural language understanding

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/chat2chart.git
   cd chat2chart
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

To run the Chat2Chart application:

```
streamlit run chat2chart/app.py
```

Then, open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

1. Upload your data file (Excel or CSV) using the file uploader.
2. Once the data is loaded, you can start asking questions about your data in natural language.
3. The assistant will analyze your query, perform the necessary data operations, and provide results or visualizations as appropriate.

## Project Structure

- `app.py`: Main Streamlit application file
- `agent.py`: Contains the chat agent and data processing logic
- `pandas_agent.py`: Wrapper for Pandas operations
- `prompt.py`: Defines the system prompt for the AI agent

## How It Works

1. The user uploads a data file, which is read into a Pandas DataFrame.
2. The user enters a natural language query about the data.
3. The query is sent to the AI agent, which interprets the request and generates appropriate Pandas operations.
4. The operations are executed on the DataFrame, and the results are processed.
5. Depending on the nature of the result, the system either returns a text response or generates a visualization.
6. The response is displayed to the user in the chat interface.

## Future Work

## Future Work

As we continue to develop Chat2Chart, we have identified several areas for improvement and expansion:

1. Conversation Memory:
   - Implement a system to remember previous conversations and maintain context throughout a session.
   - Explore techniques to efficiently pass contextual information to the LLM for more coherent and relevant responses.

2. Complex Query Handling:
   - Enhance the AI agent's ability to handle multi-step queries that require generating multiple lines of Python code.
   - Develop a more robust parsing system to break down complex queries into manageable sub-tasks.

3. Feature Expansion:
   - Integrate the ability to publish dashboards directly from the application.
   - Incorporate Streamlit bar charts and other advanced visualization features into the interface.

4. Transition to Next.js:
   - Move from the current Streamlit demo to a more scalable, production-ready platform using Next.js.
   - Leverage Next.js to improve performance, enhance UI/UX, and provide greater flexibility in application architecture.

5. LLM Optimization:
   - Refine the LLM's capability to handle and generate complex, multi-line code queries.
   - Implement techniques to improve the accuracy and relevance of the LLM's responses.

6. Enhanced Data Visualization:
   - Integrate more robust and interactive data visualization tools in the Next.js-based application.
   - Explore advanced charting libraries to provide users with a wider range of visualization options.

7. Additional Data Sources:
   - Expand support for more data file formats (e.g., JSON, XML, SQL databases).
   - Develop capabilities to merge and analyze data from multiple sources simultaneously.

These enhancements aim to transform Chat2Chart into a more powerful, versatile, and user-friendly data analysis assistant, capable of handling a wider range of data sources and complex analytical tasks.


## Acknowledgments

This project was created as part of the [Replit and Cursor Hackathon](https://lablab.ai/event/replit-and-cursor-hackathon).
