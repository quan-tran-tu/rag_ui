def construct_prompt(history: list[str], context: str | None = None) -> list[dict]:
    """
    Constructs and returns a list of messages with a predefined prompt format to pass to an LLM.
    
    Args:
        user_message: The user's question to be answered
        context: Optional context information to answer the question
        
    Returns:
        A list of dictionaries representing the system and user messages
    """
    user_message = history[-1]
    past_messages = history[:-1]
    past_messages_text = "\n".join([f"User: {msg}" for msg in past_messages])
    
    # RAG-based Q&A prompt (with context)
    system_prompt = """
    You are a precise and helpful AI assistant. Your task is to answer questions based on the provided context information. Always prioritize information from the context over your general knowledge.

    - Keep answers concise (2-6 sentences) and directly address the question
    - Format your entire response using markdown with MathJax support for equations
    - For mathematical expressions, use single $ for inline math and double $$ for display math
    - Write Latex expression in MathJax format
    - If the context doesn't contain the answer, acknowledge this limitation
    - Structure your response: first provide the direct answer, then support with relevant details
    - Respond in the same language as the user's question
    - Never ask the user for more information
    """

    user_prompt = f"""
    Based on the information in <context>, answer the question in <question>.
    Use the additional context from <history> if needed if the current user message is too vague.
    Conversation history:
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

    # Construct the messages list
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    return messages