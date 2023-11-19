import asyncio
import json
import os
import shutil
import subprocess
import time
import tkinter as tk
from typing import List

import matplotlib.pyplot as plt
import networkx as nx
import openai

from interface.cls_chat_session import ChatSession
from interface.cls_ollama_client import OllamaClient


def list_openai_engines():
    engines = openai.Engine.list()
    for engine in engines.data:
        print(f"Openai:\t{engine.id}")


def setup_sandbox():
    sandbox_dir = "./sandbox/"
    if os.path.exists(sandbox_dir):
        shutil.rmtree(sandbox_dir)
    os.mkdir(sandbox_dir)


setup_sandbox()


if __name__ == "__main__":
    # 1. Example usage - Single prompt
    session = OllamaClient()
    while True:
        response = session.generate_completion(
            input("###\tEnter your prompt:\n"),
        )
        print(response)

    # 2. Example usage - Multiple rounds of chat
    session = ChatSession()
    while True:
        response = session.generate_completion(
            input("###\tEnter your prompt:\n"),
        )
        print(response)
