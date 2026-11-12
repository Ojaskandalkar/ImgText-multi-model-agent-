import os
from agent import ask_agent

def main():
    print("=====================================================")
    print(" 🧠 Multimodal MCP Agent (Gemini 3.5 Flash-Lite) ")
    print("=====================================================")
    print("1. Place your files in the 'uploads/' folder.")
    print("2. Ask the agent to upload them (e.g., 'Upload policy.pdf').")
    print("3. Type 'exit' to quit.\n")
    
    os.makedirs("uploads", exist_ok=True)
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            if not user_input.strip():
                continue
                
            print("\n[Agent is thinking and using tools...]")
            response = ask_agent(user_input)
            
            print("\nAgent:")
            print(response)
            print("-" * 50)
            
        except Exception as e:
            print(f"\n[System Error]: {e}")

if __name__ == "__main__":
    main()