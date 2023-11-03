import asyncio
import html
import json
import re
import sys
from typing import Dict, List, Tuple

import requests
import websockets

from interface.cls_llm_messages import Chat, Role

# For local streaming, the websockets are hosted without ssl - ws://
WEBSOCKET_HOST: str = "localhost:5005"
WEBSOCKET_PROMPT_URI: str = f"ws://{WEBSOCKET_HOST}/api/v1/stream"
WEBSOCKET_CHAT_URI = f'ws://{WEBSOCKET_HOST}/api/v1/chat-stream'
REST_HOST: str = "localhost:5000"
REST_URI: str = f"http://{REST_HOST}/api/v1/model"


class OobaboogaClient:
    async def _websocket_generate_text_stream(self, prompt: str) -> str:
        action_data: dict = {
            "prompt": prompt,
            "max_new_tokens": 250,
            "auto_max_new_tokens": False,
            "max_tokens_second": 0,
            # Generation params. If 'preset' is set to different than 'None', the values
            # in presets/preset-name.yaml are used instead of the individual numbers.
            "preset": "None",
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.1,
            "typical_p": 1,
            "epsilon_cutoff": 0,  # In units of 1e-4
            "eta_cutoff": 0,  # In units of 1e-4
            "tfs": 1,
            "top_a": 0,
            "repetition_penalty": 1.18,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "repetition_penalty_range": 0,
            "top_k": 40,
            "min_length": 0,
            "no_repeat_ngram_size": 0,
            "num_beams": 1,
            "penalty_alpha": 0,
            "length_penalty": 1,
            "early_stopping": False,
            "mirostat_mode": 0,
            "mirostat_tau": 5,
            "mirostat_eta": 0.1,
            "grammar_string": "",
            "guidance_scale": 1,
            "negative_prompt": "",
            "seed": -1,
            "add_bos_token": True,
            "truncation_length": 2048,
            "ban_eos_token": False,
            "custom_token_bans": "",
            "skip_special_tokens": True,
            "stopping_strings": [],
        }

        print(prompt, end="")

        full_response: str = ""
        async for response in self._websocket_api(action_data):
            full_response += response
            print(response, end="")
            sys.stdout.flush()  # If we don't flush, we won't see tokens in realtime.
        return full_response
    
    
    async def _websocket_generate_chat_stream(self, user_input:str, history: Dict[str, List], instruction: str = "") -> str:
        request = {
            'user_input': user_input,
            'max_new_tokens': 250,
            'auto_max_new_tokens': False,
            'max_tokens_second': 0,
            'history': history,
            'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
            'character': 'Example',
            'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
            'your_name': 'You',
            # 'name1': 'name of user', # Optional
            # 'name2': 'name of character', # Optional
            # 'context': 'character context', # Optional
            # 'greeting': 'greeting', # Optional
            # 'name1_instruct': 'You', # Optional
            # 'name2_instruct': 'Assistant', # Optional
            # 'context_instruct': 'context_instruct', # Optional
            # 'turn_template': 'turn_template', # Optional
            'regenerate': False,
            '_continue': True,
            'chat_instruct_command':  instruction if instruction else 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>' ,

            # Generation params. If 'preset' is set to different than 'None', the values
            # in presets/preset-name.yaml are used instead of the individual numbers.
            'preset': 'None',
            'do_sample': True,
            'temperature': 0.7,
            'top_p': 0.1,
            'typical_p': 1,
            'epsilon_cutoff': 0,  # In units of 1e-4
            'eta_cutoff': 0,  # In units of 1e-4
            'tfs': 1,
            'top_a': 0,
            'repetition_penalty': 1.18,
            'presence_penalty': 0,
            'frequency_penalty': 0,
            'repetition_penalty_range': 0,
            'top_k': 40,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'mirostat_mode': 0,
            'mirostat_tau': 5,
            'mirostat_eta': 0.1,
            'grammar_string': '',
            'guidance_scale': 1,
            'negative_prompt': '',

            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'custom_token_bans': '',
            'skip_special_tokens': True,
            'stopping_strings': []
        }

        full_response: str = ""
        cur_len = 0
        async for response in self._websocket_api(request, True):
            cur_message = html.unescape(response['visible'][-1][1][cur_len:])
            cur_len += len(cur_message)
            full_response += cur_message
            print(cur_message, end="")
            sys.stdout.flush()  # If we don't flush, we won't see tokens in realtime.
        return full_response

    def decode_custom_escape_sequences(self, input_string:str):
        pattern = r'&#x([0-9A-Fa-f]+);'
        def replace(match):
            char_code = int(match.group(1), 16)
            return chr(char_code)
        decoded_text = re.sub(pattern, replace, input_string)
        return decoded_text

    async def _websocket_api(self, action_data: dict, chat_mode:bool=False):
        async with websockets.connect((WEBSOCKET_CHAT_URI if chat_mode else WEBSOCKET_PROMPT_URI), ping_interval=None) as websocket:
            await websocket.send(json.dumps(action_data))
            while True:
                incoming_data_json: str = await websocket.recv()
                incoming_data: dict = json.loads(incoming_data_json)
                match incoming_data['event']:
                    case 'text_stream':
                        yield incoming_data['history' if chat_mode else 'text' ]
                    case 'stream_end':
                        return

    def _rest_api(self, action_data: dict) -> dict:
        response = requests.post(REST_URI, json=action_data)

        if response.status_code == 200:
            result: dict = response.json()
            return result
        else:
            print(json.dumps(response))

    def _websocket_model_load(self, model_name: str) -> dict:
        action_data: dict = {"action": "load", "model_name": model_name}
        return self._rest_api(action_data)

    def _websocket_model_list(self) -> List[str]:
        action_data: dict = {"action": "list"}
        models: List[str] = self._rest_api(action_data)["result"]
        models.remove("None")
        return models

    def websocket_model_info(self) -> dict:
        action_data: dict = {"action": "info"}
        return self._rest_api(action_data)

    def _websocket_loaded_model(self) -> str:
        return self.websocket_model_info()["result"]["model_name"]

    def _websocket_get_template(self) -> tuple[str, str]:
        info: dict = self.websocket_model_info()
        return info["shared.settings"]["name1"], info["shared.settings"]["character"]

    def _websocket_model_unload(self) -> dict:
        action_data: dict = {"action": "unload"}
        return self._rest_api(action_data)

    def _websocket_stop_text_generation(self) -> dict:
        action_data: dict = {"action": "stop-stream"}
        return self._rest_api(action_data)

    def _websocket_count_tokens_in_prompt(self, prompt: str) -> dict:
        action_data: dict = {"action": "token-count", "prompt": prompt}
        return self._rest_api(action_data)

    def websocket_prompt(self, prompt: str, history: Dict[str,list] = []) -> str:
        if (history):
            generation: str = asyncio.run(self._websocket_generate_chat_stream(prompt))
        else:
            generation: str = asyncio.run(self._websocket_generate_text_stream(prompt))
        return generation

    def websocket_chat(self, chat:Chat) -> Chat:
        history, instruction = chat.to_oobabooga_history()
        generation: str = asyncio.run(self._websocket_generate_chat_stream("", history, instruction))
        chat.add_message(Role.ASSISTANT, generation) # if issues arise, then maybe the chat object was not passed as reference as hoped
        return generation

    def __init__(self):
        print()
        print("\n".join(self._websocket_model_list()))
        print()
        if self._websocket_loaded_model() == "None":
            self._websocket_model_load(self._websocket_model_list()[1])
            print(f"LOADING MODEL:\t{self._websocket_model_list()[3]}")
        print(f"LOADED MODEL:\t{self._websocket_loaded_model()}")
        print()
        
        chat = Chat("Can you implement a python script for generating a string of random numbers of length 42?")
        # prompt = "A higher temperature in large language model text generation causes the model to generate text which "
        self.websocket_chat(chat)


