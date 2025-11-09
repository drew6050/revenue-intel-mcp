"""
Data access layer for the Revenue Intelligence MCP server.
Provides functions to interact with in-memory data structures.
In production, this would interface with databases, data warehouses, or APIs.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

from mock_data import ACCOUNTS, LEADS, PREDICTION_LOGS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_account(account_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve account by ID.

    Args:
        account_id: The account identifier

    Returns:
        Account data dictionary or None if not found
    """
    logger.info(f"Fetching account: {account_id}")
    for account in ACCOUNTS:
        if account["id"] == account_id:
            logger.info(f"Account found: {account['company']}")
            return account

    logger.warning(f"Account not found: {account_id}")
    return None


def get_lead(lead_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve lead by ID.

    Args:
        lead_id: The lead identifier

    Returns:
        Lead data dictionary or None if not found
    """
    logger.info(f"Fetching lead: {lead_id}")
    for lead in LEADS:
        if lead["id"] == lead_id:
            logger.info(f"Lead found: {lead['company']}")
            return lead

    logger.warning(f"Lead not found: {lead_id}")
    return None


def get_all_accounts() -> List[Dict[str, Any]]:
    """
    Retrieve all accounts.

    Returns:
        List of all account dictionaries
    """
    logger.info(f"Fetching all accounts (count: {len(ACCOUNTS)})")
    return ACCOUNTS


def get_all_leads() -> List[Dict[str, Any]]:
    """
    Retrieve all leads.

    Returns:
        List of all lead dictionaries
    """
    logger.info(f"Fetching all leads (count: {len(LEADS)})")
    return LEADS


def store_prediction_log(
    prediction_type: str,
    input_data: Dict[str, Any],
    prediction_result: Dict[str, Any],
    model_version: str
) -> Dict[str, Any]:
    """
    Store a prediction log entry for monitoring and drift detection.

    Args:
        prediction_type: Type of prediction (lead_score, churn_risk, etc.)
        input_data: The input features used for prediction
        prediction_result: The prediction output
        model_version: Version of the model used

    Returns:
        Dictionary with log_id, timestamp, and success status
    """
    log_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"

    log_entry = {
        "log_id": log_id,
        "timestamp": timestamp,
        "prediction_type": prediction_type,
        "input_data": input_data,
        "prediction_result": prediction_result,
        "model_version": model_version
    }

    PREDICTION_LOGS.append(log_entry)

    logger.info(
        f"Stored prediction log: {log_id} | "
        f"Type: {prediction_type} | "
        f"Model: {model_version}"
    )

    return {
        "log_id": log_id,
        "timestamp": timestamp,
        "stored_successfully": True
    }


def get_prediction_logs(
    prediction_type: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Retrieve prediction logs, optionally filtered by type.

    Args:
        prediction_type: Filter by prediction type (optional)
        limit: Maximum number of logs to return

    Returns:
        List of prediction log dictionaries
    """
    logs = PREDICTION_LOGS

    if prediction_type:
        logs = [log for log in logs if log["prediction_type"] == prediction_type]

    # Return most recent first
    logs = sorted(logs, key=lambda x: x["timestamp"], reverse=True)

    logger.info(
        f"Retrieved {len(logs[:limit])} prediction logs "
        f"(type: {prediction_type or 'all'})"
    )

    return logs[:limit]


def get_prediction_count_24h() -> int:
    """
    Get count of predictions in last 24 hours.
    For demo purposes, returns total count.
    In production, would filter by timestamp.

    Returns:
        Count of recent predictions
    """
    count = len(PREDICTION_LOGS)
    logger.info(f"Total predictions logged: {count}")
    return count


def get_accounts_by_status(status: str) -> List[Dict[str, Any]]:
    """
    Retrieve accounts filtered by status.

    Args:
        status: Account status (active, trial, at_risk, churned)

    Returns:
        List of account dictionaries matching the status
    """
    accounts = [acc for acc in ACCOUNTS if acc["status"] == status]
    logger.info(f"Found {len(accounts)} accounts with status: {status}")
    return accounts


def get_leads_by_tier(tier: str) -> List[Dict[str, Any]]:
    """
    Retrieve leads that would score in a particular tier.
    Note: This is a simplified version; in production would use actual scores.

    Args:
        tier: Lead tier (hot, warm, cold)

    Returns:
        List of lead dictionaries
    """
    # For demo purposes, returns all leads
    # In production, would filter by pre-computed scores
    logger.info(f"Fetching leads for tier: {tier}")
    return LEADS
