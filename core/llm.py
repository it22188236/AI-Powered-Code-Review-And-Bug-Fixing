import ollama

def call_llm(system_prompt: str, user_prompt: str, model="phi3:mini") -> str:
    """Call local Ollama model."""
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response['message']['content']