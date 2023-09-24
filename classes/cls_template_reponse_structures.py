import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class cls_template_reponse_structures:
    @staticmethod
    def task_to_microtask():
        return {
            "REQUEST": "Let's split the following into manageable microtasks:",
            "EXAMPLE_PROMPT": "Let's split the following into manageable microtasks: 'Could you establish my online presence by creating a website?'",
            "EXAMPLE_RESPONSE": """{
                "Tasks": [
                    "1. Define Website Purpose - Determine your website's main goal",
                    "2. Plan Structure and Content - Outline site structure and content",
                    "3. Domain and Hosting - Choose a domain, purchase it, and get hosting",
                    "4. Select Website Builder - Pick a user-friendly builder/CMS",
                    "5. Design Website - Choose a purposeful template, customize with branding",
                    "6. Create Content - Write text, gather media, add content",
                    "7. Add Key Features - Implement contact forms, social links, navigation",
                    "8. Mobile Optimization - Ensure mobile-friendly design",
                    "9. Test and Debug - Thoroughly test and fix issues",
                    "10. SEO Optimization - Add keywords, meta tags, optimize images",
                    "11. Implement Security - Set up SSL encryption",
                    "12. Launch Website - Connect the domain, make it live",
                    "13. Announce and Monitor - Share the launch, gather user feedback"
                ]
            }"""
        }

    @staticmethod
    def indexValue_to_string(index: str):
        return {
            "REQUEST": f"Let's extract the {index} value from the following:",
            "EXAMPLE_PROMPT": "Let's extract the second value from the following: '\"Strategy\": {\"Steps\": [\"1. Define Website Purpose - Determine your website's main goal\",\"2. Plan Structure and Content - Outline site structure and content\",\"3. Domain and Hosting - Choose a domain, purchase it, and get hosting\"]}'",
            "EXAMPLE_RESPONSE": "Plan Structure and Content - Outline site structure and content"
        }
        
    @staticmethod
    def success_analysis():
        return {
            "REQUEST": "Assess the feasibility of a given set of steps and provide a probability estimate, ranging from 0.00 to 1.00, to predict the likelihood of successfully reaching the goal when the steps are followed.",
            "EXAMPLE_PROMPT": "Assess the feasibility of the following steps and provide a probability estimate of successfully reaching the goal: '1. Define the project scope 2. Gather required resources 3. Develop a project plan 4. Execute the plan 5. Monitor progress'",
            "EXAMPLE_RESPONSE": "0.75"
        }
        
    @staticmethod
    def is_python_needed():
        return {
            "REQUEST": "Determine if the request suggests the need for a Python script.",
            "EXAMPLE_PROMPT": "I need to research advanced prompting techniques for large language models.",
            "EXAMPLE_RESPONSE": "True"
        }   
        
    @staticmethod
    def extract_script():
        return {
            "REQUEST": "Extract the python script which is contained within the text. Alter the code only to be syntactically correct and executable.",
            "EXAMPLE_PROMPT": """
            Sure, here's the same Python script with all comments removed:

python

import requests
from bs4 import BeautifulSoup

url = 'https://example.com'

try:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find(class_='content')
        extracted_string = element.get_text() if element else 'Element not found'
        print(extracted_string)
    else:
        print(f'Failed to retrieve the web page. Status code: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')

except Exception as e:
    print(f'An unexpected error occurred: {e}')

Please note that while removing comments may make the code shorter, comments are essential for understanding and maintaining code in a real-world development environment.
            """,
            "EXAMPLE_RESPONSE": """import requests
from bs4 import BeautifulSoup

url = 'https://example.com'

try:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find(class_='content')
        extracted_string = element.get_text() if element else 'Element not found'
        print(extracted_string)
    else:
        print(f'Failed to retrieve the web page. Status code: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')

except Exception as e:
    print(f'An unexpected error occurred: {e}')"""
        }
        
    @staticmethod
    def check_goals():
        return {
            "REQUEST": "Check if the response contains all expected goals. The Goals are: 'To Check if our weatherstation works the script needs to return the temperature in Nuremberg which can be extracted from wetter.com. '",
            "EXAMPLE_PROMPT": "Nuremberg: 24 degrees Celsius, Sunny  ",
            "EXAMPLE_RESPONSE": "True"
        }  

