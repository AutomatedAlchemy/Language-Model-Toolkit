
class cls_template_llm_tokens:
    def __init__(self, load_llama2_template=True):
        if not load_llama2_template:
            raise Exception("Not implemented")
        self.__prompt_start = "[INST]"
        self.__instruction_start = self.__prompt_start + " <<SYS>>\n"
        self.__instruction_end = "\n<</SYS>>\n\n"
        self.__user_end = " [/INST] "
        self.__llm_end = " [INST] "

    def create_instruction_msg(self, instruction: str) -> str:
        return self.__instruction_start + instruction + self.__instruction_end

    def create_user_msg(self, prompt: str, start_of_prompt: bool = True) -> str:
        if (start_of_prompt):
            return self.__prompt_start + prompt + self.__user_end
        else:
            return prompt + self.__user_end

    def create_llm_msg(self, response: str) -> str:
        return response + self.__llm_end

    def is_valid_template(self, prompt: str):
        return self.__instruction_start in prompt or self.__instruction_end in prompt or self.__user_end in prompt or self.__llm_end in prompt

test = cls_template_llm_tokens()
test.create_llm_msg("")