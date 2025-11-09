"""
Configuration management for the Revenue Intelligence MCP server.
Contains model parameters, thresholds, and feature weights.
In production, this would be loaded from environment variables or a config service.
"""

from typing import Dict

# Model versioning
MODEL_VERSION = "v1.2.3"
TRAINING_DATE = "2024-10-15"

# Lead scoring feature weights (must sum to 1.0)
LEAD_SCORE_WEIGHTS: Dict[str, float] = {
    "company_size": 0.20,
    "engagement_signals": 0.40,
    "industry_fit": 0.20,
    "intent_signals": 0.20
}

# Lead tier thresholds
LEAD_TIER_THRESHOLDS = {
    "hot": 70,   # score >= 70
    "warm": 40,  # 40 <= score < 70
    "cold": 0    # score < 40
}

# Churn risk thresholds
CHURN_RISK_THRESHOLDS = {
    "critical": 70,  # risk >= 70
    "high": 50,      # 50 <= risk < 70
    "medium": 30,    # 30 <= risk < 50
    "low": 0         # risk < 30
}

# Conversion probability thresholds (for trial accounts)
CONVERSION_THRESHOLDS = {
    "high": 0.70,   # >= 70% probability
    "medium": 0.40, # 40-70% probability
    "low": 0.0      # < 40% probability
}

# Model performance metrics (from last evaluation)
MODEL_PERFORMANCE_METRICS = {
    "accuracy": 0.89,
    "precision": 0.85,
    "recall": 0.82,
    "f1_score": 0.83,
    "roc_auc": 0.91
}

# Feature importance (from training)
FEATURE_IMPORTANCE = {
    "email_engagement_score": 0.25,
    "website_visits": 0.18,
    "demo_requested": 0.15,
    "employee_count": 0.12,
    "free_trial_started": 0.10,
    "whitepaper_downloads": 0.08,
    "linkedin_engagement": 0.07,
    "industry_fit": 0.05
}

# Industry fit scoring (based on historical conversion rates)
INDUSTRY_FIT_SCORES: Dict[str, int] = {
    "technology": 90,
    "saas": 85,
    "data_analytics": 95,
    "finance": 80,
    "healthcare": 75,
    "insurance": 75,
    "manufacturing": 70,
    "energy": 70,
    "professional_services": 65,
    "education": 60,
    "retail": 55,
    "logistics": 50,
    "real_estate": 45,
    "agriculture": 40,
    "hospitality": 35,
    "nonprofit": 30,
    "default": 50  # fallback for unknown industries
}

# Company size scoring (employee count buckets)
def get_company_size_score(employee_count: int) -> int:
    """Returns a score based on company size."""
    if employee_count >= 1000:
        return 100
    elif employee_count >= 500:
        return 90
    elif employee_count >= 200:
        return 80
    elif employee_count >= 100:
        return 70
    elif employee_count >= 50:
        return 60
    elif employee_count >= 20:
        return 50
    else:
        return 30

# Drift detection parameters
DRIFT_WARNING_THRESHOLD = 0.10  # 10% deviation from baseline
DRIFT_CRITICAL_THRESHOLD = 0.20  # 20% deviation from baseline

# Health monitoring SLOs
SLO_TARGETS = {
    "uptime_percent": 99.9,
    "max_latency_ms": 500,
    "min_accuracy": 0.85,
    "max_drift_percent": 10
}

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
