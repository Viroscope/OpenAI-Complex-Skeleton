import os                                                                                         
from dotenv import load_dotenv                                                                  
import openai
import json

load_dotenv()                                                                                           
openai.api_key = os.getenv('OpenAIKey')                                                                   

function_descriptions = [
    {
        "name": "function_1",
        "description": "When the user asks to run function one",
        "parameters": {
            "type": "object",
            "properties": {
                "one": {
                    "type": "string",
                    "description": "User asked to run function one, with the required argument one"
                },
            },
            "required": ["one"]
        }
    },
    {
        "name": "function_2",
        "description": "When the user asks to run function two",
        "parameters": {
            "type": "object",
            "properties": {
                "one": {
                    "type": "string",
                    "description": "User asked for function two with argument one"
                },
                "two": {
                    "type": "string",
                    "description": "User asked for function two with argument two"
                },
            },
        }
    }
]

def function_call(ai_response):
    function_call = ai_response["choices"][0]["message"]["function_call"]
    function_name = function_call["name"]
    arguments = function_call["arguments"]
    
    if function_name == "function_1":
        one = eval(arguments).get("one")
        print(f"Function 1 {one}")
        return
     
    if function_name == "function_2":
        print('Function 2')
        one = eval(arguments).get("one")
        two = eval(arguments).get("toe")
        print(f"Function 2 {one}{two}")
        return
    
    else: 
        return

def feedback(query):
    messages = [{"role": "user", "content": query}]
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions = function_descriptions,
    function_call="auto"
    )

    while response["choices"][0]["finish_reason"] == "function_call":
        function_response = function_call(response)
        messages.append({
            "role": "function",
            "name": response["choices"][0]["message"]["function_call"]["name"],
            "content": json.dumps(function_response)
        })
        
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                functions = function_descriptions,
                function_call="auto"
        )
        
        print("\n"+response['choices'][0]['message']['content'].strip())

    print("\n"+response['choices'][0]['message']['content'].strip())

while True:
    user_input = input("User: ")
    feedback(user_input)