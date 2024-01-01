import argparse
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import time as t

parser = argparse.ArgumentParser()
# parser.add_argument("--prompt", help="Prompt")
parser.add_argument("--range", help="Range")

args = parser.parse_args()

# print(args.prompt)
# print(args.range)

# Chat Model
mm_model = GenerativeModel("gemini-pro")
mm_chat = mm_model.start_chat()


def start_chat(prompt):
    start = t.time()
    response = mm_chat.send_message(prompt)
    print(response.text)
    end = t.time()
    # print(f"Total Processing Time: {end - start}")

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

for _ in range (int(args.range)):
    # prompt = args.prompt
    prompt = input("Prompt:  ")
    stream = input("Stream (T or F):  ")
    if stream == "T":
        start_chat_stream(prompt)
    elif stream == "F":
        start_chat(prompt)

    # Chat History
    print(mm_chat.history)