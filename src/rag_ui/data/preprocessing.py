from markitdown import MarkItDown

from rag_ui.core.config import EMBEDDING_MAX_TOKENS

def to_text(file_path: str) -> str:
    """
    Read the content of a document as string using markitdown.
    """
    md = MarkItDown()
    result = md.convert(file_path)
    res = result.text_content
    assert res.encode('utf-8') # Ensure the string can be encoded to utf-8 for Ollama
    return res

def to_chunks(text: str) -> list[str]:
    """
    Split the text into chunks of text with a maximum number of tokens.
    """
    chunks = []
    current_chunk = []
    current_estimate_token_count = 0

    sentences = text.split(".")
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence == "":
            continue

        # Considering each word is a token
        estimate_token_count = len([word.strip() for word in sentence.split(" ") if word.strip() != ""])
        if current_estimate_token_count + estimate_token_count <= EMBEDDING_MAX_TOKENS - 1000:
            current_chunk.append(sentence)
            current_estimate_token_count += estimate_token_count
        else:
            chunks.append(".".join(current_chunk))
            current_chunk = [sentence]
            current_estimate_token_count = estimate_token_count
    # Add the last sentence (if any) to it own chunk
    if current_chunk:
        chunks.append(".".join(current_chunk))
    return chunks
