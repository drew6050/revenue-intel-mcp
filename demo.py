#!/usr/bin/env python3
"""
Interactive demo of the Revenue Intelligence MCP Server.
Run this to explore the system interactively.
"""

import json
from scoring import score_lead, detect_churn_risk, calculate_conversion_probability
from data_store import get_account, get_lead, get_all_accounts, get_all_leads
from config import MODEL_VERSION


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title):
    """Print a section divider."""
    print(f"\n--- {title} ---")


def print_json(data):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=2))


def show_menu():
    """Display the main menu."""
    print_header("Revenue Intelligence System - Interactive Demo")
    print("\nWhat would you like to explore?\n")
    print("  [1] Browse sample accounts (CRM data)")
    print("  [2] Browse sample leads")
    print("  [3] Score a specific lead")
    print("  [4] Detect churn risk for an account")
    print("  [5] Calculate conversion probability (trial account)")
    print("  [6] View model information")
    print("  [7] See what MCP tools are available")
    print("  [0] Exit\n")


def browse_accounts():
    """Browse and display accounts."""
    accounts = get_all_accounts()

    print_section("Sample Accounts (20 total)")
    print("\nAccount Tiers:")

    by_plan = {}
    for acc in accounts:
        plan = acc['plan']
        if plan not in by_plan:
            by_plan[plan] = []
        by_plan[plan].append(acc)

    for plan in ['enterprise', 'professional', 'starter', 'trial']:
        if plan in by_plan:
            print(f"\n  {plan.upper()} ({len(by_plan[plan])} accounts):")
            for acc in by_plan[plan][:3]:  # Show first 3 of each
                status_emoji = "✓" if acc['status'] == 'active' else "⚠" if acc['status'] == 'at_risk' else "◉"
                print(f"    {status_emoji} {acc['id']}: {acc['company']:<30} MRR: ${acc['mrr']:>6}")

    print("\n\nPick an account to see details (or press Enter to skip):")
    choice = input("  Account ID (e.g., acc_001): ").strip()

    if choice:
        account = get_account(choice)
        if account:
            print_section(f"Account Details: {account['company']}")
            print_json(account)
        else:
            print("  Account not found!")


def browse_leads():
    """Browse and display leads."""
    leads = get_all_leads()

    print_section("Sample Leads (30 total)")
    print("\nShowing first 10:\n")

    for lead in leads[:10]:
        signals = lead['signals']
        demo = "✓" if signals.get('demo_requested') else " "
        trial = "✓" if signals.get('free_trial_started') else " "
        engagement = signals.get('email_engagement_score', 0)

        print(f"  {lead['id']}: {lead['company']:<35} | Demo:{demo} Trial:{trial} | Engagement:{engagement:>3}")

    print("\n\nPick a lead to see details (or press Enter to skip):")
    choice = input("  Lead ID (e.g., lead_001): ").strip()

    if choice:
        lead = get_lead(choice)
        if lead:
            print_section(f"Lead Details: {lead['company']}")
            print_json(lead)
        else:
            print("  Lead not found!")


