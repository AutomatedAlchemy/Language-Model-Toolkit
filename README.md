# Welcome to the (Local)-Language-Model-Toolkit

Welcome to the (Local)-Language-Model-Toolkit, an open-source framework designed to serve as a foundation for building advanced language model tools. Whether you're a seasoned developer or a newcomer eager to automate tasks requiring contextual understanding, this project is tailored to your needs.

# Getting Started

## Getting Started
    1.Rename .env.example to .env, insert the path of you local language models (ex.: "..\text-generation-webui-main\models") and/or insert your OpenAI token.
    2.Manually launch the llm.api.py to run in the background and serve models.
    3.Run your project by execute the main.py file (ensure llm.api.py is active for local LLM support). This will print out all available models (local and OpenAI).
    3.To start a custom project, it's recommended to begin by implementing and experimenting in the main.py file.

    NOTES:
    When executing the main.py file all available models (OPENAI and local) will be printed. To use a model, insert its name into the "cls_llm_host_interface" class!

## Project Execution


# Contributing

I'd love to hear what you think about this project! Dive in, propose/(commit) changes, or simply share your thoughts. Feedback is highly encouraged.

# License

This project is open source and is provided as-is. You are free to use it at your discretion. Please review the LICENSE file for more details.


Enjoy!