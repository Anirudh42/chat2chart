from openai import OpenAI
from pandas_agent import PandasAgent
import pandas as pd
import json
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import os
from prompt import PANDAS_AGENT_PROMPT
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def chat_with_dataframe(df_agent, user_message):
    system_prompt = PANDAS_AGENT_PROMPT.format(
        COLUMNS="\n".join(df_agent.get_column_names()),
        DF_DESCRIPTION=df_agent.describe_dataframe().to_string(),
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    last_image_result = None  # Store the last image result
    with st.spinner("Thinking..."):
        for _ in range(4):
            response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages
            )
            response_content = response.choices[0].message.content
            try:
                response_json = json.loads(response_content)
            except json.JSONDecodeError:
                return f"Error: Invalid JSON response from AI: {response_content}"

            messages.append({"role": "assistant", "content": json.dumps(response_json)})
            if "action" in response_json:
                result = df_agent.execute(response_json["action"])
                if isinstance(result, plt.Axes):
                    # Handle matplotlib Axes
                    fig = result.figure
                    img_buffer = BytesIO()
                    fig.savefig(img_buffer, format="png")
                    img_buffer.seek(0)

                    # Encode the image as base64
                    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
                    last_image_result = f"data:image/png;base64,{img_str}"
                    # Clear the figure and close it to free up memory
                    plt.clf()
                    plt.close(fig)
                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {"url": last_image_result},
                                },
                                {"type": "text", "text": "Image generated successfully"},
                            ],
                        }
                    )
                else:
                    messages.append(
                        {"role": "user", "content": f"User feedback: {str(result)}"}
                    )

            elif "final_result" in response_json:
                if response_json["final_result"] == "plot":
                    return {"image": last_image_result}
                else:
                    return response_json["final_result"]
            else:
                return f"Error: Invalid response format from AI: {response_json}"

    return "Maximum iterations reached without a final result."


if __name__ == "__main__":
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    agent = PandasAgent(df)
    print(chat_with_dataframe(agent, "Show me the sum of column A"))
