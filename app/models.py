from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

# USERS (Admins, Reps, Designers, Installers)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# LEADS
class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    status = Column(String, default="new")
    assigned_to = Column(Integer, ForeignKey("users.id"))
    source = Column(String)
    notes = Column(Text)
    ai_score = Column(Integer)
    ai_notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    rep = relationship("User")


# CUSTOMERS
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    utility_bill = Column(Numeric)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# PROJECTS (OpenSolar Sync)
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    opensolar_id = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    system_size_kw = Column(Numeric)
    proposal_status = Column(String)
    design_status = Column(String)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    last_synced = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    customer = relationship("Customer")


# DESIGNS
class Design(Base):
    __tablename__ = "designs"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    version = Column(Integer)
    design_metadata = Column(JSON)
    ai_notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


# PROPOSALS
class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    pdf_url = Column(String)
    pricing = Column(JSON)
    margin = Column(Numeric)
    ai_notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


# BAULIVER ACTION LOGS
class BauliverLog(Base):
    __tablename__ = "bauliver_logs"

    id = Column(Integer, primary_key=True)
    action_type = Column(String)
    details = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())


# AUTONOMOUS BOT TASKS
class BotTask(Base):
    __tablename__ = "bot_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String)  # e.g., "permit_processing", "project_automation", "workflow_execution"
    status = Column(String, default="pending")  # pending, running, completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    creator = relationship("User")


# AUTONOMOUS BOT WORKFLOWS
class BotWorkflow(Base):
    __tablename__ = "bot_workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    workflow_type = Column(String)  # e.g., "permit_automation", "inspection_scheduling"
    steps = Column(JSON)  # Workflow steps configuration
    is_active = Column(Boolean, default=True)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
