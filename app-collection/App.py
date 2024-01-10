#----------Import libraries----------# 
import streamlit as st
import psycopg2
import os
import time as t
import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from vertexai.language_models import CodeChatModel
from vertexai.preview.generative_models import GenerativeModel, Part
import base64
from vertexai.preview.generative_models import GenerativeModel, Part

#----------Database Credentials----------# 
DB_NAME=os.getenv("DB_NAME") 
DB_USER=os.getenv("DB_USER")
DB_HOST= os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_PASSWORD=os.getenv("DB_PASSWORD")
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")
SPECIAL_NAME=os.getenv("SPECIAL_NAME")
#----------Cloud Credentials----------# 
PROJECT_NAME=os.getenv("PROJECT_NAME")
vertexai.init(project=PROJECT_NAME, location="us-central1")

#----------Page Configuration----------# 
st.set_page_config(page_title="Matt Cloud Tech",
                   page_icon=":cloud:" ,
                   layout="wide")

#--------------Title----------------------#
st.write("#### App Collection using Multimodal Model")

#----------Connect to a database----------# 
def connection():
    con = psycopg2.connect(f"""
                           dbname={DB_NAME}
                           user={DB_USER}
                           host={DB_HOST}
                           port={DB_PORT}
                           password={DB_PASSWORD}
                           """)
    cur = con.cursor()
    # Create a table if not exists
    
    # Multimodal
    # cur.execute("DROP TABLE multimodal")
    cur.execute("CREATE TABLE IF NOT EXISTS multimodal(id serial PRIMARY KEY, name varchar, prompt varchar, output varchar, model varchar, time varchar, start_time float, end_time float, image_detail varchar, saved_image_data_base_string varchar, total_input_characters int, total_output_characters int)")
    
    con.commit()
    return con, cur


#----------Models----------#
def models():
    # Chat Capable Model
    mm_model = GenerativeModel("gemini-pro")
    mm_chat = mm_model.start_chat()
    # print(mm_chat.send_message("""Hi. I'm Matt.""", generation_config=mm_config))
    
    return mm_model, mm_chat



