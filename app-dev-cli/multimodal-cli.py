# py multimodal-cli.py

import argparse
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import time as t

#------------- For flags --------------------#
# parser = argparse.ArgumentParser()
# parser.add_argument("--prompt", help="Prompt")
# parser.add_argument("--range", help="Range")

# args = parser.parse_args()

# print(args.prompt)
# print(args.range)

#-------------- Chat Model -------------------#
mm_model = GenerativeModel("gemini-pro")
mm_chat = mm_model.start_chat()


def start_chat_stream(prompt):
    start = t.time()
    response_ = ""
    response = mm_chat.send_message(prompt, stream=True)
    for chunk in response:
        print(chunk.text)
        response_ = response_ + chunk.text 
    print(response_)
    end = t.time()
    # print(f"Total Processing Time: {end - start}")
    return response
    
def start_chat(prompt):
    start = t.time()
    response = mm_chat.send_message(prompt)
    print(response.text)
    end = t.time()
    # print(f"Total Processing Time: {end - start}")
    return response

print("\n")
print("-----------Configuration Setup-------------")
stream = input("Stream Output? (Yes/Y or No/N/Enter):  ")
if stream == "":
    stream = "No"
output = input("Save Output? (Yes/Y or No/N/Enter):  ")
if output == "":
    output = "No"
if output == "Yes" or output == "Y":
    print("\n")
    print("Conversation will be saved as output.md")
    
print("\n")
print("-----------Chat Starts here-------------")
stop = "No"
while stop == "No" or stop =="N":
    # prompt = args.prompt
    print("\n \n")
    prompt = input("Prompt:  ")   
    
    print("\n \n")
    print("Output: \n")
    if stream == "Yes" or stream == "Y":
        response = start_chat_stream(prompt)
    elif stream == "No" or stream == "N":
        response = start_chat(prompt)
    
    print("\n \n")
    # Chat History
    # print(mm_chat.history)
    # print("\n \n")
    
    # Save output
    if output == "Yes" or output == "Y":
        with open("output.md", "w") as file:
            file.write(f"""**Prompt**: {prompt}
                        \n **Output**:
                        \n {response.text}
                        \n
                        \n ---------------------
                        """)
    
    # End the conversation
    stop = input("End the conversation? (Yes/Y or No/N/Enter):  ")
    print("\n \n")
    if stop == "":
        stop = "No"
       
    print("------------------------")
    if stop == "Yes" or stop ==  "Y":
        print("Chat Logout")
        
