

import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
# from langchain.chat_models import ChatOpenAI
import concurrent.futures
import re
import json
import pandas as pd
from datetime import datetime

from helper_functions.quiz_maker import qanda_maker
from dotenv import load_dotenv
import json
import os
import pickle

# Define custom CSS styles
main_bg_color = "#f8f9fa"
main_text_color = "#1c6dad"
header_bg_color = "#1c6dad"
header_text_color = "#ffffff"
button_bg_color = "#1c6dad"
button_text_color = "#ffffff"

# Apply custom styles
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background-color: {main_bg_color};
        color: {main_text_color};
    }}
    .css-1aumxhk {{
        background-color: {header_bg_color} !important;
    }}
    .css-1aumxhk > h1 {{
        color: {header_text_color};
        text-align: center;
        margin-bottom: 1rem;
    }}
    .stButton button {{
        background-color: {button_bg_color} !important;
        color: {button_text_color} !important;
        margin-top: 1rem;
    }}
    .output {{
        margin-top: 2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)





###################### MAIN APP CODE #####################

def main():
    st.title("Quiz generator")
    
    # Get user input for the API key
    api_key = st.text_input("Enter your API key:")

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("API key set successfully")


    #1
    topic_name = st.text_input("Enter the topic name:")
    #2
    num_question = st.number_input("Enter number of questions you want to generate:", step =1)
    #3
    language = st.text_input("Enter the language in which you want to generate questions")
    #4
    level_options = [1,2,3,4,5,6,7,8,9,10]
    level_dropdown = st.selectbox('Level of questions', level_options)
  


    if st.button("Generate questions"):
        with st.spinner("Generating questions..."):
                

                
                
                final_output = {"questions": []}
                
                for i in range(int(num_question/20)):                    

                    
                    retry = True
                    while retry == True:

                        try:
                    
                            module_output = qanda_maker(topic_name, language, level_dropdown)

                            # with open(f'module_output_{i}.txt', 'w') as file:
                            #     file.write(module_output)

                            # print("AT I :", i)
                            

                            module_output = json.loads(module_output)

                            retry = False  # Break out of the loop if no error occurs
                            break
                        
                        except json.decoder.JSONDecodeError as e:
                            pass
                            
                    
                    # Append the questions from module_output to the final_output
                    final_output["questions"].extend(module_output["questions"])
                                
                                

                # Save the data to a JSON file
                with open('final_output.json', 'w') as file:
                    json.dump(final_output, file, indent=4)


                # Iterate through the questions in the 'questions' list
                for i,question_data in enumerate(final_output['questions']):
                    st.write(f"**Question {i+1} :** {question_data['question']}")
                    st.write(f"**Options:** {', '.join(question_data['options'])}")
                    st.write(f"**Correct Answer:** {question_data['correct_answer']}")
                    st.write("____________________NEXT QUESTION ______________________")

                        
      
        # Create a DataFrame from the final_output JSON
        data = pd.DataFrame(final_output["questions"])
        data['topic_name'] = topic_name
        data['language'] = language
        data['level'] = level_dropdown
        # Add a new column "unique_id" to the data dictionary
        data['unique_id'] = [f"{data['topic_name'][i]}_{data['language'][i]}_{data['level'][i]}_{i + 1}" for i in range(len(data['topic_name']))]
        data['active_flag'] = 1
        data['added_ts'] = pd.to_datetime(datetime.now())
        data['added_by'] = 'udbhav'
        data['last_modified_ts'] =  pd.to_datetime(datetime.now())
        data['last_modified_by'] = 'udbhav'
        data['country'] = 'India'
        data['state'] = 'All'
        
        csv_data = data.to_csv(index=False)

        st.write("Hit download to save the datatset in the CSV format")
        
        with st.empty():            
            st.download_button(label='Download CSV data', data=csv_data, file_name=f'data_{topic_name}_{language}_{level_dropdown}.csv')
        
            
    


if __name__ == "__main__":
    main()


