from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Autonomous Bot Schemas
class BotTaskCreate(BaseModel):
    task_type: str
    input_data: Optional[Dict[str, Any]] = None


class BotTaskOut(BaseModel):
    id: int
    task_type: str
    status: str
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class BotWorkflowCreate(BaseModel):
    name: str
    description: str
    workflow_type: str
    steps: List[Dict[str, Any]]


class BotWorkflowOut(BaseModel):
    id: int
    name: str
    description: str
    workflow_type: str
    steps: List[Dict[str, Any]]
    is_active: bool
    success_count: int
    failure_count: int
    created_at: datetime

    class Config:
        orm_mode = True


class BotStatusOut(BaseModel):
    status: str
    message: str
    active_workflows: int
    total_tasks: int
    pending_tasks: int
    running_tasks: int
    completed_tasks: int
    failed_tasks: int

