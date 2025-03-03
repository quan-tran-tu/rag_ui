from markitdown import MarkItDown
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser

from rag_ui.core.config import config

def to_text(file_path: str) -> str:
    """
    Read the content of a document as string using markitdown.
    """
    if file_path.endswith(".pdf"):
        config = {
            "output_format": "markdown",
            "output_dir": "/home/tuquan/rag_ui/src/rag_ui/data/marker-output/"
        }
        config_parser = ConfigParser(config)

        converter = PdfConverter(
            config=config_parser.generate_config_dict(),
            artifact_dict=create_model_dict(),
        )
        rendered = converter(file_path)
        return rendered.markdown
    
    md = MarkItDown()
    result = md.convert(file_path)
    res = result.text_content
    assert res.encode('utf-8') # Ensure the string can be encoded to utf-8 for Ollama
    return res

def to_chunks_words(text: str) -> list[str]:
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
        words = [word.strip() for word in sentence.split(" ") if word.strip() != ""]
        # Check UTF-8
        new_words = [word for word in words if word.encode("utf-8")]
        estimate_token_count = len(new_words)
        if current_estimate_token_count + estimate_token_count <= config.EMBEDDING_MAX_WORDS:
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

def to_chunks_paragraphs(text: str) -> list[str]:
    """
    Chunks a markdown string by paragraphs while preserving header context.
    
    Args:
        text: A markdown string
        
    Returns:
        A list of chunks where each chunk contains a header and a paragraph
    """
    lines = text.strip().split('\n')
    chunks = []
    current_header = ""
    current_chunk = ""
    
    for line in lines:
        # Check if line is a header (starts with #)
        if line.startswith('#'):
            # If we have a chunk in progress, save it first
            if current_chunk:
                chunks.append(f"{current_header}\n{current_chunk}")
                current_chunk = ""
            
            # Update the current header
            current_header = line
        elif line.strip() == '':
            # Empty line indicates a paragraph break
            if current_chunk:
                chunks.append(f"{current_header}\n{current_chunk}")
                current_chunk = ""
        else:
            # If we're starting a new paragraph and don't have a header yet, use empty header
            if not current_header and not current_chunk:
                current_header = ""
            
            # Add line to current chunk
            if current_chunk:
                current_chunk += f"\n{line}"
            else:
                current_chunk = line
    
    # Don't forget to add the last chunk if there is one
    if current_chunk:
        chunks.append(f"{current_header}\n{current_chunk}")
    
    return chunks
