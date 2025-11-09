"""
Tests for scoring logic.
"""

import pytest
from scoring import (
    score_lead,
    detect_churn_risk,
    calculate_conversion_probability,
    calculate_engagement_score,
    calculate_intent_score
)
from config import MODEL_VERSION


class TestLeadScoring:
    """Test lead scoring functionality."""

    def test_score_lead_hot_tier(self):
        """Test that high-quality leads score in hot tier."""
        signals = {
            "website_visits_30d": 60,
            "demo_requested": True,
            "whitepaper_downloads": 5,
            "email_engagement_score": 90,
            "linkedin_engagement": True,
            "free_trial_started": True
        }

        result = score_lead(
            company_name="Test Corp",
            signals=signals,
            industry="technology",
            employee_count=1000
        )

        assert result["score"] >= 70
        assert result["tier"] == "hot"
        assert result["model_version"] == MODEL_VERSION
        assert "feature_attributions" in result
        assert len(result["feature_attributions"]) > 0

    def test_score_lead_cold_tier(self):
        """Test that low-quality leads score in cold tier."""
        signals = {
            "website_visits_30d": 2,
            "demo_requested": False,
            "whitepaper_downloads": 0,
            "email_engagement_score": 15,
            "linkedin_engagement": False,
            "free_trial_started": False
        }

        result = score_lead(
            company_name="Small Co",
            signals=signals,
            industry="retail",
            employee_count=10
        )

        assert result["score"] < 40
        assert result["tier"] == "cold"

    def test_score_lead_warm_tier(self):
        """Test that medium-quality leads score in warm tier."""
        signals = {
            "website_visits_30d": 25,
            "demo_requested": True,
            "whitepaper_downloads": 2,
            "email_engagement_score": 65,
            "linkedin_engagement": False,
            "free_trial_started": False
        }

        result = score_lead(
            company_name="MidMarket Inc",
            signals=signals,
            industry="finance",
            employee_count=250
        )

        assert 40 <= result["score"] < 70
        assert result["tier"] == "warm"

    def test_score_lead_feature_attributions(self):
        """Test that feature attributions are generated."""
        signals = {
            "website_visits_30d": 30,
            "demo_requested": True,
            "whitepaper_downloads": 3,
            "email_engagement_score": 75,
            "linkedin_engagement": True,
            "free_trial_started": True
        }

        result = score_lead(
            company_name="Test Corp",
            signals=signals,
            industry="technology",
            employee_count=500
        )

        # Check that attributions exist and have required fields
        assert "feature_attributions" in result
        attributions = result["feature_attributions"]
        assert len(attributions) > 0

        for attr in attributions:
            assert "feature_name" in attr
            assert "contribution" in attr
            assert "value" in attr
            assert "impact" in attr

    def test_score_lead_explanation_generated(self):
        """Test that explanation is generated."""
        signals = {
            "website_visits_30d": 45,
            "demo_requested": True,
            "whitepaper_downloads": 4,
            "email_engagement_score": 85,
            "linkedin_engagement": True,
            "free_trial_started": True
        }

        result = score_lead(
            company_name="HighValue Corp",
            signals=signals,
            industry="saas",
            employee_count=800
        )

        assert "explanation" in result
        assert len(result["explanation"]) > 0
        assert "HighValue Corp" in result["explanation"]


class TestEngagementScoring:
    """Test engagement score calculation."""

    def test_calculate_engagement_score_high(self):
        """Test high engagement signals."""
        signals = {
            "website_visits_30d": 50,
            "email_engagement_score": 90,
            "demo_requested": True,
            "free_trial_started": True,
            "whitepaper_downloads": 5
        }

        score, attributions = calculate_engagement_score(signals)

        assert score > 70
        assert len(attributions) == 5

    def test_calculate_engagement_score_low(self):
        """Test low engagement signals."""
        signals = {
            "website_visits_30d": 2,
            "email_engagement_score": 10,
            "demo_requested": False,
            "free_trial_started": False,
            "whitepaper_downloads": 0
        }

        score, attributions = calculate_engagement_score(signals)

        assert score < 30
        assert len(attributions) == 5


