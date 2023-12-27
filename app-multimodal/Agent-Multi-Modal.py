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

# Title
st.write("#### Multimodal Model Deployment ")

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
    cur.execute("CREATE TABLE IF NOT EXISTS chats(id serial PRIMARY KEY, name varchar, prompt varchar, output varchar, model varchar, time varchar)")
    # cur.execute("DROP TABLE chats_mmm")
    cur.execute("CREATE TABLE IF NOT EXISTS chats_mmm(id serial PRIMARY KEY, name varchar, prompt varchar, output varchar, model varchar, time varchar, start_time float, end_time float)")
    # cur.execute("DROP TABLE vision_db")
    cur.execute("CREATE TABLE IF NOT EXISTS vision_db(id serial PRIMARY KEY, name varchar, prompt varchar, output varchar, model varchar, time varchar, start_time float, end_time float, saved_image_data_base_string varchar)")
    # cur.execute("DROP TABLE multimodal")
    cur.execute("CREATE TABLE IF NOT EXISTS multimodal(id serial PRIMARY KEY, name varchar, prompt varchar, output varchar, model varchar, time varchar, start_time float, end_time float, image_detail varchar, saved_image_data_base_string varchar, total_characters int, total_output_characters int)")
    # cur.execute("DROP TABLE multimodal_DB")
    cur.execute("CREATE TABLE IF NOT EXISTS multimodal_DB(id serial PRIMARY KEY, name varchar, prompt varchar, output varchar, model varchar, time varchar, start_time float, end_time float, image_detail varchar, saved_image_data_base_string varchar, total_characters int)")
    cur.execute("CREATE TABLE IF NOT EXISTS multimodal_guest_chats(id serial PRIMARY KEY, name varchar, prompt varchar, output varchar, model varchar, time varchar, count_prompt int)")
    cur.execute("CREATE TABLE IF NOT EXISTS guest_chats(id serial PRIMARY KEY, name varchar, prompt varchar, output varchar, model varchar, time varchar, count_prompt int)")
    # cur.execute("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, name varchar, password varchar)")
    # cur.execute("DROP TABLE total_prompts")
    cur.execute("CREATE TABLE IF NOT EXISTS total_prompts(id serial PRIMARY KEY, name varchar, prompt varchar, output varchar, model varchar, time varchar, count_prompt int)")
    cur.execute("CREATE TABLE IF NOT EXISTS chat_view_counter(id serial PRIMARY KEY, view int, time varchar)")
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
    mm_chat = mm_model.start_chat()
    # print(mm_chat.send_message("""Hi. I'm Matt.""", generation_config=mm_config))
    
    #----------Gemini Pro Vision---------------#
    multimodal_model = GenerativeModel("gemini-pro-vision")
    multimodal_generation_config = {
        "max_output_tokens": 2048,
        "temperature": 0.2,
        "top_p": 1,
        "top_k": 32
    }
    
    #----------Vertex AI Chat----------#
    chat_parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 40
    }
    chat_model = ChatModel.from_pretrained("chat-bison")
    chat = chat_model.start_chat(
        context=f"""I am an agent for Matt."""
    )

    #----------Vertex AI Code----------#
    code_parameters = {
        "candidate_count": 1,
        "max_output_tokens": 1024,
        "temperature": 0.2
    }
    code_chat_model = CodeChatModel.from_pretrained("codechat-bison")
    code_chat = code_chat_model.start_chat(
        context=f"""I am an agent for Matt."""
    )
    

    return mm_config, mm_chat, multimodal_model, multimodal_generation_config, chat, chat_parameters, code_chat, code_parameters


