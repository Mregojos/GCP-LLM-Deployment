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

sleep = 1

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
    #----------Gemini Pro---------------#
    mm_config = {
        "max_output_tokens": 2048,
        "temperature": 0.2,
        "top_p": 1
    }
    mm_model = GenerativeModel("gemini-pro")
    
    
    return mm_config, mm_model

#----------Execution----------#
if __name__ == '__main__':
    # Connection
    con = False
    try:
        con, cur = connection()
        con = True
    except:
        st.info("##### :computer: ```DATABASE CONNECTION: The app can't connect to the database right now. Please try again later.```")
    if con == True:
        # Connection
        con, cur = connection()
        mm_config, mm_model  = models()
        st.info("DB Connected")
        
        mm_chat = mm_model.start_chat(history=[])
                
        prompt = st.text_area("Prompt")
        button = st.button("Send (Stream)")
        button_ = st.button("Send")
        refresh = st.button("Refresh")
        response_ = ""
        # prompt_sample = "What is Google Cloud in one line?"
        # "In tababular format, list down Google Cloud Services"
        if prompt and button:
            response = mm_chat.send_message(prompt, stream=True)
            for chunk in response:
                st.write(chunk.text)
                t.sleep(sleep)
                # response_ = response_ + chunk.text 
            # st.write(response_)
        if prompt and button_:
            response = mm_chat.send_message(prompt)
            st.write(response.text)
            st.write(mm_chat.history)
        if refresh:
            st.rerun()
        