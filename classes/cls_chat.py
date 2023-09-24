from interface.cls_llm_host_interface import cls_llm_host_interface


class cls_chat:
    def __init__(self, llm_host: cls_llm_host_interface, instruction: str = ""):
        self.__llm_host = llm_host
        if (instruction!=""):
            self.__instruction = self.__llm_host.template.create_instruction(instruction)
            self.chat_storage = self.__instruction
        else:
            self.chat_storage = ""
            
    def chat(self, message: str):
        self.chat_storage += self.__llm_host.template.create_prompt(message)
        response = self.__llm_host.prompt(self.chat_storage)
        self.chat_storage += self.__llm_host.template.create_response(response)
        return response
        
