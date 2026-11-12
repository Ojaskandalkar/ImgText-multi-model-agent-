import os
import json
from document_processor import process_file

# In-memory JSON storage
MEMORY_STORE = {}
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_document(file_name: str) -> str:
    """Uploads and processes a document by its file_name. The file must exist in the 'uploads' directory."""
    file_path = os.path.join(UPLOAD_DIR, file_name)
    if not os.path.exists(file_path):
        return f"Error: File {file_name} not found in {UPLOAD_DIR} folder."
    
    try:
        content = process_file(file_path)
        MEMORY_STORE[file_name] = {
            "file_name": file_name,
            "content": content
        }
        return f"Successfully processed and stored {file_name}."
    except Exception as e:
        return f"Failed to process {file_name}: {str(e)}"

def list_documents() -> list[str]:
    """Returns a list of all uploaded and processed document file names."""
    return list(MEMORY_STORE.keys())

def get_document_content(file_name: str) -> str:
    """Returns the full parsed content, text, and image descriptions of a specific document."""
    if file_name not in MEMORY_STORE:
        return f"Error: {file_name} not found in memory."
    return json.dumps(MEMORY_STORE[file_name])

def search_documents(query: str) -> str:
    """Searches all uploaded documents for a specific keyword or query string and returns matching segments."""
    results = []
    for file_name, data in MEMORY_STORE.items():
        for page in data["content"]:
            if query.lower() in page["text"].lower():
                results.append({
                    "file_name": file_name, 
                    "page": page["page"], 
                    "match": page["text"][:300] + "..." # Snippet
                })
    if not results:
        return "No matching information found."
    return json.dumps(results)

def summarize_document(file_name: str = "ALL") -> str:
    """Returns content for summarization. Pass 'ALL' to get all documents, or a specific file_name."""
    if file_name == "ALL":
        return json.dumps(MEMORY_STORE)
    if file_name not in MEMORY_STORE:
        return f"Error: {file_name} not found."
    return json.dumps(MEMORY_STORE[file_name])