
from app.classifier import classify_question


def route_question(question):
    # Identify question complexity
    complexity = classify_question(question)

    # Select model based on complexity
    if complexity == "simple":
        model = "openai/gpt-oss-20b"

    elif complexity == "medium":
        model = "openai/gpt-oss-20b"

    else:
        model = "openai/gpt-oss-120b"

    return {
        "question": question,
        "complexity": complexity,
        "selected_model": model
    }
