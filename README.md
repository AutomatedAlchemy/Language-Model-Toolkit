(Local)-Language-Model-Toolkit

Welcome to the (Local)-Language-Model-Toolkit, an open-source framework designed to serve as a foundation for building advanced language model tools. Whether you're a seasoned developer or a newcomer eager to automate tasks requiring contextual understanding, this project is tailored to your needs.
Getting Started
Local Language Models

To use local language models, follow these steps:

    Manually launch the llm.api.py to run in the background and serve models.

Configuration

Before you get started, make sure to configure your environment:

    Rename .env.example to .env.
    Insert the path of your local language models (e.g., ..\text-generation-webui-main\models) in the .env file.
    Insert your OpenAI token in the .env file.

Implementing Your Project

To implement your project using this toolkit:

    Start working in the main.py file.
    When you execute the main.py file, all available models (OPENAI and local) will be printed.
    Insert your choice in the cls_llm_host_interface class for direct use.

Project Execution

To run your project, execute the main.py file. Ensure that llm.api.py is active for local LLM support.
Contributing

We welcome contributions and feedback:

    Dive in, propose changes, or commit your improvements.
    Share your thoughts and suggestions.
    Feedback is highly encouraged.

License

This project is open source and is provided as-is. You are free to use it at your discretion. Please review the LICENSE file for more details.

Enjoy!