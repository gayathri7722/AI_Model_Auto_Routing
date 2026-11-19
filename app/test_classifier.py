
from app.classifier import classify_question_details

questions = [
    "Hi, how are you?",
    "Explain Python loops with examples.",
    "Analyze neural network architecture and optimize its performance.",
    "Write Python code to sort a list.",
    "Compare machine learning and deep learning step by step."
]

for question in questions:

    result = classify_question_details(question)

    print("\nQuestion:", question)
    print("Complexity:", result["complexity"].upper())
    print("Score:", result["score"])
    print("Confidence:", str(result["confidence"]) + "%")
    print("Reason:", result["reason"])
    print("-" * 60)