def main():
    # Connection
    con = False
    mm_model, mm_chat = models()
    input_name = "Admin"
    column_num = 2
    round_number = 2
    
    try:
        con, cur = connection()
        con = True
    except:
        st.info("##### :computer: ```DATABASE CONNECTION: The app can't connect to the database right now. Please try again later.```")
    if con == True:
        # st.info("Database Connected")
        # Connection
        con, cur = connection()
        
        apps = st.selectbox("Tools", ["Text Only (One-Turn)", "Code Analysis (One-Turn)", "GCP CLI Maker (One-Turn)", "Text Only (Multi-Turn)"])
        
        if apps == "Text Only (One-Turn)":

            info_sample_prompts = """
                You can now start the conversation by prompting in the text bar. :smile: You can ask:
                * List down the things you can do 
                * What is Cloud Computing?
                * What is Google Cloud? Important Google Cloud Services to know
                * Compare Site Reliability Engineering with DevOps
                * Tell me about different cloud services
                * Explain Cloud Computing in simple terms
                """
            st.info(info_sample_prompts)

            col_A, col_B = st.columns(column_num)

            with col_A:

                prompt = st.text_area("Prompt")
                button = st.button("Generate")
                button_stream = st.button("Generate (Stream)")
                refresh = st.button("Refresh")
                # button_multi_turn = st.button("Generate (Multi-Turn)")


            with col_B:
                start = t.time()
                if prompt and button:
                    response = mm_chat.send_message(prompt)
                    # st.write(response.text)
                    st.info("Output in markdown \n")
                    st.markdown(response.text)
                    # st.text(mm_chat.history)
                    end = t.time()
                    st.caption(f"Total Processing Time: {end - start}")
                if prompt and button_stream:
                    response_ = ""
                    response = mm_chat.send_message(prompt, stream=True)
                    st.info("Output streaming... \n")
                    for chunk in response:
                        st.write(chunk.text)
                        response_ = response_ + chunk.text 
                    st.info("Output in markdown \n")
                    st.markdown(response_)
                    end = t.time()
                    st.caption(f"Total Processing Time: {end - start}")
                # if prompt and button_multi_turn:            
                #    pass
                    # st.caption(f"Total Processing Time: {end - start}")
                if refresh:
                    st.rerun()

                # for message in mm_chat.history:
                #    st.markdown(f'**{message.role}**: {message.parts[0].text}')
                
        if apps == "Code Analysis (One-Turn)":

            info_sample_prompts = """
                You can now start the conversation by prompting in the text bar. Enjoy. :smile: You can ask:
                * What is this code about?
                * How to optimize this code?
                """
            st.info(info_sample_prompts)

            col_A, col_B = st.columns(column_num)

            with col_A:
                
                code_text = st.text_area("Code")
                prompt_text = st.text_area("Prompt")
                prompt = f"This is the code: \n\n {code_text} \n\n {prompt_text}"
                button = st.button("Generate")
                button_stream = st.button("Generate (Stream)")
                if button or button_stream:
                    st.info(f"""Total Code and Text Characters: {len(code_text + prompt_text)} 
                            \n Code: {len(code_text)} 
                            \n Text: {len(prompt_text)}
                            """)
                refresh = st.button("Refresh")

            with col_B:
                start = t.time()
                if prompt and button:
                    response = mm_chat.send_message(prompt)
                    st.info("Output in markdown \n")
                    st.markdown(response.text)
                    end = t.time()
                    st.caption(f"Total Processing Time: {end - start}")
                if prompt and button_stream:
                    response_ = ""
                    response = mm_chat.send_message(prompt, stream=True)
                    st.info("Output streaming... \n")
                    for chunk in response:
                        st.write(chunk.text)
                        response_ = response_ + chunk.text 
                    st.info("Output in markdown \n")
                    st.markdown(response_)
                    end = t.time()
                    st.caption(f"Total Processing Time: {end - start}")
                if refresh:
                    st.rerun()
                
        if apps == "GCP CLI Maker (One-Turn)":

            info_sample_prompts = """
                You can now start the conversation by prompting in the text bar. Enjoy. :smile: You can ask:
                * Command line to List down GCP Services
                * Command line to create a bucket
                * Command line to create a compute engine
                """
            st.info(info_sample_prompts)

            col_A, col_B = st.columns(column_num)

            with col_A:

                prompt = st.text_area("Prompt")
                button = st.button("Generate")
                button_stream = st.button("Generate (Stream)")
                refresh = st.button("Refresh")

            with col_B:
                start = t.time()
                if prompt and button:
                    response = mm_chat.send_message(f"Write only the Google Cloud Command Line in code format markdown: {prompt}")
                    st.info("Output in markdown \n")
                    st.markdown(response.text)
                    # st.text(mm_chat.history)
                    end = t.time()
                    #st.caption(f"Total Processing Time: {end - start}")
                if prompt and button_stream:
                    response_ = ""
                    response = mm_chat.send_message(prompt, stream=True)
                    st.info("Output streaming... \n")
                    for chunk in response:
                        st.write(chunk.text)
                        response_ = response_ + chunk.text 
                    st.info("Output in markdown \n")
                    st.markdown(response_)
                    end = t.time()
                    # st.caption(f"Total Processing Time: {end - start}")
                if refresh:
                    st.rerun()

        if apps == "Text Only (Multi-Turn)":
            current_model = "Text Only (Multi-Turn)"
            current_time = t.strftime("Date: %Y-%m-%d | Time: %H:%M:%S UTC")
            prompt_error = "Sorry about that. Please prompt it again, prune the history, or change the model if the issue persists."

            info_sample_prompts = """
                You can now start the conversation by prompting in the text bar. Enjoy. :smile: You can ask:
                * What is Cloud Computing?
                * What is Google Cloud?
                * Important Google Cloud Services to know
                * Compare Site Reliability Engineering with DevOps
                * Tell me about different cloud services
                * Explain Cloud Computing in simple terms
                * Tell me a funny quote related to Cloud Computing
                """
            st.info(info_sample_prompts)

            col_A, col_B = st.columns(column_num)

            with col_A:
                prompt_user = st.text_area("Prompt")
                button = st.button("Generate")
                refresh = st.button("Refresh")
                if refresh:
                    st.rerun()
                prune = st.button(":red[Prune History]")
                if prune:
                    cur.execute("DROP TABLE multimodal")
                    con.commit()
                    st.info("Done")
                    st.rerun()


            with col_B:
                start = t.time()
                if prompt_user and button:
                    prompt_history = ""
                    current_start_time = t.time() 
                    cur.execute(f"""
                            SELECT * 
                            FROM multimodal
                            WHERE name='{input_name}'
                            ORDER BY time ASC
                            """)                    
                    try:
                        for id, name, prompt, output, model, time, start_time, end_time, image_detail, saved_image_data_base_string, total_input_characters, total_output_characters in cur.fetchall():
                            prompt_history = prompt_history + f"\n\n User: {prompt}" + f"\n\n Model: {output}"

                        st.write(prompt_history)

                        if prompt_history == "":
                            response = mm_model.generate_content(prompt_user)
                        elif prompt_history != "":
                            prompt_history = prompt_history + f"\n\n User: {prompt_user}"
                            response = mm_model.generate_content(prompt_history)
                        output = response.text
                    except:
                        output = prompt_error

                    output_characters = len(output)
                    characters = len(prompt_user)
                    end_time = t.time() 
                    SQL = "INSERT INTO multimodal (name, prompt, output, model, time, start_time, end_time, total_input_characters, total_output_characters) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time, characters, output_characters)
                    cur.execute(SQL, data)
                    con.commit() 
                    
                    
                cur.execute(f"""
                SELECT * 
                FROM multimodal
                WHERE name='{input_name}'
                ORDER BY time ASC
                """)
                for id, name, prompt, output, model, time, start_time, end_time, image_detail, saved_image_data_base_string, total_input_characters, total_output_characters in cur.fetchall():
                    message = st.chat_message("user")
                    message.write(f":blue[{name}]") 
                    message.text(f"{prompt}")
                    message.caption(f"{time} | Input Characters: {total_input_characters}")
                    message = st.chat_message("assistant")
                    message.markdown(output)
                    message.caption(f"{time} | Model: {model} | Processing Time: {round(end_time-start_time, round_number)} seconds | Output Characters: {total_output_characters}")
                    
                    
#----------Execution----------#
if __name__ == '__main__':
    main()
    
    #----------Footer----------#
    #----------Sidebar Footer----------#
    with st.sidebar:
        st.markdown("""
                    ---
                    > :gray[:copyright: Portfolio Website by [Matt R.](https://github.com/mregojos)]            
                    > :gray[:cloud: Deployed on [Google Cloud](https://cloud.google.com)]
                    
                    > :gray[For demonstration purposes only, to showcase the latest multimodal model capabilities.]
                    ---
                    """)