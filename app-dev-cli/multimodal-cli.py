# sh multimodal-cli.sh
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
    
def start_chat(prompt):
    start = t.time()
    response = mm_chat.send_message(prompt)
    print(response.text)
    end = t.time()
    # print(f"Total Processing Time: {end - start}")

print("\n")
print("-----------Chat Starts here-------------")
stream = input("Stream Output? (Yes/Y or No/N):  ")
stop = "No"
while stop == "No" or stop =="N":
    # prompt = args.prompt
    print("\n \n")
    prompt = input("Prompt:  ")   
    
    print("\n \n")
    if stream == "Yes" or stream == "Y":
        start_chat_stream(prompt)
    elif stream == "No" or stream == "N":
        start_chat(prompt)
    
    print("\n \n")
    # Chat History
    # print(mm_chat.history)
    # print("\n \n")
    
    stop = input("End the conversation? (Yes/Y or No/N):  ")
    print("\n \n")
    
    print("------------------------")