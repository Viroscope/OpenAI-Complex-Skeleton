# Open AI Complex Skeleton

The Open AI Complex Skeleton is a Python program that demonstrates a conversation-based interaction with the OpenAI GPT-3.5 language model. It allows users to communicate with the model by sending queries and receiving responses. The program utilizes the OpenAI API to generate chat-based completions.

## Prerequisites
Before running the program, make sure you have the following dependencies installed:
- Python 3.x
- OpenAI Python library (`openai`)
- `dotenv` Python library

You will also need an OpenAI API key, which can be obtained by creating an account on the OpenAI website.

## Setup
1. Clone or download the program's source code.
2. Install the required Python libraries by running the following command:
   ```
   pip install openai python-dotenv
   ```
3. Create a file named `.env` in the program's directory and add the following line, replacing `YOUR_API_KEY` with your actual OpenAI API key:
   ```
   OpenAIKey=YOUR_API_KEY
   ```

## Usage
1. Import the necessary modules:
   ```python
   import os
   from dotenv import load_dotenv
   import openai
   import json
   ```

2. Load the environment variables and set the OpenAI API key:
   ```python
   load_dotenv()
   openai.api_key = os.getenv('OpenAIKey')
   ```

3. Define the function descriptions and their parameters:
   ```python
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
   ```

4. Define the `function_call` function to handle the responses from the OpenAI model:
   ```python
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
           two = eval(arguments).get("two")
           print(f"Function 2 {one}{two}")
           return
       
       else: 
           return
   ```

5. Define the `feedback` function to send queries and receive responses:
   ```python
   def feedback(query):
       messages = [{"role": "user", "content": query}]
       
       response = openai.ChatCompletion.create(
           model="gpt-3.5-turbo-0613",
           messages=messages,
           functions=function_descriptions,
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
               functions=function_descriptions,
               function_call="auto"
           )
           
           print("\n" + response['choices'][0]['message']['content'].strip())
   ```

6. Start the conversation by calling the `feedback` function and passing the user's query:
   ```python
   feedback("Hello, what can you do?")
   ```

## Explanation
The program follows a simple conversational structure where the user sends queries, and the program responds accordingly.

1. The `feedback` function takes a query as input and initializes the conversation by creating a list of messages. The user's query is added as the first message.

2. The `openai.ChatCompletion.create` method is called to generate a response from the OpenAI model. The `model` parameter specifies the GPT-3.5 model to use, and the `messages` parameter contains the conversation history.

3. If the response indicates a function call, the `function_call` function is invoked to handle the specific function requested by the model.

4. The function call and its response are added to the message list, and the conversation continues by calling `openai.ChatCompletion.create` again.

5. The process continues until the response indicates that the conversation is finished. The program prints the generated content of the response.

Note that the program assumes there are two specific functions named "function_1" and "function_2." You can modify the function descriptions and implementation according to your specific use case.

## Limitations and Enhancements
- The program uses a specific model (`gpt-3.5-turbo-0613`). You can experiment with other models offered by OpenAI to achieve different behaviors and results.
- The current implementation handles two specific functions. To expand the program's functionality, you can add more function descriptions and their corresponding implementations.
- The program assumes a simple input-output structure. For more complex conversations, you may need to modify the code and handle the responses differently.
- Be cautious when using `eval` to parse the function arguments. Ensure that the input is safe and well-formed to prevent any potential security risks.

## Conclusion
The Open AI Complex Skeleton provides a starting point for building conversational applications using the OpenAI GPT-3.5 language model. By following the provided structure, you can extend the program's functionality and create more interactive and dynamic conversations.
