"""
Quick test script using SimpleQA (no LLM download required)
"""

from vector_store import VectorStore
from llm_qa import SimpleQA
import config

def main():
    print("\n" + "="*70)
    print("QUICK SYSTEM TEST - Multi-Modal RAG")
    print("="*70 + "\n")
    
    # Load vector store
    print("Loading vector store...")
    vector_store = VectorStore(model_name=config.EMBEDDING_MODEL)
    vector_store.load(config.VECTOR_STORE_PATH)
    
    print(f"✓ Loaded {len(vector_store.chunks)} chunks")
    print(f"  - Text: {sum(1 for c in vector_store.chunks if c['type'] == 'text')}")
    print(f"  - Tables: {sum(1 for c in vector_store.chunks if c['type'] == 'table')}")
    print(f"  - Images: {sum(1 for c in vector_store.chunks if c['type'] == 'image')}")
    
    # Test queries
    queries = [
        "What is Qatar's economic growth?",
        "What are the fiscal policy recommendations?",
        "What is the banking sector situation?"
    ]
    
    qa = SimpleQA()
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}: {query}")
        print("="*70)
        
        # Search
        results = vector_store.search(query, k=3)
        print(f"\nTop 3 Results:")
        for j, result in enumerate(results, 1):
            chunk = result['chunk']
            print(f"\n{j}. {chunk['source']} (Type: {chunk['type']}, Score: {result['score']:.4f})")
            print(f"   {chunk['content'][:100]}...")
        
        # Generate answer
        answer_result = qa.generate_answer_with_citations(query, results)
        
        print(f"\n{'─'*70}")
        print("ANSWER:")
        print(answer_result['answer'][:500])
        if len(answer_result['answer']) > 500:
            print("...")
        
        print(f"\n{'─'*70}")
        print("CITATIONS:")
        for citation in answer_result['citations']:
            print(f"  • {citation['source']} (Page {citation['page']}) - {citation['type']}")
    
    print(f"\n{'='*70}")
    print("✓ TEST COMPLETE - System is working!")
    print("="*70)
    print("\nTo use the full system with LLM:")
    print("  streamlit run app.py")

if __name__ == "__main__":
    main()
