from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Agent:
    id: str
    name: str
    type: str
    location: str
    current_task: str
    xp: int = 0


@dataclass
class Project:
    id: str
    name: str
    status: str
    priority: str
    owner: str
    target_launch: str
    revenue_target: str
    progress: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Opportunity:
    id: str
    title: str
    score: float
    status: str
    description: str


@dataclass
class Decision:
    id: str
    title: str
    description: str
    recommended_by: str
    status: str = "PENDING"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
