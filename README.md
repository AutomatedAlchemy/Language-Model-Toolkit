
# Python Module for Conversational AI Interactions

This Python module, built around the `OllamaClient`, facilitates generating text completions and managing interactive chat sessions. It is designed to serve as a foundational tool for developers, researchers, and hobbyists who are exploring conversational AI technologies. The module provides a straightforward interface for sending prompts to a conversational AI model and receiving generated responses, suitable for a wide range of applications from chatbots to creative writing aids.

## Features

- **Sandbox Setup:** Automates the creation of a sandbox environment for safe and isolated operation.
- **Text Generation:** Supports sending individual prompts to the AI model and receiving text completions.
- **Interactive Chat:** Allows for dynamic chat sessions with the AI, enabling real-time conversation simulations.

## Getting Started

### Installation

Ensure Python 3.6+ is installed. Clone this repository and install the required dependencies to get started:

```bash
git clone https://github.com/yourusername/conversational-ai-module.git
cd conversational-ai-module
pip install -r requirements.txt
```

### Quick Start

Import the `OllamaClient` in your Python script to begin interacting with the conversational AI model:

```python
from interface.cls_ollama_client import OllamaClient

# Initialize the client
client = OllamaClient()

# Generate a single completion
response = client.generate_completion("Your prompt here.")
print(response)
```

### Running Interactive Chat

To engage in an interactive chat session, you can use the following pattern in your script:

```python
client = OllamaClient()

while True:
    user_input = input("Enter your prompt: ")
    response = client.generate_completion(user_input)
    print(response)
```

## Sandbox Environment

The module includes functionality to set up a sandbox environment, isolating your interactions and data. This is particularly useful for testing and development purposes.

### Setup Sandbox

Call `setup_sandbox()` before starting your session to prepare the environment:

```python
from your_module import setup_sandbox

setup_sandbox()
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features.

## License

This project is licensed under the MIT License - see the LICENSE file for more details.

## Acknowledgments

- Thanks to the developers and contributors who made this project possible.
- Special thanks to OpenAI for providing the API and support for conversational AI research and development.
