import json
import math
from enum import Enum
from typing import List, Tuple, Union


class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Chat:
    def __init__(self, user_message: str, instruction_message: str = ""):
        self.messages: List[tuple[Role, str]] = []
        if instruction_message:
            self.add_message(Role.SYSTEM, instruction_message)
        self.add_message(Role.USER, user_message)

    def add_message(self, role: Role, content: str):
        self.messages.append((role, content))

    def __str__(self):
        return json.dumps([{"role": message[0].value, "content": message[1]} for message in self.messages])

    def to_openai_chat(self):
        return [{"role": message[0].value, "content": message[1]} for message in self.messages]

    def to_oobabooga_history(self) -> Tuple[dict, str]:
        internal_arr: list[str] = []
        visible_arr: list[str] = []
        instruction: str = ""
        if self.messages[0][0] == Role.SYSTEM:
            instruction = self.messages[0][1]

        user_assistant_arr = ["", ""]
        for i in range(len(self.messages)):
            if self.messages[i][0] == Role.SYSTEM:
                instruction = self.messages[0][1]

            elif self.messages[i][0] == Role.USER:
                user_assistant_arr[0] = self.messages[i][1]

            elif self.messages[i][0] == Role.SYSTEM:
                user_assistant_arr[1] = self.messages[i][1]
                internal_arr.append(user_assistant_arr)
                visible_arr.append(user_assistant_arr)
                user_assistant_arr = ["", ""]

        if not user_assistant_arr[1]:
            user_assistant_arr[1] = "Sure! "

        if user_assistant_arr[0] or user_assistant_arr[1]:
            internal_arr.append(user_assistant_arr)
            visible_arr.append(user_assistant_arr)
        # for i in range((1 if instruction else 0), math.ceil((len(self.messages)) / 2)):
        #     user_assistant_arr = []
        #     user_assistant_arr.append(self.messages[i * 2][0].value)
        #     user_assistant_arr.append(self.messages[i * 2 + 1][1])
        #     internal_arr.append(user_assistant_arr)
        #     visible_arr.append(user_assistant_arr)

        return {"internal": internal_arr, "visible": visible_arr}, instruction
