
import re


def classify_question_details(question):

    question = question.lower().strip()

    score = 0
    reasons = []

    # 1. Detect technical concepts
    technical_keywords = [
        "machine learning", "deep learning",
        "neural network", "artificial intelligence",
        "architecture", "database",
        "microcontroller", "optimization",
        "algorithm", "scalability",
        "quantum computing", "data structure"
    ]

    if any(word in question for word in technical_keywords):
        score += 2
        reasons.append("Technical concepts detected")

    # 2. Detect coding requirements
    coding_keywords = [
        "write code", "debug", "implement",
        "program", "python", "java",
        "function", "code", "algorithm",
        "error", "fix this"
    ]

    if any(word in question for word in coding_keywords):
        score += 2
        reasons.append("Programming or coding requirement detected")

    # 3. Detect analytical and reasoning tasks
    reasoning_keywords = [
        "analyze", "evaluate", "compare",
        "optimize", "justify", "critique",
        "design", "synthesize", "architecture",
        "differentiate", "assess", "investigate"
    ]

    if any(word in question for word in reasoning_keywords):
        score += 2
        reasons.append("Advanced reasoning or analysis detected")

    # 4. Detect multi-step requirements
    multi_step_keywords = [
        "step by step", "in detail",
        "with examples", "explain why",
        "pros and cons", "advantages and disadvantages"
    ]

    if any(word in question for word in multi_step_keywords):
        score += 1
        reasons.append("Detailed explanation requested")

    # 5. Consider question length
    if len(question) > 180:
        score += 1
        reasons.append("Long question detected")

    if len(question) > 350:
        score += 1

    # 6. Classify question
    if score <= 1 and len(question) < 80:
        complexity = "simple"
        confidence = 85 + (1 - score) * 5

    elif score <= 3:
        complexity = "medium"
        confidence = 80 + (score - 2) * 5

    else:
        complexity = "complex"
        confidence = min(95, 80 + (score - 4) * 5)

    # 7. Generate explanation
    if not reasons:
        reasons.append("Basic question with low technical complexity")

    return {
        "complexity": complexity,
        "score": score,
        "confidence": min(95, confidence),
        "reason": ", ".join(reasons)
    }


# Keep compatibility with the existing router
def classify_question(question):

    result = classify_question_details(question)

    return result["complexity"]
