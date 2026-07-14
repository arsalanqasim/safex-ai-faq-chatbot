# ==============================================================================
# SafeX AI FAQ Chatbot - Performance Evaluation Benchmark
# ==============================================================================
import json
import sys
import time
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.chatbot import FAQChatbot
from src.config import FAQ_PATH, TEST_QUESTIONS_PATH, DEFAULT_THRESHOLD

def run_benchmarks():
    print("=" * 70)
    print(" SafeX AI FAQ Chatbot - Benchmark Evaluation Running...")
    print("=" * 70)
    
    if not TEST_QUESTIONS_PATH.exists():
        print(f"ERROR: Test questions dataset not found at {TEST_QUESTIONS_PATH}")
        sys.exit(1)
        
    # Initialize chatbot
    print(f"Initializing chatbot with FAQ database: {FAQ_PATH.name}...")
    chatbot = FAQChatbot(FAQ_PATH)
    print(f"Chatbot ready. Loaded {len(chatbot.faq_data)} FAQ entries.")
    
    # Load evaluation questions
    with open(TEST_QUESTIONS_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
        
    print(f"Loaded {len(test_cases)} evaluation test cases.")
    
    positive_count = 0
    positive_correct = 0
    negative_count = 0
    negative_correct = 0
    total_latency_ms = 0.0
    
    failures = []
    
    for idx, case in enumerate(test_cases):
        query_text = case["input"]
        expected_id = case["expected_answer_id"]
        
        # Determine case category
        is_positive = (expected_id is not None)
        if is_positive:
            positive_count += 1
        else:
            negative_count += 1
            
        # Query chatbot
        res = chatbot.query(query_text, threshold=DEFAULT_THRESHOLD)
        total_latency_ms += res["latency_ms"]
        
        # Check correctness
        if is_positive:
            # For positive queries, we want:
            # 1. Not fallback
            # 2. Retrieved ID matches expected ID
            retrieved_id = res["expected_answer_id"]
            if not res["is_fallback"] and retrieved_id == expected_id:
                positive_correct += 1
            else:
                failures.append({
                    "type": "Positive Misclassification / Fallback",
                    "query": query_text,
                    "expected_id": expected_id,
                    "retrieved_id": retrieved_id,
                    "score": res["similarity_score"],
                    "is_fallback": res["is_fallback"]
                })
        else:
            # For negative queries, we want fallback to trigger
            if res["is_fallback"]:
                negative_correct += 1
            else:
                failures.append({
                    "type": "False Positive (Should have triggered fallback)",
                    "query": query_text,
                    "expected_id": None,
                    "retrieved_id": res["expected_answer_id"],
                    "score": res["similarity_score"],
                    "is_fallback": res["is_fallback"]
                })
                
    total_cases = len(test_cases)
    avg_latency = total_latency_ms / total_cases if total_cases > 0 else 0
    
    pos_accuracy = (positive_correct / positive_count * 100.0) if positive_count > 0 else 0
    neg_accuracy = (negative_correct / negative_count * 100.0) if negative_count > 0 else 0
    overall_accuracy = ((positive_correct + negative_correct) / total_cases * 100.0) if total_cases > 0 else 0
    
    print("\n" + "=" * 70)
    print(" EVALUATION RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total Test Cases Run:   {total_cases}")
    print(f"Positive Test Cases:    {positive_count} (Correct: {positive_correct})")
    print(f"Negative Test Cases:    {negative_count} (Correct: {negative_correct})")
    print("-" * 70)
    print(f"Retrieval Accuracy:     {pos_accuracy:.2f}%")
    print(f"Fallback Success Rate:  {neg_accuracy:.2f}%")
    print(f"Overall Accuracy:       {overall_accuracy:.2f}%")
    print(f"Average Response Time:  {avg_latency:.2f} ms")
    print("=" * 70 + "\n")
    
    if failures:
        print(f"Found {len(failures)} failures/mismatches. Top 5 mismatches:")
        for f in failures[:5]:
            print(f"- Type: {f['type']}")
            print(f"  Query:      '{f['query']}'")
            print(f"  Expected:   {f['expected_id']}")
            print(f"  Retrieved:  {f['retrieved_id']} (Score: {f['score']:.4f}, Fallback: {f['is_fallback']})")
            print()
            
    # Output markdown table for docs
    print("Markdown Table for Case Study:")
    print("| Evaluation Metric | Target Value | Achieved Value | Target Met? |")
    print("| :--- | :--- | :--- | :--- |")
    print(f"| **Retrieval Accuracy** | &ge; 90% | {pos_accuracy:.2f}% | {'Yes' if pos_accuracy >= 90 else 'No'} |")
    print(f"| **Response Latency** | &lt; 50ms | {avg_latency:.2f}ms | {'Yes' if avg_latency < 50 else 'No'} |")
    print(f"| **Fallback Success Rate** | &ge; 95% | {neg_accuracy:.2f}% | {'Yes' if neg_accuracy >= 95 else 'No'} |")
    print()

if __name__ == "__main__":
    run_benchmarks()
