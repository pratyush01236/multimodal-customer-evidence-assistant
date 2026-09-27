from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Evidence:
    source: str
    text: str = ""
    order_id: Optional[str] = None
    date: Optional[str] = None
    amount: Optional[str] = None
    product: Optional[str] = None
    error_codes: list[str] = field(default_factory=list)
    quality: float = 1.0
    safe: bool = True
    rejection_reason: Optional[str] = None

@dataclass
class AnalysisResult:
    status: str
    message: str
    evidence: list[Evidence] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    clarification: list[str] = field(default_factory=list)
    background_job_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
