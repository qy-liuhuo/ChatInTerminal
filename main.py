import time
import os
from openai import OpenAI
from rich import print
from rich.console import Console
from rich.markdown import Markdown
import argparse

parser = argparse.ArgumentParser(description="answer your question by chatgpt3.5")
parser.add_argument('question', type=str, nargs='?', default="hello", help="Descript your question")
parser.add_argument('-printMethod', '-p', type=str, choices=['normal', 'stream'], default='normal',
                    help="Choose the method for print: normal or stream")
parser.add_argument('-longDialog', '-l', type=str, choices=['true', 'false'], default='false',
                    help="Setting whether or not to have a continuous dialog")
args = parser.parse_args()

console = Console()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.chatanywhere.tech/v1"
)

def normal_method():
    message = args.question
    messages = [{
        "role": "user",
        "content": message
    }]
    while True:
        console.print("please wait....")
        result = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        console.print(Markdown(result.choices[0].message.content))
        if args.longDialog == 'true':
            new_question = input("Q:")
            if new_question == "exit":
                break
            messages.append({"role": "system", "content": result.choices[0].message.content})
            messages.append({
                "role": "user",
                "content": new_question
            })
        else:
            break


def stream_method():
    message = args.question
    messages = [{
        "role": "user",
        "content": message
    }]
    while True:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        result = ""
        # print(completion.choices[0].message.content)
        for chunk in stream:
            temp = (chunk.choices[0].delta.content or "")
            result = result + temp
            console.print(temp, end="")
            # print(chunk.choices[0].delta.content or "",end="")
        console.clear()
        console.print(Markdown(result))

        if args.longDialog == 'true':
            new_question = input("Q:")
            if  new_question == "exit":
                break
            messages.append({"role": "system", "content": result})
            messages.append({
                "role": "user",
                "content": new_question
            })
        else:
            break


if args.printMethod == "normal":
    normal_method()
elif args.printMethod == "stream":
    stream_method()
