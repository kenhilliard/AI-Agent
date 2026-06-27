import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function

def main():
    # 1. load_environment, API key, client
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("No API key found")
    client = genai.Client(api_key=api_key)

    # 2. parse args
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # 3. build initial messages list
    messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    # 4. generate loop
    for _ in range(20):
        result = generate_content(client, messages, args.verbose)
        if result:
            print(result)
            return
    print("Max iterations reached")

def generate_content(client, messages, verbose):
    # 5. call client.models.generate_content
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents= messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0
    ))
    # 6. verbose output and error handling
    if verbose:            
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.usage_metadata is None:
        raise RuntimeError("failed API request")
    
    # 7. check the .candidates property of the response. if any, append the content into the messages list
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
            
    # 8. function call handling
    if response.function_calls is not None:
        function_results = []        
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if not function_call_result.parts:
                raise Exception("No parts in function result")
            if function_call_result.parts[0].function_response is None:
                raise Exception("No response in function result")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("No response content in function result")
            function_results.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        # append tool resonses
        messages.append(types.Content(role="user", parts=function_results))
    else:        
        # return response.text when no more function calls are present, and it has an answer for the user
        return response.text
        
if __name__ == "__main__":
    main()