
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import concurrent.futures
import multiprocessing




def qanda_maker(topic_name, language, level_dropdown):
    # llm = ChatOpenAI(temperature=0.9, request_timeout=300)
    # llm = OpenAI(model_name = "gpt-3.5-turbo")
    llm= OpenAI(model_name = "gpt-3.5-turbo-16k", temperature = 0.9)

    module_prompt = PromptTemplate(
    input_variables=["topic", "language", "level_dropdown"],
    template= ''' You're structuring a MCQ quiz on '{topic}' in language '{language}'. 
                Please provide 20 questions with 3 options in each. 
                Also add correct option at the bottom as well. The difficulty level of the questions varies on the scale of 1-10 with
                1 as least difficult and 10 as most difficut. The difficulty level of the questions must be {level_dropdown}.
                 Give the output in this JSON format with keys as 'question','options' and 'correct_answer'.

                 {{
                "questions": [
                    {{
                    "question": "Which of the following is NOT a common funding source for startups?",
                    "options": [
                        "Venture capital",
                        "Bank loans",
                        "Angel investors"
                    ],
                    "correct_answer": "Bank loans"
                    }},
                    {{
                    "question": "What is the term used to describe the process of obtaining a larger market share than existing competitors?",
                    "options": [
                        "Oligopoly",
                        "Market penetration",
                        "Market segmentation"
                    ],
                    "correct_answer": "Market penetration"
                    }}]

                    }}
                            
                 
                   ''')



    module_chain = LLMChain(llm=llm, prompt=module_prompt)

    module_output = module_chain.predict(topic=topic_name, language = language, level_dropdown = level_dropdown)

    # module_points = module_output.split('\n')
    # print("Modules created:", module_points)

    



    return module_output