class TestChurnDetection:
    """Test churn risk detection."""

    def test_detect_churn_risk_low(self):
        """Test account with low churn risk."""
        account = {
            "id": "acc_test",
            "company": "Healthy Co",
            "plan": "enterprise",
            "usage_signals": {
                "daily_active_users": 100,
                "features_adopted": 10,
                "support_tickets_30d": 1,
                "nps_score": 9,
                "login_frequency_7d": 35
            }
        }

        result = detect_churn_risk(account)

        assert result["risk_score"] < 30
        assert result["risk_tier"] == "low"
        assert "account_id" in result
        assert "declining_signals" in result

    def test_detect_churn_risk_high(self):
        """Test account with high churn risk."""
        account = {
            "id": "acc_test",
            "company": "AtRisk Co",
            "plan": "professional",
            "usage_signals": {
                "daily_active_users": 3,
                "features_adopted": 2,
                "support_tickets_30d": 8,
                "nps_score": 3,
                "login_frequency_7d": 2
            }
        }

        result = detect_churn_risk(account)

        assert result["risk_score"] >= 50
        assert result["risk_tier"] in ["high", "critical"]
        assert len(result["declining_signals"]) > 0
        assert len(result["suggested_interventions"]) > 0

    def test_detect_churn_risk_interventions(self):
        """Test that interventions are suggested for at-risk accounts."""
        account = {
            "id": "acc_test",
            "company": "NeedsHelp Co",
            "plan": "starter",
            "usage_signals": {
                "daily_active_users": 4,
                "features_adopted": 1,
                "support_tickets_30d": 6,
                "nps_score": 4,
                "login_frequency_7d": 3
            }
        }

        result = detect_churn_risk(account)

        assert "suggested_interventions" in result
        assert len(result["suggested_interventions"]) > 0


class TestConversionProbability:
    """Test conversion probability calculation."""

    def test_calculate_conversion_high_probability(self):
        """Test trial with high conversion probability."""
        account = {
            "id": "acc_trial",
            "company": "ActiveTrial Co",
            "plan": "trial",
            "created_date": "2024-10-20",
            "usage_signals": {
                "daily_active_users": 20,
                "features_adopted": 6,
                "api_calls_per_day": 500,
                "login_frequency_7d": 18
            }
        }

        result = calculate_conversion_probability(account)

        assert result["conversion_probability"] > 0.5
        assert result["probability_tier"] in ["high", "medium"]
        assert len(result["recommended_actions"]) > 0

    def test_calculate_conversion_low_probability(self):
        """Test trial with low conversion probability."""
        account = {
            "id": "acc_trial",
            "company": "InactiveTrial Co",
            "plan": "trial",
            "created_date": "2024-10-20",
            "usage_signals": {
                "daily_active_users": 2,
                "features_adopted": 1,
                "api_calls_per_day": 10,
                "login_frequency_7d": 3
            }
        }

        result = calculate_conversion_probability(account)

        assert result["conversion_probability"] < 0.4
        assert result["probability_tier"] in ["low", "medium"]

    def test_calculate_conversion_recommendations(self):
        """Test that recommendations are provided."""
        account = {
            "id": "acc_trial",
            "company": "Trial Co",
            "plan": "trial",
            "created_date": "2024-10-20",
            "usage_signals": {
                "daily_active_users": 12,
                "features_adopted": 4,
                "api_calls_per_day": 200,
                "login_frequency_7d": 12
            }
        }

        result = calculate_conversion_probability(account)

        assert "recommended_actions" in result
        assert len(result["recommended_actions"]) > 0
        assert "key_engagement_signals" in result


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_score_lead_missing_signals(self):
        """Test scoring with minimal signals."""
        signals = {}

        result = score_lead(
            company_name="Minimal Co",
            signals=signals,
            industry="technology",
            employee_count=50
        )

        # Should still return valid result with defaults
        assert "score" in result
        assert "tier" in result
        assert result["score"] >= 0

    def test_score_lead_unknown_industry(self):
        """Test scoring with unknown industry."""
        signals = {
            "website_visits_30d": 30,
            "demo_requested": True,
            "whitepaper_downloads": 2,
            "email_engagement_score": 70,
            "linkedin_engagement": True,
            "free_trial_started": False
        }

        result = score_lead(
            company_name="Unknown Industry Co",
            signals=signals,
            industry="unknown_industry_xyz",
            employee_count=200
        )

        # Should use default industry score
        assert "score" in result
        assert result["tier"] in ["hot", "warm", "cold"]

    def test_churn_risk_none_nps(self):
        """Test churn detection when NPS is None."""
        account = {
            "id": "acc_test",
            "company": "NoNPS Co",
            "plan": "trial",
            "usage_signals": {
                "daily_active_users": 10,
                "features_adopted": 3,
                "support_tickets_30d": 2,
                "nps_score": None,
                "login_frequency_7d": 12
            }
        }

        result = detect_churn_risk(account)

        # Should handle None NPS gracefully
        assert "risk_score" in result
        assert result["risk_score"] >= 0
