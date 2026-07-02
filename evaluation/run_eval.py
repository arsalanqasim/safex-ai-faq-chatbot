# ==============================================================================
# SafeX AI FAQ Chatbot - Performance Evaluation Runner
# ==============================================================================
import json
import csv
import sys
from pathlib import Path

# Ensure root directory is on python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import FAQ_PATH, TEST_QUESTIONS_PATH, EVAL_RESULTS_PATH, SIMILARITY_THRESHOLD
from src.chatbot import FAQChatbot

def run_evaluation():
    print("==================================================")
    print("Starting SafeX FAQ Chatbot Evaluation...")
    print("==================================================")
    
    # Check if necessary files exist
    if not FAQ_PATH.exists():
        print(f"Error: FAQ Knowledge Base not found at {FAQ_PATH}")
        sys.exit(1)
    if not TEST_QUESTIONS_PATH.exists():
        print(f"Error: Test Questions JSON not found at {TEST_QUESTIONS_PATH}")
        sys.exit(1)
        
    # Initialize Chatbot
    try:
        chatbot = FAQChatbot(FAQ_PATH)
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        sys.exit(1)
        
    # Load test questions
    with open(TEST_QUESTIONS_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
        
    print(f"Loaded {len(test_cases)} test cases from {TEST_QUESTIONS_PATH.name}")
    print(f"Configured Similarity Threshold: {SIMILARITY_THRESHOLD}")
    print("--------------------------------------------------")
    
    results = []
    passed_count = 0
    total_latency = 0.0
    
    # Run test cases
    for idx, case in enumerate(test_cases):
        q_id = case["id"]
        question = case["question"]
        expected_faq_id = case["expected_faq_id"]
        category = case["category"]
        
        # Query chatbot
        res = chatbot.query(question)
        predicted_faq_id = res["faq_id"]
        score = res["similarity_score"]
        is_fallback = res["is_fallback"]
        answer = res["answer"]
        latency = res["latency_seconds"]
        
        total_latency += latency
        
        # Evaluate PASS/FAIL condition
        if category == "positive":
            # For positive case: must match correct FAQ ID and NOT trigger fallback
            passed = (predicted_faq_id == expected_faq_id) and (not is_fallback)
        else:
            # For negative case: must trigger fallback
            passed = is_fallback
            
        status = "PASS" if passed else "FAIL"
        if passed:
            passed_count += 1
            
        print(f"[{idx+1}/{len(test_cases)}] ID: {q_id} | Type: {category.upper()} | Score: {score:.4f} | Status: {status}")
        
        results.append({
            "Question ID": q_id,
            "Question": question,
            "Category": category,
            "Expected FAQ ID": expected_faq_id,
            "Predicted FAQ ID": "None" if is_fallback else predicted_faq_id,
            "Similarity Score": f"{score:.4f}",
            "Is Fallback": str(is_fallback),
            "Predicted Answer": answer.replace("\n", " "),
            "Evaluation Status": status,
            "Latency (ms)": f"{latency * 1000:.2f}"
        })
        
    # Write results to CSV
    fields = [
        "Question ID", "Question", "Category", "Expected FAQ ID", 
        "Predicted FAQ ID", "Similarity Score", "Is Fallback", 
        "Predicted Answer", "Evaluation Status", "Latency (ms)"
    ]
    
    with open(EVAL_RESULTS_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
        
    # Calculate statistics
    total_cases = len(test_cases)
    accuracy = (passed_count / total_cases) * 100 if total_cases > 0 else 0.0
    avg_latency = (total_latency / total_cases) * 1000 if total_cases > 0 else 0.0
    
    print("--------------------------------------------------")
    print("Evaluation Complete!")
    print(f"Results written to: {EVAL_RESULTS_PATH}")
    print(f"Total Test Cases: {total_cases}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {total_cases - passed_count}")
    print(f"System Accuracy: {accuracy:.2f}%")
    print(f"Average Latency: {avg_latency:.2f} ms")
    print("==================================================")

if __name__ == "__main__":
    run_evaluation()
