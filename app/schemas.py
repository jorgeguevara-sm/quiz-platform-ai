from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any, Literal
from datetime import datetime

# ---------- Auth ----------
class MagicLinkRequest(BaseModel):
    email: EmailStr

class MagicLinkVerify(BaseModel):
    token: str

class UserOut(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    plan: str

    class Config:
        from_attributes = True

# ---------- Generation (Onboarding -> LLM) ----------
class OnboardingInput(BaseModel):
    professional_name: str
    profession: str
    industry: str
    business_description: str = Field(..., min_length=10)
    test_goal: Literal["calificar_leads", "diagnosticar_necesidades", "evaluar_conocimiento", "recomendar_servicios"]
    language: Literal["es", "en"] = "es"
    num_questions: int = Field(default=8, ge=5, le=15)

class QuestionOption(BaseModel):
    label: str
    value: str
    score: float = 0

class GeneratedQuestion(BaseModel):
    type: Literal["multiple_choice", "yes_no", "scale", "free_text"]
    text: str
    options: List[QuestionOption] = []
    weight: float = 1.0

class GeneratedResult(BaseModel):
    label: str
    min_score: float
    max_score: float
    message: str
    cta_text: Optional[str] = None

class GeneratedTestSchema(BaseModel):
    """Contrato estricto que el LLM debe devolver en JSON."""
    title: str
    industry: str
    language: str
    questions: List[GeneratedQuestion]
    results: List[GeneratedResult]

# ---------- Test CRUD ----------
class BrandingIn(BaseModel):
    business_name: Optional[str] = None
    primary_color: Optional[str] = "#2563eb"
    logo_url: Optional[str] = None

class QuestionOut(BaseModel):
    id: str
    type: str
    text: str
    options: List[Any] = []
    order: int
    weight: float
    logic_rules: List[Any] = []

    class Config:
        from_attributes = True

class ResultOut(BaseModel):
    id: str
    label: str
    min_score: float
    max_score: float
    message: str
    cta_text: Optional[str] = None
    cta_url: Optional[str] = None

    class Config:
        from_attributes = True

class TestOut(BaseModel):
    id: str
    title: str
    industry: Optional[str]
    language: str
    branding: dict
    status: str
    slug: Optional[str]
    questions: List[QuestionOut] = []
    results: List[ResultOut] = []

    class Config:
        from_attributes = True

class TestUpdate(BaseModel):
    title: Optional[str] = None
    branding: Optional[BrandingIn] = None
    status: Optional[Literal["draft", "published"]] = None

class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    type: Optional[str] = None
    options: Optional[List[QuestionOption]] = None
    order: Optional[int] = None
    weight: Optional[float] = None
    logic_rules: Optional[List[Any]] = None

# ---------- Public response submission ----------
class ResponseSubmit(BaseModel):
    respondent_name: Optional[str] = None
    respondent_email: Optional[EmailStr] = None
    respondent_phone: Optional[str] = None
    answers: dict

class ResponseOut(BaseModel):
    id: str
    total_score: float
    result_label: Optional[str]
    completed: bool

    class Config:
        from_attributes = True
