# pip install -U -r requirements.txt -q
# python multimodal-cli.py

# or 

# multimodal-cli.sh
# python -m venv env
# source env/bin/activate
# pip install -U -r requirements.txt -q
# python multimodal-cli.py
# for env cleanup: rm -rf env

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

def main():
    print("\n")
    print("-----------Configuration Setup-------------")
    choose = input("Choose: Conversation/Chat or Code?  ")

    if choose == "Conversation" or choose == "Chat":
        stream = input("Stream Output? (Yes/Y or No/N/Enter):  ")
        if stream == "":
            stream = "No"
        output = input("Save Output? (Yes/Y/Enter or No/N):  ")
        if output == "":
            output = "Yes"
        if output == "Yes" or output == "Y":
            print("\n")
            print("Conversation(s) will be saved as output.md")
        output_copy = ""

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

            output_copy = output_copy + f"\n\n **Prompt**: {prompt} \n\n **Output**: \n\n {response.text} \n \n\n --------------------- \n\n\n"

            # Save output
            if output == "Yes" or output == "Y":
                with open("output.md", "w") as file:
                    file.write(output_copy)

            # End the conversation
            stop = input("End the conversation? (Yes/Y or No/N/Enter):  ")
            print("\n \n")
            if stop == "":
                stop = "No"

            print("------------------------")
            if stop == "Yes" or stop ==  "Y":
                print("Chat Logout")

    if choose == "Code":
        file_name = input("File name with extension? ")
        # Open File
        try:
            with open(file_name, "r") as file:
                content = file.read()
            print("\n")
            print("Code: \n")
            print(content)

            print("\n")
            prompt = input("Prompt:  ")
            prompt_code = f"This code: \n\n {content}. \n\n {prompt}"
            print("\n")
            print("Output: \n")
            response = start_chat(prompt_code)

            # Save output
            with open("output.md", "w") as file:
                file.write(response.text)

        except:
            print("File not found")
            

if __name__ == '__main__':
    main()
        
        

        
    
        
