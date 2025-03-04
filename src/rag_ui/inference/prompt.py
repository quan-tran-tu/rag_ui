def construct_prompt(user_message: str, context: str | None = None) -> list[dict]:
    """
    Constructs and returns a list of messages with a predefined prompt format to pass to an LLM.
    
    Args:
        user_message: The user's question to be answered
        context: Optional context information to answer the question
        
    Returns:
        A list of dictionaries representing the system and user messages
    """
    if context is not None:
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
        """

        user_prompt = f"""
        Based on the information in <context>, answer the question in <question>.

        <context>
        {context}
        </context>

        <question>
        {user_message}
        </question>
        """
    else:
        # General-purpose Q&A prompt (without context)
        system_prompt = """
        You are a helpful AI assistant. Answer questions accurately and concisely.

        - Keep answers brief (ideally 2-6 sentences)
        - Respond in the same language as the user's question
        """

        user_prompt = f"""
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