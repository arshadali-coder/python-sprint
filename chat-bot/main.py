import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def Chatbot():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        print("Please add your API key to the .env file.")
        return

    # Initialize the client
    client = genai.Client(api_key=api_key)
    
    # Create a chat session
    chat = client.chats.create(model='gemini-2.5-flash')
    
    print("Chatbot connected to Gemini API (google-genai). Type 'quit' to exit.")
    print("-" * 40)

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break
            
        if not user_input:
            continue

        # Generate response
        response = chat.send_message(user_input)
        print(f"Gemini: {response.text}")
        print("-" * 40)

if __name__ == "__main__":
    Chatbot()