#----------- Multimodal, Chat, Multimodal with Database, Vision (One Turn), Vision with DB, Chat with DB --------------#
def multimodal(con, cur):    
    #----------------- Variables ------------------------#
    total_prompt = 0
    button = False
    model = ""
    
    #------------------ Admin --------------------------#
    with st.sidebar:
        if GUEST == False:
            input_name = st.text_input("Name", default_name)

    #------------------ Guest Counter ------------------#
    if GUEST == True:
        input_name = default_name
    LIMIT = 18
    time = t.strftime("Date: %Y-%m-%d | Time: %H:%M:%S UTC")
    time_date = time[0:15]
    cur.execute(f"""
            SELECT SUM(count_prompt)
            FROM multimodal_guest_chats
            WHERE time LIKE '{time_date}%'
            """)
    for total in cur.fetchone():
        if total is None:
            total_count = 0
        else:
            total_count = total
            # st.write(total_count)
    
    #------------------ Info --------------------------#
    if GUEST == False or (GUEST == True and total_count < LIMIT):
        st.info("""
                You can now start the conversation by prompting in the text bar. Enjoy. :smile: You can ask:
                * What is Cloud Computing?
                * What is Google Cloud?
                * Important Google Cloud Services to know
                * Compare Site Reliability Engineering with DevOps
                * Tell me about different cloud services
                * Explain Cloud Computing in simple terms
                * Tell me a funny quote related to Cloud Computing
                """)
    
    #------------------ prompt_info ------------------#
    prompt_history = "You are an intelligent Agent."
    limited_prompt = "For Multimodal Model, chat history (short-term memory) is purposely limited to four prompts only. :red[Prune history] to clear the previous prompts or use other models."
    prompt_prune_info = f"Prompt history by {input_name} is successfully deleted."
    prompt_error = "Sorry about that. Please prompt it again, prune the history, or change the model if the issue persists."

    with st.sidebar:
        #------------------ Prompt starts --------------------------#
        if (GUEST == False) or (GUEST == True and total_count < LIMIT): 
            model = st.selectbox("Choose Model", (["Multimodal", "Chat Only", "Multimodal with DB", "Vision (One Turn)", "Vision (One Turn) with DB", "Chat Only with DB", "Chat Only (Old Version)", "Code (Old Version)"]))
            prompt_user = st.text_area("Prompt")
            uploaded_file = None
            current_image_detail = ""
            image_data_base_string = ""
            current_time = t.strftime("Date: %Y-%m-%d | Time: %H:%M:%S UTC")
            total_prompt_limit = 4
            count_prompt = 1
            round_number = 2
            vision_response = ""
        
        #------------------ Guest limit --------------------------#
        if GUEST == True and total_count >= LIMIT:
            st.info("Guest daily limit has reached!")

        #------------------ Multimodal Chats --------------------------#
        if (GUEST == False) or (GUEST == True and total_count < LIMIT): 
            #-------------------Multi-Modal---------------------#
            if model == "Multimodal":
                image = st.checkbox("Add a photo")
                if image:
                    uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
                    if uploaded_file is not None:
                        image_data = uploaded_file.read()
                        image_name = uploaded_file.name
                        st.image(image_data, image_name)
                        image_data_base = base64.b64encode(image_data)
                        image_data_base_string = base64.b64encode(image_data).decode("utf-8")
                        # image_data_base_string_data = base64.b64decode(image_data_base_string)
                        # st.image(image_data_base_string_data)
                        image = Part.from_data(data=base64.b64decode(image_data_base), mime_type="image/png")
                        responses = multimodal_model.generate_content(["Explain the image in detail", image], generation_config=multimodal_generation_config)
                        current_image_detail = responses.text
                    else:
                        image_data_base_string = ""
                # video = st.checkbox("Add a video")
                # if video:
                #     pass

                cur.execute(f"""
                    SELECT COUNT(*) 
                    FROM multimodal
                    WHERE name='{input_name}'
                    """)
                total_prompt =cur.fetchone()[0]
                if total_prompt <= total_prompt_limit:
                    if total_prompt < total_prompt_limit: 
                        button = True 
                        button = st.button("Send")
                    elif total_prompt >= total_prompt_limit:
                        button = False
                if button:
                    current_start_time = t.time() 
                    current_model = "Multimodal"
                    cur.execute(f"""
                            SELECT * 
                            FROM multimodal
                            WHERE name='{input_name}'
                            ORDER BY time ASC
                            """)
                    try:
                        for id, name, prompt, output, model, time, start_time, end_time, image_detail, saved_image_data_base_string, total_characters, total_output_characters in cur.fetchall():
                            response = mm_chat.send_message(prompt, generation_config=mm_config)
                        if uploaded_file is not None:
                            response = mm_chat.send_message(f"{prompt_user}. I add an image: {current_image_detail}"  , generation_config=mm_config)
                            output = response.text
                            characters = len(prompt_user)
                            output_characters = len(output)
                            end_time = t.time() 
                            ### Insert into a table
                            SQL = "INSERT INTO multimodal (name, prompt, output, model, time, start_time, end_time, saved_image_data_base_string, total_characters, total_output_characters) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time, image_data_base_string, characters, output_characters)
                            cur.execute(SQL, data)
                            con.commit()
                        else:
                            response = mm_chat.send_message(prompt_user, generation_config=mm_config)
                            output = response.text
                            characters = len(prompt_user)
                            output_characters = len(output)
                            end_time = t.time() 
                            ### Insert into a table
                            SQL = "INSERT INTO multimodal (name, prompt, output, model, time, start_time, end_time, saved_image_data_base_string, total_characters, total_output_characters) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time, image_data_base_string, characters, output_characters)
                            cur.execute(SQL, data)
                            con.commit()
                    except Exception as e:
                        # st.write(f"Exception: {e}")
                        output = prompt_error
                        characters = len(prompt_user)
                        output_characters = len(output)
                        end_time = t.time() 
                        ### Insert into a table
                        SQL = "INSERT INTO multimodal (name, prompt, output, model, time, start_time, end_time, saved_image_data_base_string, total_characters, total_output_characters) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time, image_data_base_string, characters, output_characters)
                        cur.execute(SQL, data)
                        con.commit()
                    # Print out expection
                    # except Exception as e:
                    #    with st.sidebar:
                    #        st.write(f"Exception: {e}")
                    #    output = "Sorry about that. Please prompt it again."
                prune = st.button(":red[Prune History]")
                if prune:
                    cur.execute(f"""
                                DELETE  
                                FROM multimodal
                                WHERE name='{input_name}'
                                """)
                    con.commit()
                    st.info(prompt_prune_info)
                    st.rerun()
                    
        
                if total_prompt == total_prompt_limit: 
                    st.info(limited_prompt) 

            #-------------------Chat---------------------#
            if model == "Chat Only":
                button = st.button("Send")
                if button:
                    current_start_time = t.time() 
                    current_model = "Chat Only"
                    cur.execute(f"""
                            SELECT * 
                            FROM chats_mmm
                            WHERE name='{input_name}'
                            ORDER BY time ASC
                            """)
                    try:
                        for id, name, prompt, output, model, time, start_time, end_time in cur.fetchall():
                            response = mm_chat.send_message(prompt, generation_config=mm_config)
                        response = mm_chat.send_message(prompt_user, generation_config=mm_config)
                        output = response.text
                        end_time = t.time()
                        ### Insert into a table
                        SQL = "INSERT INTO chats_mmm (name, prompt, output, model, time, start_time, end_time) VALUES(%s, %s, %s, %s, %s, %s, %s);"
                        data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time)
                        cur.execute(SQL, data)
                        con.commit()
                    except Exception as e:
                        # st.write(f"Exception: {e}")
                        output = prompt_error
                        characters = len(prompt_user)
                        end_time = t.time() 
                        ### Insert into a table
                        SQL = "INSERT INTO chats_mmm (name, prompt, output, model, time, start_time, end_time) VALUES(%s, %s, %s, %s, %s, %s, %s);"
                        data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time)
                        cur.execute(SQL, data)
                        con.commit()
                        

                prune = st.button(":red[Prune History]")
                if prune:
                    cur.execute(f"""
                                DELETE  
                                FROM chats_mmm
                                WHERE name='{input_name}'
                                """)
                    con.commit()
                    st.info(prompt_prune_info)

            #-------------------Multimodal with DB---------------------#
            if model == "Multimodal with DB":
                uploaded_file = None
                current_image_detail = ""
                image_data_base_string = ""
                image = st.checkbox("Add a photo")
                if image:
                    uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
                    if uploaded_file is not None:
                        image_data = uploaded_file.read()
                        image_name = uploaded_file.name
                        st.image(image_data, image_name)
                        image_data_base = base64.b64encode(image_data)
                        image_data_base_string = base64.b64encode(image_data).decode("utf-8")
                        # image_data_base_string_data = base64.b64decode(image_data_base_string)
                        # st.image(image_data_base_string_data)
                        image = Part.from_data(data=base64.b64decode(image_data_base), mime_type="image/png")
                        responses = multimodal_model.generate_content(["Explain the image in detail", image], generation_config=multimodal_generation_config)
                        current_image_detail = responses.text
                    else:
                        image_data_base_string = ""
                # video = st.checkbox("Add a video")
                # if video:
                #     pass

                current_time = t.strftime("Date: %Y-%m-%d | Time: %H:%M:%S UTC")
                button = st.button("Send")
                if button:
                    current_start_time = t.time() 
                    current_model = "Multimodal with DB"
                    cur.execute(f"""
                            SELECT * 
                            FROM multimodal_DB
                            WHERE name='{input_name}'
                            ORDER BY time ASC
                            """)
                    try:
                        for id, name, prompt, output, model, time, start_time, end_time, image_detail, saved_image_data_base_string, total_characters in cur.fetchall():
                            prompt_history = f"""
                                             \n {prompt_history} 
                                             \n ------------
                                             \n Conversion ID: {id}
                                             \n {name}: {prompt} 
                                             \n Model Output: {output}
                                             \n Input Characters: {total_characters}
                                             \n ------------
                                             \n
                                              """
                        response = mm_chat.send_message(prompt_history, generation_config=mm_config)
                        if uploaded_file is not None:
                            response = mm_chat.send_message(f"{prompt_user}. I add an image: {current_image_detail}"  , generation_config=mm_config)
                            output = response.text
                            characters = len(prompt_history)
                            end_time = t.time() 
                            ### Insert into a table
                            SQL = "INSERT INTO multimodal_DB (name, prompt, output, model, time, start_time, end_time, saved_image_data_base_string, total_characters) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time, image_data_base_string, characters)
                            cur.execute(SQL, data)
                            con.commit()
                        else:
                            response = mm_chat.send_message(prompt_user, generation_config=mm_config)
                            output = response.text
                            characters = len(prompt_history)
                            end_time = t.time() 
                            ### Insert into a table
                            SQL = "INSERT INTO multimodal_DB (name, prompt, output, model, time, start_time, end_time, saved_image_data_base_string, total_characters) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time, image_data_base_string, characters)
                            cur.execute(SQL, data)
                            con.commit()
                    except:
                        output = prompt_error
                        characters = len(prompt_history)
                        end_time = t.time() 
                        ### Insert into a table
                        SQL = "INSERT INTO multimodal_DB (name, prompt, output, model, time, start_time, end_time, saved_image_data_base_string, total_characters) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time, image_data_base_string, characters)
                        cur.execute(SQL, data)
                        con.commit()
                    # Print out expection
                    # except Exception as e:
                    #    with st.sidebar:
                    #        st.write(f"Exception: {e}")
                    #    output = "Sorry about that. Please prompt it again."

                prune = st.button(":red[Prune History]")
                if prune:
                    cur.execute(f"""
                                DELETE  
                                FROM multimodal_DB
                                WHERE name='{input_name}'
                                """)
                    con.commit()
                    st.info(prompt_prune_info)

            #-------------------Vision (One Turn)---------------------#
            if model == "Vision (One Turn)":
                if prompt_user == "":
                    prompt_user = "What is the image? Tell me more about the image."   
                image = st.checkbox("Add a photo")
                try:
                    if image:
                        uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
                        if uploaded_file is not None:
                            image_data = uploaded_file.read()
                            image_name = uploaded_file.name
                            st.image(image_data, image_name)
                            image_data_base = base64.b64encode(image_data)
                            image_data_base_string = base64.b64encode(image_data).decode("utf-8")
                            # image_data_base_string_data = base64.b64decode(image_data_base_string)
                            # st.image(image_data_base_string_data)
                            image = Part.from_data(data=base64.b64decode(image_data_base), mime_type="image/png")
                    start_time = t.time() 
                    current_model = "Vision (One Turn)"
                    button = st.button("Send")
                    if button:
                        if uploaded_file is None:
                            st.info("Upload file first")
                        else:
                            responses = multimodal_model.generate_content([prompt_user, image], generation_config=multimodal_generation_config)
                            output = responses.text
                            end_time = t.time()
                except:
                    output = prompt_error
                    end_time = t.time()

            #-------------------Vision with DB--------------------#
            if model == "Vision (One Turn) with DB":
                if prompt_user == "":
                    prompt_user = "What is the image? Tell me more about the image."  
                uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
                if uploaded_file is not None:
                    image_data = uploaded_file.read()
                    image_name = uploaded_file.name
                    st.image(image_data, image_name)
                    image_data_base = base64.b64encode(image_data)
                    image_data_base_string = base64.b64encode(image_data).decode("utf-8")
                    # image_data_base_string_data = base64.b64decode(image_data_base_string)
                    # st.image(image_data_base_string_data)
                    image = Part.from_data(data=base64.b64decode(image_data_base), mime_type="image/png")            
                button = st.button("Send")
                if button:
                    if uploaded_file is None:
                        st.info("Upload file first")
                        current_start_time = t.time() 
                        current_model = "Vision (One Turn) with DB"
                        output = "Upload file first" 
                    else:
                        current_start_time = t.time() 
                        current_model = "Vision (One Turn) with DB"
                        cur.execute(f"""
                                SELECT * 
                                FROM vision_db
                                WHERE name='{input_name}'
                                ORDER BY time ASC
                                """)
                        try: 
                            for id, name, prompt, output, model, time, start_time, end_time, saved_image_data_base_string in cur.fetchall():
                                if saved_image_data_base_string is not None:
                                    image_data_base_string_data = base64.b64decode(saved_image_data_base_string)
                                    image_data_base = base64.b64encode(image_data_base_string_data)
                                    saved_image = Part.from_data(data=base64.b64decode(image_data_base), mime_type="image/png")       
                                    responses = multimodal_model.generate_content([prompt, saved_image], generation_config=multimodal_generation_config)
                                else:
                                    responses = multimodal_model.generate_content(prompt, generation_config=multimodal_generation_config)
                            if uploaded_file is not None:
                                responses = multimodal_model.generate_content([prompt_user, image], generation_config=multimodal_generation_config)
                                end_time = t.time()
                                output = responses.text
                                ### Insert into a table
                                SQL = "INSERT INTO vision_db (name, prompt, output, model, time, start_time, end_time, saved_image_data_base_string) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
                                data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time, image_data_base_string)
                                cur.execute(SQL, data)
                                con.commit()
                            else:
                                responses = multimodal_model.generate_content(prompt_user, generation_config=multimodal_generation_config)
                                end_time = t.time()
                                output = responses.text
                                ### Insert into a table
                                SQL = "INSERT INTO vision_db (name, prompt, output, model, time, start_time, end_time) VALUES(%s, %s, %s, %s, %s, %s, %s);"
                                data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time)
                                cur.execute(SQL, data)
                                con.commit()
                        except:
                                responses = multimodal_model.generate_content(prompt_user, generation_config=multimodal_generation_config)
                                end_time = t.time()
                                output = responses.text
                            
                prune = st.button(":red[Prune History]")
                if prune:
                    cur.execute(f"""
                                DELETE  
                                FROM vision_db
                                WHERE name='{input_name}'
                                """)
                    con.commit()
                    st.info(prompt_prune_info)

            #-------------------Chat Only with DB---------------------#
            if model == "Chat Only with DB":
                button = st.button("Send")
                if button:
                    current_start_time = t.time() 
                    current_model = "Chat with DB"
                    cur.execute(f"""
                            SELECT * 
                            FROM chats_mmm
                            WHERE name='{input_name}'
                            ORDER BY time ASC
                            """)
                    try:
                        for id, name, prompt, output, model, time, start_time, end_time in cur.fetchall():
                            prompt_history = prompt_history + "\n " + f"{name}: {prompt}" + "\n " + f"Model Output: {output}"
                        response = mm_chat.send_message(prompt_history, generation_config=mm_config)
                        response = mm_chat.send_message(prompt_user, generation_config=mm_config)
                        if response != " ":
                            output = response.text
                        elif response == "" or response == None:
                            output = "Oh snap. Could your repeat the prompt?"
                        else:
                            output = "Oh snap. Could your repeat the prompt?"
                        end_time = t.time()

                        ### Insert into a table
                        SQL = "INSERT INTO chats_mmm (name, prompt, output, model, time, start_time, end_time) VALUES(%s, %s, %s, %s, %s, %s, %s);"
                        data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time)
                        cur.execute(SQL, data)
                        con.commit()
                    except:
                        output = prompt_error
                        characters = len(prompt_user)
                        end_time = t.time() 
                        ### Insert into a table
                        SQL = "INSERT INTO chats_mmm (name, prompt, output, model, time, start_time, end_time) VALUES(%s, %s, %s, %s, %s, %s, %s);"
                        data = (input_name, prompt_user, output, current_model, current_time, current_start_time, end_time)
                        cur.execute(SQL, data)
                        con.commit()
                        
                        
                prune = st.button(":red[Prune History]")
                if prune:
                    cur.execute(f"""
                                DELETE  
                                FROM chats_mmm
                                WHERE name='{input_name}'
                                """)
                    con.commit()
                    st.info(prompt_prune_info)

    #-------------------Conversations---------------------#
    #-------------------Multimodal---------------------#
    if model == "Multimodal Model" or model == "Multimodal":
        cur.execute(f"""
        SELECT * 
        FROM multimodal
        WHERE name='{input_name}'
        ORDER BY time ASC
        """)
        for id, name, prompt, output, model, time, start_time, end_time, image_detail, saved_image_data_base_string, total_characters, total_output_characters in cur.fetchall():
            message = st.chat_message("user")
            message.write(f":blue[{name}]") 
            if total_prompt <= 4:
                if saved_image_data_base_string is not "":
                    image_data_base_string_data = base64.b64decode(saved_image_data_base_string)
                    message.image(image_data_base_string_data)
                    message.text(f"{prompt}")
                    message.caption(f"{time} | Input Characters: {total_characters}")
                    message = st.chat_message("assistant")
                    message.markdown(output)
                    message.caption(f"{time} | Model: {model} | Processing Time: {round(end_time-start_time, round_number)} seconds | Output Characters: {total_output_characters}" )                 
                elif saved_image_data_base_string is "":
                    message.text(f"{prompt}")
                    message.caption(f"{time} | Input Characters: {total_characters}")
                    message = st.chat_message("assistant")
                    message.markdown(output)
                    message.caption(f"{time} | Model: {model} | Processing Time: {round(end_time-start_time, round_number)} seconds | Output Characters: {total_output_characters}")

    #-------------------Chat---------------------#
    if model == "Chat Model" or model == "Chat Only":
        cur.execute(f"""
        SELECT * 
        FROM chats_mmm
        WHERE name='{input_name}'
        ORDER BY time ASC
        """)
        for id, name, prompt, output, model, time, start_time, end_time in cur.fetchall():
            message = st.chat_message("user")
            message.write(f":blue[{name}]") 
            message.text(f"{prompt}")
            message.caption(f"{time}")
            message = st.chat_message("assistant")
            message.markdown(output)
            message.caption(f"{time} | Model: {model} | Processing Time: {round(end_time-start_time, round_number)} seconds")

    #-------------------Multi-Modal with DB---------------------#
    if model == "Multimodal with DB":
        cur.execute(f"""
        SELECT * 
        FROM multimodal_DB
        WHERE name='{input_name}'
        ORDER BY time ASC
        """)
        for id, name, prompt, output, model, time, start_time, end_time, image_detail, saved_image_data_base_string, total_characters in cur.fetchall():
            message = st.chat_message("user")
            message.write(f":blue[{name}]") 
            if saved_image_data_base_string is not "":
                image_data_base_string_data = base64.b64decode(saved_image_data_base_string)
                message.image(image_data_base_string_data)
                message.text(f"{prompt}")
                message.caption(f"{time}")
                message = st.chat_message("assistant")
                message.markdown(output)
                message.caption(f"{time} | Model: {model} | Processing Time: {round(end_time-start_time, round_number)} seconds | Input Characters: {total_characters}" )
            else:
                message.text(f"{prompt}")
                message.caption(f"{time}")
                message = st.chat_message("assistant")
                message.markdown(output)
                message.caption(f"{time} | Model: {model} | Processing Time: {round(end_time-start_time, round_number)} seconds | Input Characters: {total_characters}")

    #-------------------Vision---------------------#
    if model == "Vision (One Turn)":
        if uploaded_file is not None and button:
            message = st.chat_message("assistant")
            message.image(image_data)
            message.markdown(output)
            message.caption(f"{current_time} | Model: {current_model} | Processing Time: {round(end_time-start_time, round_number)} seconds")

    #-------------------Vision with DB--------------------#
    if model == "Vision (One Turn) with DB":
        cur.execute(f"""
        SELECT * 
        FROM vision_db
        WHERE name='{input_name}'
        ORDER BY time ASC
        """)
        for id, name, prompt, output, model, time, start_time, end_time, saved_image_data_base_string in cur.fetchall():
            message = st.chat_message("assistant")
            if saved_image_data_base_string is not None:
                image_data_base_string_data = base64.b64decode(saved_image_data_base_string)
                message.image(image_data_base_string_data)
            message.markdown(output)
            message.caption(f"{time} | Model: {model} | Processing Time: {round(end_time-start_time, round_number)} seconds")

    #-------------------Chat with DB---------------------#
    if model == "Chat Only with DB":
        cur.execute(f"""
        SELECT * 
        FROM chats_mmm
        WHERE name='{input_name}'
        ORDER BY time ASC
        """)
        for id, name, prompt, output, model, time, start_time, end_time in cur.fetchall():
            message = st.chat_message("user")
            message.write(f":blue[{name}]") 
            message.text(f"{prompt}")
            message.caption(f"{time}")
            message = st.chat_message("assistant")
            message.markdown(output)
            message.caption(f"{time} | Model: {model} | Processing Time: {round(end_time-start_time, round_number)} seconds")

    #-------------------Old Version---------------------------------#
    #-------------------Chat Only (Old Version)---------------------#
    if model == "Chat Only (Old Version)":
        prompt_user_chat = st.chat_input("What do you want to talk about?")
        with st.sidebar: 
            button = st.button("Send")
            if button or prompt_user_chat:
                if prompt_user_chat:
                    prompt_user = prompt_user_chat
                try:
                    current_model = "Chat Only (Old Version)"
                    cur.execute(f"""
                            SELECT * 
                            FROM chats
                            WHERE name='{input_name}'
                            ORDER BY time ASC
                            """)
                    for id, name, prompt, output, model, time in cur.fetchall():
                        prompt_history = prompt_history + "\n " + f"{name}: {prompt}" + "\n " + f"Model Output: {output}"
                    response = chat.send_message(prompt_history, **chat_parameters)
                    response = chat.send_message(prompt_user, **chat_parameters)
                    if response != " ":
                        output = response.text
                    elif response == "" or response == None:
                        output = prompt_error
                    else:
                        output = prompt_error

                except:
                    output = prompt_error

                ### Insert into a table
                SQL = "INSERT INTO chats (name, prompt, output, model, time) VALUES(%s, %s, %s, %s, %s);"
                data = (input_name, prompt_user, output, current_model, current_time)
                cur.execute(SQL, data)
                con.commit()

            prune = st.button(":red[Prune History]")
            if prune:
                cur.execute(f"""
                            DELETE  
                            FROM chats
                            WHERE name='{input_name}'
                            """)
                con.commit()
                st.info(prompt_prune_info)

    #-------------------Code (Old Version)---------------------#
    if model == "Code (Old Version)":
        prompt_user_chat = st.chat_input("What do you want to talk about?")
        with st.sidebar: 
            button = st.button("Send")
            if button or prompt_user_chat:
                if prompt_user_chat:
                    prompt_user = prompt_user_chat
                try:
                    current_model = "Chat Only (Old Version)"
                    cur.execute(f"""
                            SELECT * 
                            FROM chats
                            WHERE name='{input_name}'
                            ORDER BY time ASC
                            """)
                    for id, name, prompt, output, model, time in cur.fetchall():
                        prompt_history = prompt_history + "\n " + f"{name}: {prompt}" + "\n " + f"Model Output: {output}"
                    response = code_chat.send_message(prompt_history, **chat_parameters)
                    response = code_chat.send_message(prompt_user, **chat_parameters)
                    if response != " ":
                        output = response.text
                    elif response == "" or response == None:
                        output = prompt_error
                    else:
                        output = prompt_error

                except:
                    output = prompt_error

                ### Insert into a table
                SQL = "INSERT INTO chats (name, prompt, output, model, time) VALUES(%s, %s, %s, %s, %s);"
                data = (input_name, prompt_user, output, current_model, current_time)
                cur.execute(SQL, data)
                con.commit()

            prune = st.button(":red[Prune History]")
            if prune:
                cur.execute(f"""
                            DELETE  
                            FROM chats
                            WHERE name='{input_name}'
                            """)
                con.commit()
                st.info(prompt_prune_info)
            
    #-------------------Chat Only and Code (Old Version)---------------------#
    if model == "Chat Only (Old Version)" or model == "Code (Old Version)":
        cur.execute(f"""
        SELECT * 
        FROM chats
        WHERE name='{input_name}'
        ORDER BY time ASC
        """)
        for id, name, prompt, output, model, time in cur.fetchall():
            message = st.chat_message("user")
            message.write(f":blue[{name}]") 
            message.text(f"{prompt}")
            message.caption(f"{time}")
            message = st.chat_message("assistant")
            message.markdown(output)
            message.caption(f"{time} | Model: {model}") 


    #------------------For Multimodal Guest Limits-----------------------#
    if guest_limit == True and button:
        ### Insert into a database
        SQL = "INSERT INTO multimodal_guest_chats (name, prompt, output, model, time, count_prompt) VALUES(%s, %s, %s, %s, %s, %s);"
        data = (input_name, prompt_user, output, model, current_time, count_prompt)
        cur.execute(SQL, data)
        con.commit()
        
    #----------Prune Guest Limits using Admin---------#
    if (GUEST == False):
        with st.sidebar:
            prune_guest_limit = st.button(":red[Prune Guest History Limit]")
            if prune_guest_limit:
                cur.execute(f"""
                            DELETE  
                            FROM multimodal_guest_chats
                            WHERE name='Guest'
                            """)
                con.commit()
                st.info(f"Prompt history by Guest is successfully deleted.")

    #---------------- Insert into a table (total_prompts) ----------------#
    if button:
        SQL = "INSERT INTO total_prompts (name, prompt, output, model, time, count_prompt) VALUES(%s, %s, %s, %s, %s, %s);"
        data = (input_name, prompt_user, output, current_model, current_time, count_prompt)
        cur.execute(SQL, data)
        con.commit()
        

    
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
        mm_config, mm_chat, multimodal_model, multimodal_generation_config, chat, chat_parameters, code_chat, code_parameters  = models()
        with st.sidebar:
            st.header(":computer: Multimodal Agent ",divider="rainbow")
            # st.caption("## Multimodal Chat Agent")
            st.write(f":violet[Your chat will be stored in a database.]")
            st.caption(":warning: :red[Do not add sensitive data.]")
            # st.write("Login or Continue as a guest")
            login = st.checkbox("Login")
            guest = st.checkbox("Continue as a guest")
            # Chat View Counter
            time = t.strftime("Date: %Y-%m-%d | Time: %H:%M:%S UTC")
            view = 1
            SQL = "INSERT INTO chat_view_counter (view, time) VALUES(%s, %s);"
            data = (view, time)
            cur.execute(SQL, data)
            con.commit()
        if login and guest:
            with st.sidebar:
                st.info("Choose only one")
        elif login:
            with st.sidebar:
                password = st.text_input("Password", type="password")
                agent = st.toggle("**:violet[Start the conversation]**")
            if password == ADMIN_PASSWORD and agent:
                default_name = "Admin"
                GUEST = False
                guest_limit = False
                multimodal(con, cur)
                
                # Counter
                with st.sidebar:
                    counter = st.checkbox("Counter")
                    if counter:
                        st.header("Counter")
                        st.caption("""
                                    Count every request in this app.
                                    """)
                        st.subheader("",divider="rainbow")
                        # Total views
                        cur.execute("""
                                    SELECT SUM(view) 
                                    FROM chat_view_counter
                                    """)
                        st.write(f"#### Total views: **{cur.fetchone()[0]}**")
                        # Current view
                        st.write(f"Current: {time}")
                        # Total views today
                        time_date = time[0:15]
                        cur.execute(f"""
                                    SELECT SUM(view) 
                                    FROM chat_view_counter
                                    WHERE time LIKE '{time_date}%'
                                    """)
                        st.write(f"#### Total views today: **{cur.fetchone()[0]}**")
                        st.divider()
                        # Previous views
                        views = st.checkbox("See Previous Views")
                        if views:
                            st.write("**Previous Views**")
                            cur.execute("""
                                        SELECT * 
                                        FROM counter
                                        ORDER BY time DESC
                                        """)
                            for _, _, time in cur.fetchall():
                                st.caption(f"{time}")
                            
            elif password != ADMIN_PASSWORD and agent:
                with st.sidebar:
                    st.info("Wrong Password")

        elif guest:
            default_name = "Guest"
            GUEST = True
            guest_limit = True
            multimodal(con, cur)
        
        elif not login and not guest:
            st.info("Choose login or continue as a guest to get started")
                
        # Close Connection
        cur.close()
        con.close()
        
    #----------Footer----------#
    #----------Sidebar Footer----------#
    with st.sidebar:
        st.markdown("""
                    ---
                    > :gray[:copyright: Portfolio Website by [Matt R.](https://github.com/mregojos)]            
                    > :gray[:cloud: Deployed on [Google Cloud](https://cloud.google.com)]
                    
                    > :gray[This website is for demonstration purposes only.]
                    ---
                    """)