def demo_lead_scoring():
    """Interactive lead scoring demo."""
    print_section("Lead Scoring Demo")

    print("\nExample leads to score:")
    examples = [
        ("lead_001", "FutureTech Innovations (Hot prospect)"),
        ("lead_002", "StartupHub (Cold prospect)"),
        ("lead_003", "Enterprise Solutions Corp (Hot enterprise)"),
    ]

    for lead_id, desc in examples:
        print(f"  {lead_id}: {desc}")

    choice = input("\nEnter lead ID to score (or press Enter for lead_001): ").strip() or "lead_001"

    lead = get_lead(choice)
    if not lead:
        print("  Lead not found!")
        return

    print(f"\nScoring: {lead['company']}")
    print(f"  Industry: {lead['industry']}")
    print(f"  Employees: {lead['employee_count']}")
    print(f"  Signals: {json.dumps(lead['signals'], indent=4)}")

    print("\n⏳ Running ML model...")

    result = score_lead(
        company_name=lead["company"],
        signals=lead["signals"],
        industry=lead["industry"],
        employee_count=lead["employee_count"]
    )

    print_section("SCORING RESULT")
    print(f"\n  🎯 Score: {result['score']:.1f}/100")
    print(f"  🔥 Tier: {result['tier'].upper()}")
    print(f"  📝 Explanation: {result['explanation']}")

    print("\n  📊 Top Feature Contributions:")
    sorted_attrs = sorted(result['feature_attributions'], key=lambda x: x['contribution'], reverse=True)
    for attr in sorted_attrs[:5]:
        impact_emoji = "📈" if attr['impact'] == 'positive' else "📉" if attr['impact'] == 'negative' else "➖"
        print(f"    {impact_emoji} {attr['feature_name']:<30} {attr['contribution']:>5.1f}% | Value: {attr['value']}")


def demo_churn_detection():
    """Interactive churn detection demo."""
    print_section("Churn Risk Detection Demo")

    print("\nExample accounts to analyze:")
    examples = [
        ("acc_001", "Acme Corp (Healthy enterprise)"),
        ("acc_006", "EduLearn Platform (At-risk)"),
        ("acc_011", "Marketing Wizards (At-risk)"),
    ]

    for acc_id, desc in examples:
        print(f"  {acc_id}: {desc}")

    choice = input("\nEnter account ID (or press Enter for acc_006): ").strip() or "acc_006"

    account = get_account(choice)
    if not account:
        print("  Account not found!")
        return

    print(f"\nAnalyzing: {account['company']}")
    print(f"  Plan: {account['plan']}")
    print(f"  Status: {account['status']}")
    print(f"  MRR: ${account['mrr']}")

    print("\n⏳ Analyzing usage patterns...")

    result = detect_churn_risk(account)

    print_section("CHURN RISK ANALYSIS")
    print(f"\n  ⚠️  Risk Score: {result['risk_score']:.1f}/100")
    print(f"  🎚️  Risk Tier: {result['risk_tier'].upper()}")

    if result['declining_signals']:
        print(f"\n  📉 Declining Signals:")
        for signal in result['declining_signals']:
            print(f"    • {signal}")

    if result['suggested_interventions']:
        print(f"\n  💡 Suggested Interventions:")
        for intervention in result['suggested_interventions']:
            print(f"    • {intervention}")


def demo_conversion():
    """Interactive conversion probability demo."""
    print_section("Conversion Probability Demo")

    # Find trial accounts
    all_accounts = get_all_accounts()
    trial_accounts = [acc for acc in all_accounts if acc['plan'] == 'trial']

    print("\nTrial accounts available:")
    for acc in trial_accounts:
        print(f"  {acc['id']}: {acc['company']}")

    if not trial_accounts:
        print("  No trial accounts found!")
        return

    choice = input(f"\nEnter trial account ID (or press Enter for {trial_accounts[0]['id']}): ").strip()
    if not choice:
        choice = trial_accounts[0]['id']

    account = get_account(choice)
    if not account:
        print("  Account not found!")
        return

    if account['plan'] != 'trial':
        print(f"  ⚠️  Warning: {account['company']} is not a trial account (plan: {account['plan']})")
        return

    print(f"\nAnalyzing trial: {account['company']}")
    print(f"  Created: {account['created_date']}")

    print("\n⏳ Calculating conversion probability...")

    result = calculate_conversion_probability(account)

    print_section("CONVERSION ANALYSIS")
    print(f"\n  📊 Conversion Probability: {result['conversion_probability']:.1%}")
    print(f"  🎯 Tier: {result['probability_tier'].upper()}")
    print(f"  📅 Trial Day: {result['trial_day']}")

    if result['key_engagement_signals']:
        print(f"\n  ✅ Key Engagement Signals:")
        for signal in result['key_engagement_signals']:
            print(f"    • {signal}")

    if result['recommended_actions']:
        print(f"\n  🎬 Recommended Actions:")
        for action in result['recommended_actions']:
            print(f"    • {action}")


