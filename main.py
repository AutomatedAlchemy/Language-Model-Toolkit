import asyncio
import json
import os
import shutil
import subprocess
import tkinter as tk
from typing import List

import matplotlib.pyplot as plt
import networkx as nx
import openai

from interface.cls_chat_session import ChatSession

# from interface.cls_llm_host_interface import LlmHostInterface, cls_llm_host_interface


def list_openai_engines():
    engines = openai.Engine.list()
    for engine in engines.data:
        print(f"Openai:\t{engine.id}")


# def list_oobabooga_models():
#     for model in OobaboogaClient().list_available_models():
#         print(f"Local:\t{model}")


def setup_sandbox():
    sandbox_dir = "./sandbox/"
    if os.path.exists(sandbox_dir):
        shutil.rmtree(sandbox_dir)
    os.mkdir(sandbox_dir)


setup_sandbox()


def main():
    session = ChatSession()
    response = session.generate_completion("What is 2 + 2?")
    print(response)
    response = session.generate_completion("What if you add 3?")
    print(response)
    response = session.generate_completion("What if you add 3 again?")
    print(response)
    response = session.generate_completion(
        "Next i'd like you to add 5.",
        start_response_with="Well you're getting annoying, but",
    )
    response = session.generate_completion(
        "Next i'd like you to add a frog.",
        start_response_with="What a complicated equation. Intriguing nonetheless! To ",
    )
    response = session.generate_completion(
        "We're here to do science I say! Let's do a metaphorical leap to see what would happen! Proceed friend!",
    )
    print(response)

    exit(0)

    context = ""
    while True:
        context += input("Enter your next Prompt: ")
        api = OllamaClient()
        result = api.generate_completion("openchat", context)
        print(result["response"])
        context += result["response"]


if __name__ == "__main__":
    main()
