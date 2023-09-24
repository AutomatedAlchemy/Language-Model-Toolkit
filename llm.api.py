import asyncio

import websockets
from transformers import AutoModelForCausalLM, AutoTokenizer


class LLMHost:
    def __init__(self, model_path: str) -> None:
        self.device = "cuda"
        self.active_model_path = ""
        self.load_model(model_path)

    def load_model(self, model_path: str):
        if self.active_model_path != model_path and model_path != "":
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(model_path, device_map='cuda', trust_remote_code=True, revision="main").to(self.device)
            self.active_model_path = model_path  # Update active_model_path

    def prompt(self, prompt) -> str:
        response = self.generate_response(prompt)
        return response

    def generate_response(self, prompt: str) -> str:
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=1024)
        # outputs = self.model.generate(inputs=input_ids, num_beams=4, num_return_sequences=2)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt,"")

model_path: str = r"C:\Users\Steffen\Desktop\oobabooga_windows\text-generation-webui\models\TheBloke_Wizard-Vicuna-7B-Uncensored-GPTQ\\"
async def websocket_handler(websocket, path):
    global llm_host
    
    if (llm_host is None):
        # When a client connects, create an LLMHost instance with the desired model path
        llm_host = LLMHost(model_path)
    
    async for message in websocket:
        print("\n--- REQUEST RECEIVED ---\n")
        response = llm_host.prompt(message)
        print("\n### MESSAGE ###\n")
        print(message)
        print("\n### RESPONSE ###\n")
        print(response)
        await websocket.send(response)

if __name__ == "__main__":
    llm_host = None  # Initialize llm_host as None
    
    start_server = websockets.serve(websocket_handler, "0.0.0.0", 8765)

    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up resources and close the WebSocket server properly
        asyncio.get_event_loop().run_until_complete(start_server.wait_closed())