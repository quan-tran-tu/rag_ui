def construct_prompt(user_message: str, context: str | None = None) -> list[dict]:
    """
    Return a list of messages with predefined prompt format to pass to Ollama
    """
    
    if context is not None:
        # Define system and user prompts
        SYSTEM_PROMPT = """
        Human: 
        You are an AI assistant. 
        You are able to find answers to the questions from the contextual passage snippets provided. 
        Try to answer as precise and short as possible. Ideally under 6 sentences.
        """
        USER_PROMPT = f"""
        Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
        <context>
        {context}
        </context>
        <question>
        {user_message}
        </question>
        """
    else:
        SYSTEM_PROMPT = """
        Human: 
        You are an AI assistant. 
        You will decided if it is necessary to use tools to answer the question.
        Try to answer as precise and short as possible. Ideally under 6 sentences.
        """
        USER_PROMPT = f"""
        <question>
        {user_message}
        </question>
        """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ]
    return messages