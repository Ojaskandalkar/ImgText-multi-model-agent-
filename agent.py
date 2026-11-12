import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from tools import (
    upload_document, 
    list_documents, 
    get_document_content, 
    search_documents, 
    summarize_document
)

load_dotenv()

# Initialize Gemini Client
client = genai.Client()

SYSTEM_INSTRUCTION = """
You are a highly capable Multimodal Document Assistant.
You have tools to upload, list, retrieve, search, and summarize documents.

AGENT BEHAVIOR RULES:
- When asked "What files are uploaded?", call list_documents().
- When asked "What is in [file]?", call get_document_content(file_name).
- When asked to "Compare uploaded files", read every file and compare them.
- When asked to "Summarize everything", read all files and create a consolidated summary.

STRICT RESPONSE FORMAT:
You MUST format your final response EXACTLY like this:
- Answer: [Your detailed answer]
- Source File Name: [Name of the file(s) used]
- Source Pages (for PDFs): [Page numbers if applicable, else N/A]
- Confidence: [High/Medium/Low]

ANTI-HALLUCINATION PROTOCOL:
If the answer cannot be found in the documents via your tools, you MUST reply EXACTLY with:
"No information found in uploaded documents."
Do not attempt to guess or use outside knowledge.
"""

# Create a Chat session with tools enabled
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.0, # Keep it deterministic and factual
        tools=[
            upload_document, 
            list_documents, 
            get_document_content, 
            search_documents, 
            summarize_document
        ]
    )
)

def ask_agent(user_prompt: str) -> str:
    """Sends the prompt to the agent, allowing it to autonomously trigger tools."""
    response = chat.send_message(user_prompt)
    return response.text