from dotenv import load_dotenv
import openai 
from pandas_agent import PandasAgent
import pandas as pd
import json 
import base64
from io import BytesIO
import matplotlib.pyplot as plt

load_dotenv()


df = pd.read_excel("sample_data/StudentPerformanceFactors.xlsx")
agent = PandasAgent(df)

prompt = f"""
You are data analyst who is helping the user analyze their data. You have access to a dataframe called df. The dataframe contains information about students and their performance in exams.
This is the list of columns in the dataframe:
{agent.get_column_names()}. 
This is the description of the dataframe:
{agent.describe_dataframe()}
Before performing the operation, think step by step about what the user is asking and what data is relevant.
Generate response in the json following format: 
{{"thoughts": <thought process>, "action": <pandas dataframe operation>}}
if action is able to be performed, then user will be give you feedback of the result of operation. 
Then use this information to decide using thoughts whether it is better to show this information in a chart or to perform another operation on dataframe or just return the final result 
final result can be in two formats:
{{"final_result": 'string which contains the final result after user feedback'}}
or
{{"final_result": "plot"}}
Sample execution process when user query is suitable for plotting:
1. User asks about distribution of a column
2. {{"thoughts": "User is asking about average score so i will perform groupby operation on dataframe to group data by student name and then perform mean operation on score column", "action": "df.groupby('Student Name').mean()"}}
3. {{"user feedback": "The result shows the average score of students group by their names", "thoughts": "Now i will show this information in a bar chart", "action": "df.plot.bar(x='Student Name', y='Score', title='Average Score of Students')"}}
4. {{"user feedback": "Image generated successfully", "final_result": "plot"}}

Sample execution process when user query is not suitable for plotting:
1. User asks for different values of a column
2. {{"thoughts": "User is asking about different values of score column", "action": "df["score"].value_counts()"}}
3. {{"user feedback": "The result shows the average score of students group by their names", "thoughts":"I can return this information to user in a string format","final_result": "this is the output score low: 12 high: 13"}}
"""


def chat_with_dataframe(user_message):
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": user_message}]

    last_image_result = None  # Store the last image result

    for _ in range(4):
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages 
        )   
        response_json = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(response_json)})
        
        if "action" in response_json:
            result = agent.execute(response_json["action"])
            if isinstance(result, plt.Axes):
                # Handle matplotlib Axes
                fig = result.figure
                img_buffer = BytesIO()
                fig.savefig(img_buffer, format='png')
                img_buffer.seek(0)
                
                # Encode the image as base64
                img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
                last_image_result = f"data:image/png;base64,{img_str}"
                # Clear the figure and close it to free up memory
                plt.clf()
                plt.close(fig)
                messages.append({"role": "user", "content": [{
                                "type": "image_url",
                                "image_url": {
                                    "url": last_image_result
                                }},
                                {"type": "text", "text": "Image generated successfully"}]
                            })
            else:
                messages.append({"role": "user", "content": f"User feedback: {str(result)}"})
        
        elif "final_result" in response_json:
            if response_json["final_result"] == "plot":
                return {"image": last_image_result}
            else:
                return response_json["final_result"]
        else:
            raise ValueError("Invalid response format")
    
    return "Maximum iterations reached without a final result."


if __name__ == "__main__":
    print(chat_with_dataframe("Motivation level counts in numerical form?"))
        

    




