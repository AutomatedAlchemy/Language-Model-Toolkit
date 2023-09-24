import asyncio

import websockets
from transformers import AutoModelForCausalLM, AutoTokenizer

from llm_graph_of_thoughts.classes.cls_template_llm_tokens import \
    cls_template_llm_tokens


class LLMHost:
    def __init__(self, model_path: str) -> None:
        self.device = "cuda"
        self.active_model_path = ""
        self.load_model(model_path)
        self.template = cls_template_llm_tokens()

    def load_model(self, model_path: str):
        if self.active_model_path != model_path and model_path != "":
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(model_path, device_map='cuda', trust_remote_code=True, revision="main").to(self.device)
            self.active_model_path = model_path  # Update active_model_path

    def prompt(self, user_prompt: str, instruction: str = "") -> str:
        if instruction:
            llm_input = self.template.create_instruction_prompt(instruction, user_prompt)
        else:
            llm_input = self.template.create_user_msg(user_prompt)
        response = self.generate_response(llm_input)
        return response

    def generate_response(self, prompt: str) -> str:
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=1024)
        return self.tokenizer.decode(outputs[0])

llm_host = None
async def websocket_handler(websocket, path):
    global llm_host
    
    if (llm_host is None):
        # When a client connects, create an LLMHost instance with the desired model path
        model_path: str = r"C:\Users\Steffen\Desktop\oobabooga_windows\text-generation-webui\models\TheBloke_Wizard-Vicuna-7B-Uncensored-GPTQ\\"
        llm_host = LLMHost(model_path)
    
    async for message in websocket:
        response = llm_host.prompt(message)
        print("\n### MESSAGE ###\n")
        print(message)
        print("\n### RESPONSE ###\n")
        print(message)
        await websocket.send(response)

if __name__ == "__main__":
    start_server = websockets.serve(websocket_handler, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)  # Use run_until_complete here
    asyncio.get_event_loop().run_forever()