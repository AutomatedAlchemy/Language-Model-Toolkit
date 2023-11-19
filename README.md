# Welcome to the (Local)-Language-Model-Toolkit

Welcome to the (Local)-Language-Model-Toolkit, an open-source framework designed for integrating advanced language models into your applications. This toolkit is ideal for both experienced developers and beginners interested in leveraging the power of language models for automation and contextual understanding.

## Getting Started

### 1. Install the Required Dependencies

To set up your environment, first install the necessary dependencies as listed in the `requirements.txt` file. Use `pip` for installation:

pip install -r requirements.txt

This command installs all the required packages for the project.

### 2. Configure Environment

The environment setup is now streamlined:

1. Rename `.env.example` to `.env`.
2. In the `.env` file, only insert your OpenAI API key, as this is now solely used for authenticating with OpenAI.

### 3. Set Up Ollama with Docker

Instead of using `llm.api.py`, the project now employs Ollama, running in a Docker container. To interface with it, use the REST API provided by Ollama. If you have the Docker container installed, it will automatically start when stopped by the project.

### 4. Run Your Project

Execute the `main.py` file to run your project. With the integration of Ollama, local language model support is automatically managed. The system will fetch and list all available models, both locally and from OpenAI.

### 5. Customize Your Project

For custom development, start by experimenting within the `main.py` file. Ollama will automatically download any model that is not available locally but exists on the Ollama model hub.

## Contributing

Your thoughts and contributions to this project are invaluable. Feel free to dive in, propose changes, commit updates, or share your feedback. All forms of engagement are highly encouraged.

## License

This project remains open source and is provided as-is. You have the freedom to use and adapt it according to your needs.

Enjoy your journey with the (Local)-Language-Model-Toolkit!
