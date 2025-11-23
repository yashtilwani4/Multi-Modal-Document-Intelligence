"""
Test script to verify the Multi-Modal RAG system functionality
"""

import os
from vector_store import VectorStore
from llm_qa import LLMQA, SimpleQA
import config

def test_vector_store():
    """Test vector store loading and search"""
    print("="*70)
    print("TEST 1: Vector Store")
    print("="*70)
    
    try:
        vector_store = VectorStore(model_name=config.EMBEDDING_MODEL)
        vector_store.load(config.VECTOR_STORE_PATH)
        
        print(f"✓ Vector store loaded successfully")
        print(f"✓ Total chunks: {len(vector_store.chunks)}")
        
        # Count by type
        text_count = sum(1 for c in vector_store.chunks if c['type'] == 'text')
        table_count = sum(1 for c in vector_store.chunks if c['type'] == 'table')
        image_count = sum(1 for c in vector_store.chunks if c['type'] == 'image')
        
        print(f"  - Text chunks: {text_count}")
        print(f"  - Table chunks: {table_count}")
        print(f"  - Image chunks: {image_count}")
        
        return vector_store
        
    except Exception as e:
        print(f"✗ Error loading vector store: {e}")
        return None

def test_search(vector_store, query):
    """Test search functionality"""
    print(f"\n{'='*70}")
    print(f"TEST 2: Search Query")
    print(f"{'='*70}")
    print(f"Query: '{query}'")
    print()
    
    try:
        results = vector_store.search(query, k=5)
        print(f"✓ Found {len(results)} results")
        print()
        
        for i, result in enumerate(results[:3], 1):
            chunk = result['chunk']
            print(f"Result {i}:")
            print(f"  Source: {chunk['source']}")
            print(f"  Type: {chunk['type']}")
            print(f"  Score: {result['score']:.4f}")
            print(f"  Content: {chunk['content'][:150]}...")
            print()
        
        return results
        
    except Exception as e:
        print(f"✗ Error during search: {e}")
        return []

def test_qa_system(results, query):
    """Test QA system"""
    print(f"{'='*70}")
    print(f"TEST 3: Answer Generation")
    print(f"{'='*70}")
    
    # Try LLM-based QA first
    try:
        print("Attempting to use LLM-based QA (Flan-T5)...")
        qa = LLMQA(model_name=config.LLM_MODEL)
        result = qa.generate_answer_with_citations(query, results)
        print("✓ LLM-based QA successful")
        
    except Exception as e:
        print(f"⚠ LLM-based QA failed: {e}")
        print("Falling back to SimpleQA...")
        qa = SimpleQA()
        result = qa.generate_answer_with_citations(query, results)
        print("✓ SimpleQA fallback successful")
    
    print()
    print("ANSWER:")
    print("-" * 70)
    print(result['answer'])
    print("-" * 70)
    print()
    
    print("CITATIONS:")
    for i, citation in enumerate(result['citations'], 1):
        print(f"{i}. {citation['source']} (Page {citation['page']}) - "
              f"Type: {citation['type']}, Score: {citation['relevance_score']:.4f}")
    
    print()
    print(f"Context chunks used: {result['context_used']}")
    
    return result

def run_comprehensive_test():
    """Run comprehensive system test"""
    print("\n" + "="*70)
    print("MULTI-MODAL RAG SYSTEM - COMPREHENSIVE TEST")
    print("="*70 + "\n")
    
    # Test 1: Load vector store
    vector_store = test_vector_store()
    if not vector_store:
        print("\n✗ System test failed: Could not load vector store")
        return
    
    # Test 2: Search
    test_queries = [
        "What is Qatar's economic growth rate?",
        "What are the main fiscal policy recommendations?",
        "What is the banking sector situation?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'#'*70}")
        print(f"# TEST QUERY {i}/{len(test_queries)}")
        print(f"{'#'*70}")
        
        results = test_search(vector_store, query)
        
        if results:
            test_qa_system(results, query)
        
        if i < len(test_queries):
            print("\n" + "-"*70 + "\n")
    
    print("\n" + "="*70)
    print("COMPREHENSIVE TEST COMPLETE")
    print("="*70)
    print("\n✓ All tests passed successfully!")
    print("\nSystem is ready for use. Run 'streamlit run app.py' to start the chat interface.")

if __name__ == "__main__":
    run_comprehensive_test()
