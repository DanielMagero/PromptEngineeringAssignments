##pip install os
##pip install google-genai
##pip install dotenv


#### please get yout API key at https://aistudio.google.com/api-keys
#### Then save the API key in a .env file GEMINI_API_KEY = "put_your_key_here" within the file
#### the .env is so that guys don't use your key

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


# --- 1. Initialize the Client ---

# The client automatically looks for the GEMINI_API_KEY 
# environment variable.
try:
    client = genai.Client()
    print("Client initialized successfully.")
except Exception as e:
    print(f"Error initializing client. Make sure GEMINI_API_KEY is set as an environment variable: {e}")
    exit()

# --- 2. Define the Prompt (Conversation) ---
# The 'contents' structure is used to define the conversation history/prompt.
# For a single-turn prompt, it typically includes a user role.
prompt_contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(text = "You will be provided with a sentence in English, and your task is to translate it into French."),
            types.Part(text = "My name is Jane. What is yours?")
        ]
    )
]

# --- 3. Generate Content (Call the API and get the response) ---
MODEL_NAME = "gemini-2.5-flash"

try:
    response = client.models.generate_content(
        model = MODEL_NAME,
        contents=prompt_contents,
        config=types.GenerateContentConfig(
            temperature=0.7,  # Adjust for creativity (0.0 for deterministic)
            max_output_tokens=1024,
        )
    )

    # --- 4. Display the Output ---
    print(f"Model Used: {MODEL_NAME}")
    print("\n--- Translation Response ---")

    if response.prompt_feedback is not None and response.prompt_feedback.block_reason:
        print(f"ERROR: Prompt was blocked. Reason: {response.prompt_feedback.block_reason.name}")
    elif response.text is not None:
        print(response.text.strip())
    else:
        print("No response text received.")
        if response.candidates and response.candidates[0].finish_reason:
            print(f"  - Finish Reason: {response.candidates[0].finish_reason.name}")


except genai.errors.APIError as e:
    print(f"An API error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")