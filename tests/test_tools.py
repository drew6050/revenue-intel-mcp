"""
Tests for MCP tools and data access.
"""

import pytest
from data_store import (
    get_account,
    get_lead,
    store_prediction_log,
    get_prediction_logs,
    get_prediction_count_24h,
    get_accounts_by_status
)
from mock_data import ACCOUNTS, LEADS, PREDICTION_LOGS
from config import MODEL_VERSION


class TestDataAccess:
    """Test data access layer."""

    def test_get_account_exists(self):
        """Test retrieving an existing account."""
        account = get_account("acc_001")

        assert account is not None
        assert account["id"] == "acc_001"
        assert "company" in account
        assert "usage_signals" in account

    def test_get_account_not_found(self):
        """Test retrieving non-existent account."""
        account = get_account("acc_nonexistent")

        assert account is None

    def test_get_lead_exists(self):
        """Test retrieving an existing lead."""
        lead = get_lead("lead_001")

        assert lead is not None
        assert lead["id"] == "lead_001"
        assert "company" in lead
        assert "signals" in lead

    def test_get_lead_not_found(self):
        """Test retrieving non-existent lead."""
        lead = get_lead("lead_nonexistent")

        assert lead is None

    def test_get_accounts_by_status(self):
        """Test filtering accounts by status."""
        active_accounts = get_accounts_by_status("active")

        assert len(active_accounts) > 0
        for account in active_accounts:
            assert account["status"] == "active"

    def test_get_accounts_by_status_trial(self):
        """Test filtering trial accounts."""
        trial_accounts = get_accounts_by_status("trial")

        assert len(trial_accounts) > 0
        for account in trial_accounts:
            assert account["status"] == "trial"
            assert account["plan"] == "trial"


class TestPredictionLogging:
    """Test prediction logging functionality."""

    def setup_method(self):
        """Clear prediction logs before each test."""
        PREDICTION_LOGS.clear()

    def test_store_prediction_log(self):
        """Test storing a prediction log."""
        input_data = {
            "company_name": "Test Corp",
            "signals": {"demo_requested": True}
        }
        prediction_result = {
            "score": 75.5,
            "tier": "hot"
        }

        result = store_prediction_log(
            prediction_type="lead_score",
            input_data=input_data,
            prediction_result=prediction_result,
            model_version=MODEL_VERSION
        )

        assert result["stored_successfully"] is True
        assert "log_id" in result
        assert "timestamp" in result

        # Verify it was added to logs
        assert len(PREDICTION_LOGS) == 1
        assert PREDICTION_LOGS[0]["prediction_type"] == "lead_score"

    def test_get_prediction_logs(self):
        """Test retrieving prediction logs."""
        # Store some logs
        for i in range(5):
            store_prediction_log(
                prediction_type="lead_score",
                input_data={"test": i},
                prediction_result={"score": i * 10},
                model_version=MODEL_VERSION
            )

        logs = get_prediction_logs()

        assert len(logs) == 5

    def test_get_prediction_logs_filtered(self):
        """Test retrieving filtered prediction logs."""
        # Store different types
        store_prediction_log(
            prediction_type="lead_score",
            input_data={},
            prediction_result={},
            model_version=MODEL_VERSION
        )
        store_prediction_log(
            prediction_type="churn_risk",
            input_data={},
            prediction_result={},
            model_version=MODEL_VERSION
        )
        store_prediction_log(
            prediction_type="lead_score",
            input_data={},
            prediction_result={},
            model_version=MODEL_VERSION
        )

        lead_logs = get_prediction_logs(prediction_type="lead_score")

        assert len(lead_logs) == 2
        for log in lead_logs:
            assert log["prediction_type"] == "lead_score"

    def test_get_prediction_logs_limit(self):
        """Test pagination/limiting of prediction logs."""
        # Store many logs
        for i in range(20):
            store_prediction_log(
                prediction_type="lead_score",
                input_data={"test": i},
                prediction_result={"score": i},
                model_version=MODEL_VERSION
            )

        logs = get_prediction_logs(limit=10)

        assert len(logs) == 10

    def test_get_prediction_count_24h(self):
        """Test getting prediction count."""
        # Clear and add some logs
        PREDICTION_LOGS.clear()

        for i in range(7):
            store_prediction_log(
                prediction_type="lead_score",
                input_data={"test": i},
                prediction_result={"score": i},
                model_version=MODEL_VERSION
            )

        count = get_prediction_count_24h()

        assert count == 7


