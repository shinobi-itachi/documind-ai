from src.pipeline.rag_pipeline import run_pipeline

query = "What is maternity leave policy?"

print("Running end-to-end pipeline...\n")

result = run_pipeline(query)

print("FINAL ANSWER:\n")
print(result["answer"])

print("\nCONFIDENCE:")
print(result["confidence"])

print("\nSOURCES:")
for s in result["sources"]:
    print(s)