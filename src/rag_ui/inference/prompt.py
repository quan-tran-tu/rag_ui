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
        - ALWAYS format your entire response using markdown with MathJax support for equations
        - Ensure ALL mathematical expressions are properly enclosed in MathJax delimiters (e.g., $...$ for inline math or $$...$$) for proper rendering
        - Properly escape all special characters and subscripts in mathematical expressions
        - Ensure curly braces {} are properly used for grouping in subscripts and superscripts
        - If the context doesn't contain the answer, acknowledge this limitation
        - Structure your response: first provide the direct answer, then support with relevant details
        - Cite specific parts of the context when applicable
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

        First, identify the key information needed to answer the question.
        Then, provide a clear and concise response strictly based on the context provided.
        Format your entire answer in markdown with MathJax support.
        IMPORTANT: 
        - Ensure ALL mathematical expressions are properly enclosed in MathJax delimiters ($...$ for inline math or $$...$$).
        - When writing mathematical expressions, properly escape all subscripts and superscripts using curly braces.
        - For example, write "\\\\mathbb{{E}}_{{{{\\\\mathbf{{x}} \\\\sim p_{{\\\\text{{data}}}}}}}}" instead of "\\\\mathbb{{E}}_{{\\\\mathbf{{x}}\\\\sim p_{{\\\\text{{data}}}}}}"
        - Always check that curly braces are properly balanced and escaped in LaTeX expressions.
        Respond in the same language as the question.
        """
    else:
        # General-purpose Q&A prompt (without context)
        system_prompt = """
        You are a helpful AI assistant. Answer questions accurately and concisely.

        - Keep answers brief (ideally 2-6 sentences)
        - Format responses in markdown with MathJax support for equations
        - Ensure ALL mathematical expressions use proper MathJax delimiters ($...$ for inline, $$...$$)
        - When using math, properly escape all subscripts and superscripts with curly braces
        - Respond in the same language as the user's question
        """

        user_prompt = f"""
        <question>
        {user_message}
        </question>

        Provide a clear and helpful response to this question.
        """

    # Construct the messages list
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    return messages