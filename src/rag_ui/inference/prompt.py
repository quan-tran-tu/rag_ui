def construct_prompt(history: list[str], context: str | None = None) -> list[dict]:
    """
    Constructs and returns a list of messages with a predefined prompt format to pass to an LLM.
    
    Args:
        user_message: The user's question to be answered
        context: Optional context information to answer the question
        
    Returns:
        A list of dictionaries representing the system and user messages
    """
    user_message = history[0]
    if len(history) > 1:
        past_messages = history[1:]
        past_messages_text = "\n".join([f"User: {msg}" for msg in past_messages])
    else:
        past_messages_text = ""
    
    # RAG-based Q&A prompt (with context)
    system_prompt = """
    You are a precise and helpful AI assistant. Your task is to answer questions based on the provided context information. Always prioritize information from the context over your general knowledge.

    Follow these exact guidelines:
    1. If the user wants to summarize content from a url, use the content provided in the context to response the user with a complete summarization;
    Else, keep answers concise (2-6 sentences) and directly address the question
    2. Format your entire response using markdown with MathJax support for equations
    3. For mathematical expressions, use single $ for inline math and double $$ for display math
    4. If the context doesn't contain the answer, state "I don't have enough information to answer this question" and suggest what information would be needed
    5. Structure your response: first provide the direct answer, then support with relevant details
    6. Respond in the same language as the user's question
    
    Do not:
    - Include any introductory phrases like "Based on the context..." or "According to the information provided..."
    - Ask the user for more information
    - Repeat the user's question
    - Mention that you're using context to answer
    - Include any self-references (e.g., "As an AI assistant...")
    """

    user_prompt = f"""
    Based on the information in <context>, answer the question in <question>.
    Use the additional context from <history> if needed if the current user message is too vague.
    <history>
    {past_messages_text}
    </history>
    <context>
    {context}
    </context>
    <question>
    {user_message}
    </question>
    """
    print("user message", user_message)
    print("context", context)
    # Construct the messages list
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    return messages