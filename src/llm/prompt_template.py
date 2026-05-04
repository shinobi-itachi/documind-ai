def build_prompt(query, docs):
    context = "\n\n".join([
        f"[Source: {doc['source']} | Page: {doc['page']}]\n{doc['text']}"
        for doc in docs
    ])

    prompt = f"""
You are an intelligent HR assistant.

Answer ONLY from the given context.
If answer is not present, say "Not found in documents".

Be clear, concise, and structured.

Question:
{query}

Context:
{context}

Answer:
"""
    return prompt