def show_model_info():
    """Display model information."""
    print_section("Model Information")

    from config import (
        MODEL_VERSION, TRAINING_DATE, MODEL_PERFORMANCE_METRICS,
        FEATURE_IMPORTANCE, LEAD_TIER_THRESHOLDS, CHURN_RISK_THRESHOLDS
    )

    print(f"\n  Model Version: {MODEL_VERSION}")
    print(f"  Training Date: {TRAINING_DATE}")

    print("\n  Performance Metrics:")
    for metric, value in MODEL_PERFORMANCE_METRICS.items():
        print(f"    {metric}: {value:.3f}")

    print("\n  Lead Scoring Thresholds:")
    for tier, threshold in LEAD_TIER_THRESHOLDS.items():
        print(f"    {tier}: ≥{threshold}")

    print("\n  Churn Risk Thresholds:")
    for tier, threshold in CHURN_RISK_THRESHOLDS.items():
        print(f"    {tier}: ≥{threshold}")

    print("\n  Top 5 Feature Importance:")
    sorted_features = sorted(FEATURE_IMPORTANCE.items(), key=lambda x: x[1], reverse=True)
    for feature, importance in sorted_features[:5]:
        bar_length = int(importance * 50)
        bar = "█" * bar_length
        print(f"    {feature:<30} {bar} {importance:.2f}")


def show_mcp_tools():
    """Show what MCP tools are available."""
    print_section("Available MCP Tools")

    tools = [
        {
            "name": "score_lead",
            "description": "Score a lead (0-100) with hot/warm/cold tier and feature attributions",
            "example": '{"company_name": "Acme", "signals": {...}, "industry": "tech", "employee_count": 500}'
        },
        {
            "name": "get_conversion_insights",
            "description": "Calculate trial-to-paid conversion probability",
            "example": '{"account_id": "acc_002"}'
        },
        {
            "name": "detect_churn_risk",
            "description": "Analyze churn risk with intervention suggestions",
            "example": '{"account_id": "acc_006"}'
        },
        {
            "name": "check_model_health",
            "description": "Monitor model health, uptime, and drift",
            "example": '{}'
        },
        {
            "name": "log_prediction",
            "description": "Log a prediction for observability",
            "example": '{"prediction_data": {...}}'
        }
    ]

    print("\nWhen integrated with MCP clients (like Claude Desktop), these tools are available:\n")

    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool['name']}")
        print(f"     {tool['description']}")
        print(f"     Example: {tool['example']}\n")

    print("\nMCP Resources:")
    print("  • crm://accounts/{id} - Get account data")
    print("  • crm://leads/{id} - Get lead data")
    print("  • models://lead_scorer/metadata - Get model metadata")

    print("\nMCP Prompts:")
    print("  • analyze-account-expansion - CS team upsell template")
    print("  • weekly-lead-report - Sales pipeline report template")
    print("  • explain-low-score - Lead score explanation template")


def main():
    """Main interactive loop."""
    while True:
        show_menu()
        choice = input("Your choice: ").strip()

        if choice == "0":
            print("\n👋 Thanks for exploring the Revenue Intelligence System!\n")
            break
        elif choice == "1":
            browse_accounts()
        elif choice == "2":
            browse_leads()
        elif choice == "3":
            demo_lead_scoring()
        elif choice == "4":
            demo_churn_detection()
        elif choice == "5":
            demo_conversion()
        elif choice == "6":
            show_model_info()
        elif choice == "7":
            show_mcp_tools()
        else:
            print("\n  ⚠️  Invalid choice. Please try again.")

        input("\n\nPress Enter to continue...")


if __name__ == "__main__":
    main()
