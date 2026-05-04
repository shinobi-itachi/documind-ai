def generate_multi_queries(query):
    queries = [
        query,
        f"Explain {query}",
        f"What does the policy say about {query}?",
        f"Details regarding {query}",
        f"Information about {query}"
    ]

    return list(set(queries))