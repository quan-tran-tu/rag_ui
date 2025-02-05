import os

UPLOAD_FOLDER = "./src/rag_ui/data/documents/"

def save_uploaded_file(file_content, filename):
    """Saves uploaded file to the specified directory."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    return file_path

def get_latest_user_message(conversation) -> str:
    """
    Get the latest user message in the conversation list.
    """
    l = len(conversation)
    while l > 0:
        l -= 1
        if conversation[l]["role"] == "user":
            return conversation[l]["content"]
    return ""


