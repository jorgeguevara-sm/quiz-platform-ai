import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON, Integer, Float
from sqlalchemy.orm import relationship
from app.database import Base

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    plan = Column(String, default="free")  # free | pay_per_use | subscription
    stripe_customer_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    tests = relationship("Test", back_populates="owner", cascade="all, delete-orphan")

class MagicLinkToken(Base):
    __tablename__ = "magic_link_tokens"
    id = Column(String, primary_key=True, default=gen_uuid)
    email = Column(String, index=True, nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

class Test(Base):
    __tablename__ = "tests"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    industry = Column(String, nullable=True)
    original_prompt = Column(String, nullable=True)
    language = Column(String, default="es")
    branding = Column(JSON, default=dict)
    status = Column(String, default="draft")  # draft | published
    slug = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="tests")
    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan", order_by="Question.order")
    results = relationship("ResultTemplate", back_populates="test", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="test", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True, default=gen_uuid)
    test_id = Column(String, ForeignKey("tests.id"), nullable=False)
    type = Column(String, nullable=False)  # multiple_choice | yes_no | scale | free_text
    text = Column(String, nullable=False)
    options = Column(JSON, default=list)
    order = Column(Integer, default=0)
    weight = Column(Float, default=1.0)
    logic_rules = Column(JSON, default=list)
    test = relationship("Test", back_populates="questions")

class ResultTemplate(Base):
    __tablename__ = "result_templates"
    id = Column(String, primary_key=True, default=gen_uuid)
    test_id = Column(String, ForeignKey("tests.id"), nullable=False)
    label = Column(String, nullable=False)
    min_score = Column(Float, default=0)
    max_score = Column(Float, default=100)
    message = Column(String, nullable=False)
    cta_text = Column(String, nullable=True)
    cta_url = Column(String, nullable=True)
    test = relationship("Test", back_populates="results")

class Response(Base):
    __tablename__ = "responses"
    id = Column(String, primary_key=True, default=gen_uuid)
    test_id = Column(String, ForeignKey("tests.id"), nullable=False)
    respondent_name = Column(String, nullable=True)
    respondent_email = Column(String, nullable=True)
    respondent_phone = Column(String, nullable=True)
    answers = Column(JSON, default=dict)
    total_score = Column(Float, default=0)
    result_label = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    test = relationship("Test", back_populates="responses")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    stripe_subscription_id = Column(String, nullable=True)
    status = Column(String, default="inactive")  # active | canceled | inactive
    plan = Column(String, default="subscription")
    created_at = Column(DateTime, default=datetime.utcnow)
