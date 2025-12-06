from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


# USERS (Admins, Reps, Designers, Installers)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String)
    phone = Column(String)
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
    metadata = Column(JSON)
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
