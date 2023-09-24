import asyncio

from classes.cls_template_llm_tokens import cls_template_llm_tokens
from classes.cls_template_reponse_structures import \
    cls_template_reponse_structures

from ..client.websocket_client import send_request


class cls_llm_host_interface():
    template: cls_template_llm_tokens
    def __init__(self):
        self.template = cls_template_llm_tokens()
    
    def prompt(self, user_message:str, instruction_message:str=None):
        prompt = ""
        if (instruction_message is not None):
            prompt += self.template.create_instruction_msg(instruction_message)
        prompt += self.template.create_user_msg(user_message, instruction_message==None)
        return asyncio.run(send_request(prompt))
        
    def prompt_for_structure(self, user_message:str, structure_template:dict[str,str]):
        prompt = ""
        prompt += self.template.create_instruction_msg(structure_template["REQUEST"])
        prompt += self.template.create_user_msg(structure_template["EXAMPLE_PROMPT"])
        prompt += self.template.create_llm_msg(structure_template["EXAMPLE_RESPONSE"]) 
        prompt += self.template.create_user_msg(user_message)
        return asyncio.run(send_request(prompt))