class TestMockData:
    """Test mock data integrity."""

    def test_accounts_have_required_fields(self):
        """Test that all accounts have required fields."""
        required_fields = ["id", "company", "plan", "mrr", "created_date", "usage_signals"]

        for account in ACCOUNTS:
            for field in required_fields:
                assert field in account, f"Account {account.get('id')} missing {field}"

    def test_leads_have_required_fields(self):
        """Test that all leads have required fields."""
        required_fields = ["id", "company", "industry", "employee_count", "signals"]

        for lead in LEADS:
            for field in required_fields:
                assert field in lead, f"Lead {lead.get('id')} missing {field}"

    def test_account_usage_signals_structure(self):
        """Test that usage signals have expected structure."""
        expected_signals = [
            "daily_active_users",
            "features_adopted",
            "api_calls_per_day"
        ]

        for account in ACCOUNTS:
            usage = account["usage_signals"]
            for signal in expected_signals:
                assert signal in usage, f"Account {account['id']} missing signal {signal}"

    def test_lead_signals_structure(self):
        """Test that lead signals have expected structure."""
        expected_signals = [
            "website_visits_30d",
            "demo_requested",
            "email_engagement_score"
        ]

        for lead in LEADS:
            signals = lead["signals"]
            for signal in expected_signals:
                assert signal in signals, f"Lead {lead['id']} missing signal {signal}"

    def test_accounts_count(self):
        """Test that we have expected number of accounts."""
        assert len(ACCOUNTS) == 20

    def test_leads_count(self):
        """Test that we have expected number of leads."""
        assert len(LEADS) == 30

    def test_account_status_variety(self):
        """Test that we have variety in account statuses."""
        statuses = set(account["status"] for account in ACCOUNTS)

        assert "active" in statuses
        assert "trial" in statuses
        assert "at_risk" in statuses

    def test_account_plan_variety(self):
        """Test that we have variety in account plans."""
        plans = set(account["plan"] for account in ACCOUNTS)

        assert "starter" in plans
        assert "professional" in plans
        assert "enterprise" in plans
        assert "trial" in plans


class TestIntegration:
    """Integration tests combining multiple components."""

    def setup_method(self):
        """Clear prediction logs before each test."""
        PREDICTION_LOGS.clear()

    def test_score_and_log_lead(self):
        """Test scoring a lead and logging the prediction."""
        from scoring import score_lead

        # Get a lead from mock data
        lead = get_lead("lead_003")
        assert lead is not None

        # Score the lead
        result = score_lead(
            company_name=lead["company"],
            signals=lead["signals"],
            industry=lead["industry"],
            employee_count=lead["employee_count"]
        )

        # Log the prediction
        log_result = store_prediction_log(
            prediction_type="lead_score",
            input_data={
                "company_name": lead["company"],
                "signals": lead["signals"]
            },
            prediction_result=result,
            model_version=MODEL_VERSION
        )

        assert log_result["stored_successfully"] is True
        assert len(PREDICTION_LOGS) == 1

    def test_churn_detection_on_real_account(self):
        """Test churn detection on actual mock account."""
        from scoring import detect_churn_risk

        # Get an at-risk account
        at_risk_accounts = get_accounts_by_status("at_risk")
        assert len(at_risk_accounts) > 0

        account = at_risk_accounts[0]
        result = detect_churn_risk(account)

        # At-risk accounts should have elevated risk scores
        assert result["risk_score"] > 0
        assert len(result["declining_signals"]) > 0

    def test_conversion_probability_on_trial(self):
        """Test conversion probability on trial account."""
        from scoring import calculate_conversion_probability

        # Get a trial account
        trial_accounts = get_accounts_by_status("trial")
        assert len(trial_accounts) > 0

        account = trial_accounts[0]
        result = calculate_conversion_probability(account)

        assert "conversion_probability" in result
        assert 0 <= result["conversion_probability"] <= 1
        assert "recommended_actions" in result
