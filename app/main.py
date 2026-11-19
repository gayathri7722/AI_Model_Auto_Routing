
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.router import route_question
from app.classifier import classify_question_details
from app.model_handler import generate_response

app = FastAPI(
    title="AI Model Auto-Routing",
    description="Intelligent AI Model Selection System",
    version="2.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Model Auto-Routing API is running!",
        "version": "2.0"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Analyze question complexity
    classification = classify_question_details(question)

    # Select appropriate AI model
    routing_info = route_question(question)

    # Generate AI response
    answer = generate_response(
        question,
        routing_info["selected_model"]
    )

    return {
        "question": question,
        "complexity": classification["complexity"],
        "complexity_score": classification["score"],
        "confidence": classification["confidence"],
        "reason": classification["reason"],
        "selected_model": routing_info["selected_model"],
        "answer": answer
    }
