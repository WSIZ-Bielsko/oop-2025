from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class CompletionChoice(BaseModel):
    message: Message
    finish_reason: Literal["stop", "length"]


class UsageStats(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = None
    temperature: float = 0.2
    top_p: float = 0.9
    search_domain_filter: Optional[List[str]] = None
    return_images: bool = False
    return_related_questions: bool = False
    search_recency_filter: Optional[str] = None
    top_k: int = 0
    stream: bool = False
    presence_penalty: float = 0
    frequency_penalty: float = 1
    response_format: Optional[dict] = None


class ChatCompletionResponse(BaseModel):
    id: str
    object: Literal["chat.completion"]
    created: int
    model: str
    choices: List[CompletionChoice]
    usage: UsageStats
