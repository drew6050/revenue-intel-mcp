#!/usr/bin/env python3
"""
Revenue Intelligence MCP Server

A production-ready MCP server demonstrating ML system integration patterns
for customer-facing business teams. Provides lead scoring, churn detection,
and conversion insights with full observability.
"""

import logging
from typing import Any
from datetime import datetime, timedelta

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from config import (
    MODEL_VERSION,
    TRAINING_DATE,
    MODEL_PERFORMANCE_METRICS,
    FEATURE_IMPORTANCE,
    LOG_LEVEL,
    LOG_FORMAT
)
from data_store import (
    get_account,
    get_lead,
    store_prediction_log,
    get_prediction_count_24h,
    get_all_accounts
)
from scoring import (
    score_lead,
    detect_churn_risk,
    calculate_conversion_probability
)

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Initialize MCP server
app = Server("revenue-intel-mcp")

# Track server start time for uptime calculation
SERVER_START_TIME = datetime.utcnow()


@app.list_resources()
async def list_resources() -> list[types.Resource]:
    """
    List available resources in the Revenue Intelligence system.
    Resources expose CRM data and model metadata.
    """
    logger.info("Listing available resources")

    return [
        types.Resource(
            uri="crm://accounts/list",
            name="All CRM Accounts",
            mimeType="application/json",
            description="List of all customer accounts with usage signals"
        ),
        types.Resource(
            uri="models://lead_scorer/metadata",
            name="Lead Scorer Model Metadata",
            mimeType="application/json",
            description="Model version, performance metrics, and drift status"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read a specific resource by URI.

    Supported URIs:
    - crm://accounts/{account_id} - Get specific account data
    - crm://leads/{lead_id} - Get specific lead data
    - models://lead_scorer/metadata - Get model metadata
    """
    logger.info(f"Reading resource: {uri}")

    # Parse URI
    if uri.startswith("crm://accounts/"):
        account_id = uri.replace("crm://accounts/", "")

        if account_id == "list":
            # Return all accounts
            accounts = get_all_accounts()
            import json
            return json.dumps(accounts, indent=2)

        account = get_account(account_id)
        if not account:
            raise ValueError(f"Account not found: {account_id}")

        import json
        return json.dumps(account, indent=2)

    elif uri.startswith("crm://leads/"):
        lead_id = uri.replace("crm://leads/", "")
        lead = get_lead(lead_id)
        if not lead:
            raise ValueError(f"Lead not found: {lead_id}")

        import json
        return json.dumps(lead, indent=2)

    elif uri == "models://lead_scorer/metadata":
        # Calculate drift status (simplified)
        prediction_count = get_prediction_count_24h()
        drift_status = "normal" if prediction_count < 1000 else "warning"

        metadata = {
            "model_version": MODEL_VERSION,
            "training_date": TRAINING_DATE,
            "performance_metrics": MODEL_PERFORMANCE_METRICS,
            "feature_importance": FEATURE_IMPORTANCE,
            "drift_status": drift_status
        }

        import json
        return json.dumps(metadata, indent=2)

    else:
        raise ValueError(f"Unknown resource URI: {uri}")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """
    List available tools for revenue intelligence operations.
    Tools enable ML predictions and system monitoring.
    """
    logger.info("Listing available tools")

    return [
        types.Tool(
            name="score_lead",
            description="Score a lead based on company attributes and engagement signals. Returns score (0-100), tier (hot/warm/cold), and feature attributions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "Name of the company"
                    },
                    "signals": {
                        "type": "object",
                        "description": "Engagement signals (website_visits_30d, demo_requested, email_engagement_score, etc.)",
                        "properties": {
                            "website_visits_30d": {"type": "number"},
                            "demo_requested": {"type": "boolean"},
                            "whitepaper_downloads": {"type": "number"},
                            "email_engagement_score": {"type": "number"},
                            "linkedin_engagement": {"type": "boolean"},
                            "free_trial_started": {"type": "boolean"}
                        }
                    },
                    "industry": {
                        "type": "string",
                        "description": "Company industry (technology, finance, healthcare, etc.)",
                        "default": "technology"
                    },
                    "employee_count": {
                        "type": "number",
                        "description": "Number of employees",
                        "default": 100
                    }
                },
                "required": ["company_name", "signals"]
            }
        ),
        types.Tool(
            name="get_conversion_insights",
            description="Analyze trial account and predict conversion probability with recommended actions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "Account ID (e.g., acc_002)"
                    }
                },
                "required": ["account_id"]
            }
        ),
        types.Tool(
            name="detect_churn_risk",
            description="Analyze account health and detect churn risk with suggested interventions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "Account ID (e.g., acc_001)"
                    }
                },
                "required": ["account_id"]
            }
        ),
        types.Tool(
            name="check_model_health",
            description="Check ML model health metrics, uptime, and drift status.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        types.Tool(
            name="log_prediction",
            description="Log a prediction for monitoring and drift detection.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prediction_data": {
                        "type": "object",
                        "description": "Prediction details including type, input, and result",
                        "properties": {
                            "prediction_type": {"type": "string"},
                            "input_data": {"type": "object"},
                            "prediction_result": {"type": "object"}
                        },
                        "required": ["prediction_type", "input_data", "prediction_result"]
                    }
                },
                "required": ["prediction_data"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[types.TextContent]:
    """
    Execute a tool with the provided arguments.
    """
    logger.info(f"Calling tool: {name}")

    import json

    try:
        if name == "score_lead":
            # Extract parameters
            company_name = arguments["company_name"]
            signals = arguments["signals"]
            industry = arguments.get("industry", "technology")
            employee_count = arguments.get("employee_count", 100)

            # Score the lead
            result = score_lead(company_name, signals, industry, employee_count)

            # Log the prediction
            store_prediction_log(
                prediction_type="lead_score",
                input_data={
                    "company_name": company_name,
                    "signals": signals,
                    "industry": industry,
                    "employee_count": employee_count
                },
                prediction_result=result,
                model_version=MODEL_VERSION
            )

            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "get_conversion_insights":
            account_id = arguments["account_id"]
            account = get_account(account_id)

            if not account:
                raise ValueError(f"Account not found: {account_id}")

            if account["plan"] != "trial":
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": f"Account {account_id} is not a trial account (plan: {account['plan']})"
                    }, indent=2)
                )]

            result = calculate_conversion_probability(account)

            # Log the prediction
            store_prediction_log(
                prediction_type="conversion_probability",
                input_data={"account_id": account_id},
                prediction_result=result,
                model_version=MODEL_VERSION
            )

            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "detect_churn_risk":
            account_id = arguments["account_id"]
            account = get_account(account_id)

            if not account:
                raise ValueError(f"Account not found: {account_id}")

            result = detect_churn_risk(account)

            # Log the prediction
            store_prediction_log(
                prediction_type="churn_risk",
                input_data={"account_id": account_id},
                prediction_result=result,
                model_version=MODEL_VERSION
            )

            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        elif name == "check_model_health":
            uptime_seconds = (datetime.utcnow() - SERVER_START_TIME).total_seconds()
            uptime_hours = uptime_seconds / 3600

            prediction_count = get_prediction_count_24h()

            # Simple drift detection (would compare distributions in production)
            drift_detected = prediction_count > 1000  # Simplified threshold

            health_status = {
                "model_version": MODEL_VERSION,
                "uptime_hours": round(uptime_hours, 2),
                "prediction_count_24h": prediction_count,
                "drift_detected": drift_detected,
                "accuracy_last_7d": MODEL_PERFORMANCE_METRICS["accuracy"],
                "performance_metrics": MODEL_PERFORMANCE_METRICS,
                "alerts": [
                    "High prediction volume - monitoring for drift"
                ] if drift_detected else []
            }

            return [types.TextContent(
                type="text",
                text=json.dumps(health_status, indent=2)
            )]

        elif name == "log_prediction":
            prediction_data = arguments["prediction_data"]

            result = store_prediction_log(
                prediction_type=prediction_data["prediction_type"],
                input_data=prediction_data["input_data"],
                prediction_result=prediction_data["prediction_result"],
                model_version=MODEL_VERSION
            )

            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "error": str(e),
                "tool": name
            }, indent=2)
        )]


@app.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    """
    List available prompt templates for revenue intelligence workflows.
    """
    logger.info("Listing available prompts")

    return [
        types.Prompt(
            name="analyze-account-expansion",
            description="Template for CS team to assess upsell opportunity for an account",
            arguments=[
                types.PromptArgument(
                    name="account_id",
                    description="Account ID to analyze",
                    required=True
                )
            ]
        ),
        types.Prompt(
            name="weekly-lead-report",
            description="Template for Sales leadership pipeline quality report",
            arguments=[
                types.PromptArgument(
                    name="week_number",
                    description="Week number for the report",
                    required=False
                )
            ]
        ),
        types.Prompt(
            name="explain-low-score",
            description="Template to generate explanation for why a lead scored poorly",
            arguments=[
                types.PromptArgument(
                    name="lead_id",
                    description="Lead ID to explain",
                    required=True
                )
            ]
        )
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    """
    Get a specific prompt template with arguments filled in.
    """
    logger.info(f"Getting prompt: {name}")

    if name == "analyze-account-expansion":
        account_id = arguments.get("account_id", "acc_001") if arguments else "acc_001"
        account = get_account(account_id)

        if not account:
            raise ValueError(f"Account not found: {account_id}")

        prompt_text = f"""# Account Expansion Analysis: {account['company']}

**Account ID:** {account_id}
**Current Plan:** {account['plan']}
**MRR:** ${account['mrr']}

## Task
Analyze this account's usage signals and determine:
1. Upsell readiness score (0-100)
2. Recommended next tier
3. Key talking points for CS conversation
4. Estimated expansion revenue potential

## Usage Signals
{account['usage_signals']}

Please provide a structured analysis with specific recommendations.
"""

        return types.GetPromptResult(
            description=f"Account expansion analysis for {account['company']}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=prompt_text
                    )
                )
            ]
        )

    elif name == "weekly-lead-report":
        week_number = arguments.get("week_number", "45") if arguments else "45"

        prompt_text = f"""# Weekly Lead Quality Report - Week {week_number}

## Task
Generate a leadership summary of lead pipeline quality including:

1. **Lead Volume & Velocity**
   - Total new leads this week
   - Hot/Warm/Cold distribution
   - Week-over-week trend

2. **Quality Metrics**
   - Average lead score
   - Demo request rate
   - Trial start rate
   - Top performing industries

3. **Pipeline Health**
   - High-value opportunities (enterprise leads scoring >80)
   - At-risk leads (engaged but not converting)
   - Recommended focus areas

4. **Action Items**
   - Leads requiring immediate follow-up
   - Campaigns to optimize
   - Resource allocation recommendations

Please analyze the lead data and provide a concise executive summary.
"""

        return types.GetPromptResult(
            description=f"Weekly lead pipeline quality report for week {week_number}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=prompt_text
                    )
                )
            ]
        )

    elif name == "explain-low-score":
        lead_id = arguments.get("lead_id", "lead_001") if arguments else "lead_001"
        lead = get_lead(lead_id)

        if not lead:
            raise ValueError(f"Lead not found: {lead_id}")

        # Score the lead
        result = score_lead(
            company_name=lead["company"],
            signals=lead["signals"],
            industry=lead["industry"],
            employee_count=lead["employee_count"]
        )

        prompt_text = f"""# Low Lead Score Explanation: {lead['company']}

**Lead ID:** {lead_id}
**Score:** {result['score']}/100 ({result['tier']} tier)
**Industry:** {lead['industry']}
**Size:** {lead['employee_count']} employees

## Current Engagement Signals
{lead['signals']}

## Task
This lead scored in the {result['tier']} tier. Please provide:

1. **Root Cause Analysis**
   - Which signals are weakest?
   - What's missing compared to high-scoring leads?

2. **Improvement Plan**
   - Specific actions to increase engagement
   - Content/campaigns to deploy
   - Timeline for re-scoring

3. **Resource Assessment**
   - Is this lead worth continued investment?
   - Should we adjust qualification criteria?

Provide a structured analysis with specific, actionable recommendations.
"""

        return types.GetPromptResult(
            description=f"Explanation for low score of {lead['company']}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=prompt_text
                    )
                )
            ]
        )

    else:
        raise ValueError(f"Unknown prompt: {name}")


async def main():
    """Run the MCP server."""
    logger.info(f"Starting Revenue Intelligence MCP Server (Model: {MODEL_VERSION})")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
