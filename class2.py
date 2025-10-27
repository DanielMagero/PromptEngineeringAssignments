# Requires: google-generativeai >= 0.7.2, python-dotenv >= 1.0.1
# Run: pip install --upgrade google-generativeai python-dotenv

import os
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables (including GEMINI_API_KEY)
load_dotenv()

try:
    # --- THIS IS THE CORRECTED PART (REVERTED) ---
    # Fetch the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY in environment. Add it to your .env file.")
    
    # Configure the genai library with the API key
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully.")
    # ---------------------------------

except RuntimeError as e:
    print(e)
    exit()
except Exception as e:
    print(f"Error during configuration: {e}")
    exit()

# System prompt remains the same
system_prompt = "You are an intelligent assistant. Make sure you stay within 10 words."

# Initialize the model and start the chat (this part was already correct)
try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt
    )
    chat = model.start_chat(history=[])  # Stateful chat carries context
    print("Model and chat initialized successfully.")
    
except Exception as e:
    print(f"Error initializing the model: {e}")
    exit()


print("\nType your messages. Type 'bye' to exit.\n")

# The chat loop (this part was also already correct)
while True:
    user_msg = input("User: ").strip()
    if not user_msg:
        continue
    if user_msg.lower() == "bye":
        print("Gemini: Goodbye 👋")
        break

    try:
        response = chat.send_message(user_msg)
        reply = (response.text or "").strip()
        if not reply:
            reply = "(No response received.)"
        print(f"Gemini: {reply}\n")
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")
        # You might want to break here if a fatal error occurs
        # break