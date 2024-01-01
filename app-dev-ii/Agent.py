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
st.write("#### Multimodal Model Deployment")

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


#----------Execution----------#
if __name__ == '__main__':
    # Connection
    con = False
    mm_model, mm_chat = models()

    try:
        con, cur = connection()
        con = True
    except:
        st.info("##### :computer: ```DATABASE CONNECTION: The app can't connect to the database right now. Please try again later.```")
    if con == True:
        st.info("Database Connected")
        # Connection
        con, cur = connection()
        
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
        
        prompt = st.text_area("Prompt")
        button = st.button("Generate")
        button_stream = st.button("Generate (Stream)")
        # button_multi_turn = st.button("Generate (Multi-Turn)")
        refresh = st.button("Refresh")
        
        start = t.time()
        if prompt and button:
            response = mm_chat.send_message(prompt)
            # st.write(response.text)
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