from pydantic import BaseModel

class KnowledgeAnswer(BaseModel):
    question: str
    answer: str
    source: str

class QuestionRequest(BaseModel):
    question: str