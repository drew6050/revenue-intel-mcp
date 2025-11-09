#!/usr/bin/env python3
"""
Example usage of the Revenue Intelligence MCP Server.
Demonstrates scoring, churn detection, and conversion analysis.
"""

from scoring import score_lead, detect_churn_risk, calculate_conversion_probability
from data_store import get_account, get_lead, store_prediction_log
from config import MODEL_VERSION

print("=" * 70)
print("Revenue Intelligence MCP Server - Example Usage")
print("=" * 70)
print()

# Example 1: Score a lead
print("1. LEAD SCORING")
print("-" * 70)

lead = get_lead("lead_003")  # Enterprise Solutions Corp
print(f"Scoring lead: {lead['company']}")
print(f"  Industry: {lead['industry']}")
print(f"  Employees: {lead['employee_count']}")
print(f"  Signals: {lead['signals']}")
print()

result = score_lead(
    company_name=lead["company"],
    signals=lead["signals"],
    industry=lead["industry"],
    employee_count=lead["employee_count"]
)

print(f"RESULT:")
print(f"  Score: {result['score']}/100")
print(f"  Tier: {result['tier'].upper()}")
print(f"  Explanation: {result['explanation']}")
print()

# Log the prediction
log = store_prediction_log(
    prediction_type="lead_score",
    input_data={"company_name": lead["company"]},
    prediction_result=result,
    model_version=MODEL_VERSION
)
print(f"  Logged: {log['log_id']}")
print()

# Example 2: Detect churn risk
print("2. CHURN RISK DETECTION")
print("-" * 70)

account = get_account("acc_006")  # EduLearn Platform (at-risk)
print(f"Analyzing account: {account['company']}")
print(f"  Plan: {account['plan']}")
print(f"  Status: {account['status']}")
print(f"  MRR: ${account['mrr']}")
print(f"  Usage signals: {account['usage_signals']}")
print()

churn_result = detect_churn_risk(account)

print(f"RESULT:")
print(f"  Risk Score: {churn_result['risk_score']}/100")
print(f"  Risk Tier: {churn_result['risk_tier'].upper()}")
print(f"  Declining signals:")
for signal in churn_result['declining_signals']:
    print(f"    - {signal}")
print(f"  Suggested interventions:")
for intervention in churn_result['suggested_interventions']:
    print(f"    - {intervention}")
print()

# Example 3: Conversion probability
print("3. CONVERSION PROBABILITY")
print("-" * 70)

trial_account = get_account("acc_009")  # CloudScale Ventures (trial)
print(f"Analyzing trial: {trial_account['company']}")
print(f"  Plan: {trial_account['plan']}")
print(f"  Created: {trial_account['created_date']}")
print(f"  Usage signals: {trial_account['usage_signals']}")
print()

conversion_result = calculate_conversion_probability(trial_account)

print(f"RESULT:")
print(f"  Conversion Probability: {conversion_result['conversion_probability']:.1%}")
print(f"  Tier: {conversion_result['probability_tier'].upper()}")
print(f"  Key engagement signals:")
for signal in conversion_result['key_engagement_signals']:
    print(f"    - {signal}")
print(f"  Recommended actions:")
for action in conversion_result['recommended_actions']:
    print(f"    - {action}")
print()

print("=" * 70)
print("All examples completed successfully!")
print(f"Model version: {MODEL_VERSION}")
print("=" * 70)
