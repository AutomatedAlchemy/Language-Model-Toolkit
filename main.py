import json
import os
import pydoc
import subprocess
import time
from enum import Enum

from classes.cls_chat import cls_chat
from classes.cls_template_reponse_structures import \
    cls_template_reponse_structures
from interface.cls_llm_host_interface import cls_llm_host_interface

llm = cls_llm_host_interface()

def Identify_Steps(request):
    instruction = "Your role is that of a prompt interpreter. As you approach this task, envision the required actions to craft a strategic, step-by-step route for responding to the user with high confidence of success. Outline the thought process you would follow to achieve this."
    response = llm.prompt(request, instruction) 
    return response

def is_reasonable(steps:str) -> float:
    response = llm.prompt_for_structure(steps, cls_template_reponse_structures.success_analysis()) 
    response_float = float(response)
    return response_float

#Planning System
def achieve_request(goal: str):
    steps = Identify_Steps(goal)
    if (is_reasonable(steps)>0.90):
        response = utilise_tool(steps)
        return response
    else:
        tasks_string = llm.prompt_for_structure(steps, cls_template_reponse_structures.task_to_microtask())
        tasks_obj = json.loads(tasks_string)
        tasks = tasks_obj["Tasks"]
        intermediate_chat = ""
        for task in tasks:
            intermediate_chat += task
            intermediate_chat = achieve_request(intermediate_chat)
        return response
		
def reason(reasoning_context:str, COT:bool, REFLECT:bool):
    chat = cls_chat(llm)
    if COT:
        reasoning_context = "Let's think about the following step by step: " + reasoning_context
    response = chat.chat(reasoning_context)
    if REFLECT:
        chat.chat("Let's reflect on your response and verify if we haven't made any mistakes.")
        response = chat.chat("Let's summarize.")
    return response
        

def utilise_tool(concrete_steps):
    for step in concrete_steps:
        python_needed_str = (llm.prompt_for_structure(step, cls_template_reponse_structures.is_python_needed()))
        python_needed = bool(python_needed_str)
        if (python_needed):
            response = Script(step)
        else:
            response = reason(step, COT = True, REFLECT = True)
        return response


def Script(step:str):
	description_prompt = f"Clearly define the requirements and the desired features for a python project which achieves the following: {step}"
	description = reason(description_prompt)
	# project_path = search_for_applicable_project(Description)
	# if (project_path!=""):
	# 	UtiliseProject()
	# else:
	CreateProject(description)

def CreateProject(description):
	milestones_prompt = "Plan the project by breaking down tasks and setting milestones." + "\n" + description
	milestones = reason(milestones_prompt)
	design_prompt = "Design the software architecture, creating a high-level design of the system's components and interactions." + "\n" + description + "\n" + milestones
	design = reason(design_prompt)
	Implementation = "Implement the core functionality by writing clean and modular code to build the essential features."
	Iterate_until_finished(Implementation, description + "\n" + milestones_prompt + "\n" + design)
	# Optimization = "Optimize and refactor your code to improve performance, readability, and adherence to coding standards."

	
def search_for_applicable_project(description):
	documentation = generate_folder_documentation("./sandbox/")
	path = reason("I need you to check if any of the listed projects can be utilised or expanded for the following requirements: " + description + "\n\nProject list" + documentation)
	return path

def generate_folder_documentation(folder_path):
    module_names = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                module_name = os.path.splitext(file)[0]
                module_names.append(module_name)

    documentation = ""

    for module_name in module_names:
        try:
            module = __import__(module_name)
            module_documentation = pydoc.render_doc(module)
            documentation += module_documentation
        except ImportError:
            documentation += f"Error: Failed to import module '{module_name}'\n"

    return documentation


def Iterate_until_finished(goals: str):
	current_output_state = reason(current_input_state, True, True)
	goals_state = verify_functionality(goals, current_output_state)
	if (goals_state.all()):
		return current_output_state
	else:
		current_input_state = "You are a software developer, tasked with fixing code. The code you are fixing has been tested and came back with unsuccessfully implemented functionality. Utilise the test feedback to fix the existing issues. Feedback:\n{goals_state}\n\nCode:\n{current_output_state}"
		current_output_state = reason(current_input_state, COT = True, REFLECT = True)

def read_script(script_name):
    try:
        with open('sandbox/' + script_name, 'r') as file:
            script_code = file.read()
        return script_code
    except FileNotFoundError:
        return f"Error occurred:\nFileNotFoundError"	
		
def save_script(script):
	with open('sandbox/' + "test.py", 'w') as file:
			file.write(script)

def execute_script(script_name = "test.py"):
    result = subprocess.run(['python', 'script.py'], capture_output=True, text=True)
    output = result.stdout.strip()
    error = result.stderr.strip()
    if error:
        return f"Error occurred:\n{error}"
    else:
        return output
    
def verify_functionality(goals, current_output_state):
    script = llm.prompt_for_structure(current_output_state, cls_template_reponse_structures.extract_script())
    save_script(script)
    script_output = execute_script(script)
    works_str = llm.prompt_for_structure(script_output, cls_template_reponse_structures.check_goals_state())
    works = bool(works_str)
    return works

user_input: str = "Implement a python script to fetch the titles of the trending topics on 4chan and show them to me in a list."
achieve_request(user_input)