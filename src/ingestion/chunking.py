from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for doc in documents:
        texts = splitter.split_text(doc["text"])
        for i, chunk in enumerate(texts):
            chunks.append({
                "text": chunk,
                "source": doc["source"],
                "page": doc["page"],
                "chunk_id": f'{doc["source"]}_{i}'
            })

    return chunks