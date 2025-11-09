"""
ML scoring logic for the Revenue Intelligence MCP server.
Implements lead scoring, churn detection, and conversion prediction.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Tuple

from config import (
    MODEL_VERSION,
    LEAD_SCORE_WEIGHTS,
    LEAD_TIER_THRESHOLDS,
    CHURN_RISK_THRESHOLDS,
    CONVERSION_THRESHOLDS,
    INDUSTRY_FIT_SCORES,
    get_company_size_score
)
from models import PredictionResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def calculate_engagement_score(signals: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]]]:
    """
    Calculate engagement score based on lead signals.

    Args:
        signals: Dictionary of engagement signals

    Returns:
        Tuple of (score, feature_attributions)
    """
    attributions = []

    # Website visits (0-100 scale, cap at 50 visits = 100)
    website_visits = signals.get("website_visits_30d", 0)
    website_score = min(100, (website_visits / 50) * 100)
    attributions.append({
        "feature_name": "website_visits_30d",
        "contribution": 25.0,
        "value": website_visits,
        "impact": "positive" if website_visits > 20 else "neutral"
    })

    # Email engagement (0-100 scale)
    email_score = signals.get("email_engagement_score", 0)
    attributions.append({
        "feature_name": "email_engagement_score",
        "contribution": 30.0,
        "value": email_score,
        "impact": "positive" if email_score > 60 else "neutral"
    })

    # Demo requested (binary, worth 20 points)
    demo_requested = signals.get("demo_requested", False)
    demo_score = 100 if demo_requested else 0
    attributions.append({
        "feature_name": "demo_requested",
        "contribution": 20.0,
        "value": demo_requested,
        "impact": "positive" if demo_requested else "negative"
    })

    # Free trial started (binary, worth 15 points)
    trial_started = signals.get("free_trial_started", False)
    trial_score = 100 if trial_started else 0
    attributions.append({
        "feature_name": "free_trial_started",
        "contribution": 15.0,
        "value": trial_started,
        "impact": "positive" if trial_started else "neutral"
    })

    # Whitepaper downloads (cap at 5 = 100)
    whitepaper_downloads = signals.get("whitepaper_downloads", 0)
    whitepaper_score = min(100, (whitepaper_downloads / 5) * 100)
    attributions.append({
        "feature_name": "whitepaper_downloads",
        "contribution": 10.0,
        "value": whitepaper_downloads,
        "impact": "positive" if whitepaper_downloads > 2 else "neutral"
    })

    # Calculate weighted average
    total_score = (
        website_score * 0.25 +
        email_score * 0.30 +
        demo_score * 0.20 +
        trial_score * 0.15 +
        whitepaper_score * 0.10
    )

    return total_score, attributions


def calculate_intent_score(signals: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]]]:
    """
    Calculate intent/buying signal score.

    Args:
        signals: Dictionary of intent signals

    Returns:
        Tuple of (score, feature_attributions)
    """
    attributions = []

    # LinkedIn engagement (binary)
    linkedin = signals.get("linkedin_engagement", False)
    linkedin_score = 100 if linkedin else 40
    attributions.append({
        "feature_name": "linkedin_engagement",
        "contribution": 100.0,
        "value": linkedin,
        "impact": "positive" if linkedin else "neutral"
    })

    return linkedin_score, attributions


def score_lead(
    company_name: str,
    signals: Dict[str, Any],
    industry: str = "technology",
    employee_count: int = 100
) -> Dict[str, Any]:
    """
    Score a lead based on company attributes and engagement signals.

    Args:
        company_name: Name of the company
        signals: Dictionary of engagement/intent signals
        industry: Company industry
        employee_count: Number of employees

    Returns:
        Dictionary containing score, tier, attributions, and explanation
    """
    logger.info(f"Scoring lead: {company_name} ({industry}, {employee_count} employees)")

    all_attributions = []

    # 1. Company size score (20% weight)
    company_size_score = get_company_size_score(employee_count)
    all_attributions.append({
        "feature_name": "company_size",
        "contribution": LEAD_SCORE_WEIGHTS["company_size"] * 100,
        "value": employee_count,
        "impact": "positive" if company_size_score > 70 else "neutral"
    })

    # 2. Engagement signals (40% weight)
    engagement_score, engagement_attrs = calculate_engagement_score(signals)
    for attr in engagement_attrs:
        # Scale contribution by weight
        attr["contribution"] = attr["contribution"] * LEAD_SCORE_WEIGHTS["engagement_signals"]
        all_attributions.append(attr)

    # 3. Industry fit (20% weight)
    industry_score = INDUSTRY_FIT_SCORES.get(industry, INDUSTRY_FIT_SCORES["default"])
    all_attributions.append({
        "feature_name": "industry_fit",
        "contribution": LEAD_SCORE_WEIGHTS["industry_fit"] * 100,
        "value": industry,
        "impact": "positive" if industry_score > 70 else "neutral"
    })

    # 4. Intent signals (20% weight)
    intent_score, intent_attrs = calculate_intent_score(signals)
    for attr in intent_attrs:
        attr["contribution"] = attr["contribution"] * LEAD_SCORE_WEIGHTS["intent_signals"]
        all_attributions.append(attr)

    # Calculate final weighted score
    final_score = (
        company_size_score * LEAD_SCORE_WEIGHTS["company_size"] +
        engagement_score * LEAD_SCORE_WEIGHTS["engagement_signals"] +
        industry_score * LEAD_SCORE_WEIGHTS["industry_fit"] +
        intent_score * LEAD_SCORE_WEIGHTS["intent_signals"]
    )

    # Determine tier
    if final_score >= LEAD_TIER_THRESHOLDS["hot"]:
        tier = "hot"
    elif final_score >= LEAD_TIER_THRESHOLDS["warm"]:
        tier = "warm"
    else:
        tier = "cold"

    # Generate explanation
    explanation = generate_lead_explanation(
        company_name, final_score, tier, signals, industry, employee_count
    )

    logger.info(f"Lead scored: {company_name} = {final_score:.1f} ({tier})")

    return {
        "score": round(final_score, 2),
        "tier": tier,
        "feature_attributions": all_attributions,
        "explanation": explanation,
        "model_version": MODEL_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def generate_lead_explanation(
    company_name: str,
    score: float,
    tier: str,
    signals: Dict[str, Any],
    industry: str,
    employee_count: int
) -> str:
    """Generate human-readable explanation for lead score."""

    explanation_parts = [
        f"{company_name} scored {score:.1f}/100 ({tier} tier)."
    ]

    # Key positive signals
    positives = []
    if signals.get("demo_requested"):
        positives.append("demo requested")
    if signals.get("free_trial_started"):
        positives.append("free trial started")
    if signals.get("email_engagement_score", 0) > 70:
        positives.append("high email engagement")
    if employee_count >= 500:
        positives.append("enterprise size")

    if positives:
        explanation_parts.append(f" Strong signals: {', '.join(positives)}.")

    # Areas for improvement
    concerns = []
    if signals.get("website_visits_30d", 0) < 10:
        concerns.append("low website engagement")
    if not signals.get("demo_requested"):
        concerns.append("no demo requested")
    if employee_count < 50:
        concerns.append("small company size")

    if concerns and tier != "hot":
        explanation_parts.append(f" Areas to improve: {', '.join(concerns)}.")

    return "".join(explanation_parts)


def detect_churn_risk(account_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate churn risk for an existing account.

    Args:
        account_data: Account dictionary with usage signals

    Returns:
        Dictionary with risk score, tier, declining signals, and interventions
    """
    company = account_data["company"]
    usage = account_data["usage_signals"]

    logger.info(f"Calculating churn risk for: {company}")

    risk_factors = []
    risk_score = 0.0

    # Factor 1: Low daily active users relative to expected
    dau = usage.get("daily_active_users", 0)
    if dau < 5:
        risk_score += 30
        risk_factors.append("Very low daily active users")
    elif dau < 10:
        risk_score += 15
        risk_factors.append("Low daily active users")

    # Factor 2: Poor NPS score
    nps = usage.get("nps_score")
    if nps is not None:
        if nps <= 4:
            risk_score += 25
            risk_factors.append("Low NPS score (detractor)")
        elif nps <= 6:
            risk_score += 10
            risk_factors.append("Below-average NPS")

    # Factor 3: High support ticket volume
    support_tickets = usage.get("support_tickets_30d", 0)
    if support_tickets > 5:
        risk_score += 20
        risk_factors.append("High support ticket volume")
    elif support_tickets > 3:
        risk_score += 10
        risk_factors.append("Elevated support tickets")

    # Factor 4: Declining login frequency
    login_freq = usage.get("login_frequency_7d", 0)
    if login_freq < 5:
        risk_score += 15
        risk_factors.append("Declining login frequency")

    # Factor 5: Low feature adoption
    features_adopted = usage.get("features_adopted", 0)
    if features_adopted < 3:
        risk_score += 10
        risk_factors.append("Low feature adoption")

    # Determine risk tier
    if risk_score >= CHURN_RISK_THRESHOLDS["critical"]:
        risk_tier = "critical"
    elif risk_score >= CHURN_RISK_THRESHOLDS["high"]:
        risk_tier = "high"
    elif risk_score >= CHURN_RISK_THRESHOLDS["medium"]:
        risk_tier = "medium"
    else:
        risk_tier = "low"

    # Generate intervention suggestions
    interventions = generate_intervention_suggestions(risk_factors, account_data)

    logger.info(f"Churn risk calculated: {company} = {risk_score:.1f} ({risk_tier})")

    return {
        "account_id": account_data["id"],
        "company": company,
        "risk_score": round(risk_score, 2),
        "risk_tier": risk_tier,
        "declining_signals": risk_factors,
        "suggested_interventions": interventions,
        "model_version": MODEL_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def generate_intervention_suggestions(
    risk_factors: List[str],
    account_data: Dict[str, Any]
) -> List[str]:
    """Generate suggested interventions based on risk factors."""

    interventions = []

    for factor in risk_factors:
        if "NPS" in factor or "support ticket" in factor:
            interventions.append("Schedule executive business review to address concerns")
        if "daily active" in factor or "login" in factor:
            interventions.append("Provide personalized onboarding/training session")
        if "feature adoption" in factor:
            interventions.append("Demonstrate advanced features relevant to their use case")

    # Add account-specific suggestions
    if account_data["plan"] == "starter":
        interventions.append("Explore upsell to Professional tier with more features")

    # Remove duplicates
    return list(set(interventions))


def calculate_conversion_probability(account_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate probability of trial conversion to paid.

    Args:
        account_data: Account dictionary (should be trial account)

    Returns:
        Dictionary with conversion probability and insights
    """
    company = account_data["company"]
    usage = account_data["usage_signals"]

    logger.info(f"Calculating conversion probability for: {company}")

    # Simple scoring model
    probability = 0.0

    # High DAU is strong signal
    dau = usage.get("daily_active_users", 0)
    if dau >= 15:
        probability += 0.30
    elif dau >= 10:
        probability += 0.20
    elif dau >= 5:
        probability += 0.10

    # Feature adoption
    features = usage.get("features_adopted", 0)
    if features >= 5:
        probability += 0.25
    elif features >= 3:
        probability += 0.15
    elif features >= 2:
        probability += 0.05

    # API usage
    api_calls = usage.get("api_calls_per_day", 0)
    if api_calls >= 300:
        probability += 0.20
    elif api_calls >= 150:
        probability += 0.10
    elif api_calls >= 50:
        probability += 0.05

    # Login frequency
    login_freq = usage.get("login_frequency_7d", 0)
    if login_freq >= 14:
        probability += 0.25
    elif login_freq >= 10:
        probability += 0.15
    elif login_freq >= 5:
        probability += 0.05

    # Determine trial day (mock calculation)
    trial_day = 10  # Would calculate from created_date in production

    # Key engagement signals
    engagement_signals = []
    if dau >= 10:
        engagement_signals.append(f"Strong daily usage ({dau} DAU)")
    if features >= 3:
        engagement_signals.append(f"Good feature adoption ({features} features)")
    if api_calls >= 150:
        engagement_signals.append(f"Active API integration ({api_calls} calls/day)")

    # Recommendations
    recommendations = []
    if probability >= CONVERSION_THRESHOLDS["high"]:
        recommendations.append("Send upgrade prompt with success stories")
        recommendations.append("Offer onboarding call to ensure success")
    elif probability >= CONVERSION_THRESHOLDS["medium"]:
        recommendations.append("Provide feature tutorial to drive adoption")
        recommendations.append("Share case study from similar customer")
    else:
        recommendations.append("Increase engagement with personalized outreach")
        recommendations.append("Identify and remove adoption blockers")

    logger.info(f"Conversion probability: {company} = {probability:.2%}")

    return {
        "account_id": account_data["id"],
        "company": company,
        "trial_day": trial_day,
        "conversion_probability": round(probability, 3),
        "probability_tier": get_probability_tier(probability),
        "key_engagement_signals": engagement_signals,
        "recommended_actions": recommendations,
        "model_version": MODEL_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def get_probability_tier(probability: float) -> str:
    """Determine tier based on probability."""
    if probability >= CONVERSION_THRESHOLDS["high"]:
        return "high"
    elif probability >= CONVERSION_THRESHOLDS["medium"]:
        return "medium"
    else:
        return "low"
