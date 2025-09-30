from fastapi import APIRouter, Depends, HTTPException, Request

from app import schemas
from app.services.knowledge_service import KnowledgeService

router = APIRouter()


@router.post("/answer", response_model=schemas.KnowledgeAnswer)
def get_knowledge_answer(req: Request, request_data: schemas.QuestionRequest):
    """
    Answers a question by searching the knowledge base.
    """
    knowledge_service = req.app.state.knowledge_service
    if knowledge_service is None:
        raise HTTPException(
            status_code=503,
            detail="KnowledgeService is not available. Ensure OPENAI_API_KEY is set and vector store is built.",
        )

    result = knowledge_service.answer_question(request_data.question)
    return schemas.KnowledgeAnswer(
        question=request_data.question,
        answer=result["answer"],
        source=result["source"],
    )