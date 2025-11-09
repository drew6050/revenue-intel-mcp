"""
Data models for the Revenue Intelligence MCP server.
Uses dataclasses with type hints for production-ready code.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any


@dataclass
class UsageSignals:
    """Usage metrics for an account."""
    daily_active_users: int
    features_adopted: int
    api_calls_per_day: int
    support_tickets_30d: int = 0
    nps_score: Optional[int] = None
    login_frequency_7d: int = 0


@dataclass
class Account:
    """Customer account model with business metrics."""
    id: str
    company: str
    plan: str  # trial, starter, professional, enterprise
    mrr: float
    created_date: str
    usage_signals: Dict[str, Any]
    industry: str = "technology"
    status: str = "active"  # active, trial, at_risk, churned

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "company": self.company,
            "plan": self.plan,
            "mrr": self.mrr,
            "created_date": self.created_date,
            "usage_signals": self.usage_signals,
            "industry": self.industry,
            "status": self.status
        }


@dataclass
class LeadSignals:
    """Engagement signals for a lead."""
    website_visits_30d: int
    demo_requested: bool
    whitepaper_downloads: int
    email_engagement_score: float  # 0-100
    linkedin_engagement: bool = False
    free_trial_started: bool = False


@dataclass
class Lead:
    """Potential customer lead model."""
    id: str
    company: str
    industry: str
    employee_count: int
    signals: Dict[str, Any]
    contact_name: str = "Unknown"
    contact_title: str = "Unknown"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "company": self.company,
            "industry": self.industry,
            "employee_count": self.employee_count,
            "signals": self.signals,
            "contact_name": self.contact_name,
            "contact_title": self.contact_title
        }


@dataclass
class FeatureAttribution:
    """Explains which features contributed to a prediction."""
    feature_name: str
    contribution: float  # Percentage contribution to final score
    value: Any
    impact: str  # positive, negative, neutral


@dataclass
class PredictionResult:
    """Result from a lead scoring prediction."""
    score: float  # 0-100
    tier: str  # hot, warm, cold
    feature_attributions: List[Dict[str, Any]]
    explanation: str
    model_version: str
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "score": self.score,
            "tier": self.tier,
            "feature_attributions": self.feature_attributions,
            "explanation": self.explanation,
            "model_version": self.model_version,
            "timestamp": self.timestamp
        }


@dataclass
class PredictionLog:
    """Log entry for a prediction, used for monitoring and drift detection."""
    log_id: str
    timestamp: str
    prediction_type: str  # lead_score, churn_risk, conversion_probability
    input_data: Dict[str, Any]
    prediction_result: Dict[str, Any]
    model_version: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "log_id": self.log_id,
            "timestamp": self.timestamp,
            "prediction_type": self.prediction_type,
            "input_data": self.input_data,
            "prediction_result": self.prediction_result,
            "model_version": self.model_version
        }


@dataclass
class ModelMetadata:
    """Metadata about the ML model."""
    model_version: str
    training_date: str
    performance_metrics: Dict[str, float]
    feature_importance: Dict[str, float]
    drift_status: str  # normal, warning, critical

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "model_version": self.model_version,
            "training_date": self.training_date,
            "performance_metrics": self.performance_metrics,
            "feature_importance": self.feature_importance,
            "drift_status": self.drift_status
        }
