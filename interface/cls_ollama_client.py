import json
import logging
import os
import subprocess
from typing import Any, Dict, Optional

import requests
from jinja2 import Template

from interface.cls_llm_messages import Chat, Role

# Configurations
BASE_URL = "http://localhost:11434/api"
TIMEOUT = 240  # Timeout for API requests in seconds
OLLAMA_CONTAINER_NAME = "ollama"  # Name of the Ollama Docker container
OLLAMA_START_COMMAND = [
    "docker",
    "run",
    "-d",
    "--gpus=all",
    "-v",
    "ollama:/root/.ollama",
    "-p",
    "11434:11434",
    "--name",
    OLLAMA_CONTAINER_NAME,
    "ollama/ollama",
]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class OllamaClient(metaclass=SingletonMeta):
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self._ensure_container_running()
        self.cache_file = "./cache/ollama_cache.json"
        self.cache = self._load_cache()

    def _ensure_container_running(self):
        """Ensure that the Ollama Docker container is running."""
        if self._check_container_exists():
            if not self._check_container_status():
                logger.info("Restarting the existing Ollama Docker container...")
                self._restart_container()
        else:
            logger.info("Starting a new Ollama Docker container...")
            self._start_container()

    def _check_container_status(self):
        """Check if the Ollama Docker container is running."""
        try:
            result = subprocess.run(
                [
                    "docker",
                    "inspect",
                    '--format="{{ .State.Running }}"',
                    OLLAMA_CONTAINER_NAME,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().strip('"') == "true"
        except subprocess.CalledProcessError:
            return False

    def _check_container_exists(self):
        """Check if a Docker container with the Ollama name exists."""
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "--filter", f"name={OLLAMA_CONTAINER_NAME}"],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() != ""

    def _restart_container(self):
        """Restart the existing Ollama Docker container."""
        subprocess.run(["docker", "restart", OLLAMA_CONTAINER_NAME], check=True)

    def _start_container(self):
        """Start the Ollama Docker container."""
        try:
            subprocess.run(OLLAMA_START_COMMAND, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(
                "Error starting the Ollama Docker container. Please check the Docker setup."
            )
            raise

    def _download_model(self, model_name: str):
        """Download the specified model if not available."""
        logger.info(f"Checking if model '{model_name}' is available...")
        if not self._is_model_available(model_name):
            logger.info(f"Model '{model_name}' not found. Downloading...")
            subprocess.run(
                ["docker", "exec", OLLAMA_CONTAINER_NAME, "ollama", "pull", model_name],
                check=True,
            )
            logger.info(f"Model '{model_name}' downloaded.")

    def _is_model_available(self, model_name: str) -> bool:
        """Check if a specified model is available in the Ollama container."""
        result = subprocess.run(
            ["docker", "exec", OLLAMA_CONTAINER_NAME, "ollama", "list"],
            capture_output=True,
            text=True,
        )
        return model_name in result.stdout

    def _load_cache(self):
        """Load cache from a file."""
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, "w") as cache_file:
                json.dump({}, cache_file)
        with open(self.cache_file, "r") as json_file:
            return json.load(json_file)

    def _get_cached_completion(self, model: str, temperature: str, prompt: str):
        """Retrieve cached completion if available."""
        cache_key = f"{model}:{temperature}:{prompt}"
        return self.cache.get(cache_key)

    def _update_cache(self, model: str, temperature: str, prompt: str, completion: str):
        """Update the cache with new completion."""
        cache_key = f"{model}:{temperature}:{prompt}"
        self.cache[cache_key] = completion
        with open(self.cache_file, "w") as json_file:
            json.dump(self.cache, json_file, indent=4)

    def _send_request(
        self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Send an HTTP request to the given endpoint."""
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, timeout=TIMEOUT)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=TIMEOUT)
            elif method == "DELETE":
                response = requests.delete(url, json=data, timeout=TIMEOUT)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            raise

    def _get_template(self, model: str):
        data = {"name": model}
        response = self._send_request("POST", "show", data).json()
        return response["template"]

    def generate_completion(
        self,
        model: str,
        prompt: str | Chat,
        start_response_with: str = "",
        instruction: str = "Anticipate user needs and conversation directions, responding in a manner that is both informative and practical.",
        temperature: float = 0.8,
        stream: bool = False,
        **kwargs,
    ) -> str:
        template_str = self._get_template(model)
        template_str = template_str.replace(".Prompt", "prompt").replace(
            ".System", "system"
        )
        if isinstance(prompt, Chat):
            prompt_str = prompt.to_jinja2(template_str)
        else:
            template = Template(template_str)
            context = {"system": instruction, "prompt": prompt}
            prompt_str = template.render(context) + start_response_with

        prompt_str += start_response_with

        # Check cache first
        cached_completion = self._get_cached_completion(model, temperature, prompt_str)
        if cached_completion:
            return start_response_with + cached_completion["response"]
        # If not cached, generate completion
        data = {
            "model": model,
            "prompt": prompt_str,
            "temperature": temperature,
            "raw": bool(instruction),
            "stream": stream,
            **kwargs,
        }
        response = self._send_request("POST", "generate", data)

        # Assuming response is a dictionary containing the completion
        completion = (
            response.json()
            if not stream
            else [
                json.loads(line.decode("utf-8"))
                for line in response.iter_lines()
                if line
            ]
        )

        # Update cache
        self._update_cache(model, temperature, prompt_str, completion)

        return start_response_with + completion["response"]


ollama_client = OllamaClient()