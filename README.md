# Revenue Intelligence MCP Server

A production-ready MCP server demonstrating ML system integration patterns for customer-facing business teams at scale. This server simulates a real-world ML-powered revenue intelligence platform, showcasing how to build observable, maintainable ML systems integrated with business workflows.

## Business Context

Modern revenue teams (Sales, Customer Success, Marketing) need real-time ML insights to prioritize leads, prevent churn, and maximize conversions. This server demonstrates how to build production ML systems that:

- **Integrate with business workflows** via MCP resources, tools, and prompts
- **Provide explainable predictions** with feature attribution
- **Enable monitoring and observability** through prediction logging
- **Support production ML patterns** like versioning, drift detection, and health checks

This is the type of system you'd find powering revenue operations at high-growth SaaS companies, integrated with tools like Salesforce, HubSpot, or custom CRMs.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Server Interface                     │
│  (Resources, Tools, Prompts for Claude Desktop/API)         │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐  ┌──────▼────────┐  ┌──────────────┐
│   Scoring    │  │  Data Store   │  │    Config    │
│   Engine     │  │   (CRM Data)  │  │  (Thresholds,│
│              │  │               │  │   Weights)   │
│ • Lead Score │  │ • Accounts    │  │              │
│ • Churn Risk │  │ • Leads       │  │ • Model v1.2.3│
│ • Conversion │  │ • Pred Logs   │  │ • Features   │
└──────────────┘  └───────────────┘  └──────────────┘
```

**Key Components:**

1. **MCP Server** (`server.py`) - Exposes resources, tools, and prompts via MCP protocol
2. **Scoring Engine** (`scoring.py`) - ML prediction logic with feature attribution
3. **Data Store** (`data_store.py`) - In-memory data access layer (simulates DB/warehouse)
4. **Configuration** (`config.py`) - Model parameters, thresholds, feature weights
5. **Mock Data** (`mock_data.py`) - 20 accounts, 30 leads with realistic signals

## Production ML Patterns Demonstrated

This server showcases essential production ML engineering patterns:

### 1. **Model Versioning & Metadata Tracking**
- Explicit model version (`v1.2.3`) stamped on every prediction
- Training date and performance metrics tracked
- Feature importance documented and accessible via MCP resource

### 2. **Prediction Logging for Monitoring**
- Every prediction logged with full input/output metadata
- Enables audit trails, debugging, and performance analysis
- Foundation for drift detection and model retraining pipelines

### 3. **Feature Attribution for Explainability**
- Each prediction includes feature-level attributions
- Shows which signals drove the score (e.g., "demo requested" contributed 20%)
- Critical for revenue team trust and regulatory compliance

### 4. **Drift Detection Framework**
- Health check tool monitors prediction volume and distribution
- Alerts when patterns deviate from training baseline
- Enables proactive model retraining before degradation

### 5. **Integration with Business Systems**
- Resources expose CRM data (accounts, leads) via standard URIs
- Tools map to revenue team workflows (score lead, detect churn)
- Prompts provide templates for common analysis tasks

### 6. **Health Monitoring and SLOs**
- `check_model_health` tool provides real-time system status
- Tracks uptime, prediction volume, accuracy, drift status
- Foundation for SLA monitoring and incident response

### 7. **Structured Error Handling**
- Comprehensive logging with structured context
- Graceful degradation for missing data
- Clear error messages for troubleshooting

## Installation

### Prerequisites
- Python 3.10+
- pip or uv for package management

### Setup

```bash
# Clone or navigate to the project
cd revenue-intel-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests to verify installation
pytest tests/ -v
```

## Usage

### Running the Server

#### With Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "revenue-intel": {
      "command": "python",
      "args": [
        "C:/Users/User/git-repo/revenue-intel-mcp/server.py"
      ]
    }
  }
}
```

Restart Claude Desktop and the server will be available.

#### Standalone Testing

```bash
# Run the server directly (for testing with MCP inspector)
python server.py
```

### Available Resources

Access CRM data and model metadata:

1. **`crm://accounts/{account_id}`** - Get account details
   ```
   Example: crm://accounts/acc_001
   Returns: Account data with usage signals, MRR, plan tier
   ```

2. **`crm://accounts/list`** - List all accounts
   ```
   Returns: Array of all 20 sample accounts
   ```

3. **`crm://leads/{lead_id}`** - Get lead details
   ```
   Example: crm://leads/lead_001
   Returns: Lead data with engagement signals, company info
   ```

4. **`models://lead_scorer/metadata`** - Model metadata
   ```
   Returns: Version, training date, performance metrics, feature importance, drift status
   ```

### Available Tools

Execute ML predictions and monitoring:

#### 1. `score_lead`
Score a lead based on company attributes and engagement signals.

```json
{
  "company_name": "Acme Corp",
  "signals": {
    "website_visits_30d": 45,
    "demo_requested": true,
    "whitepaper_downloads": 3,
    "email_engagement_score": 85,
    "linkedin_engagement": true,
    "free_trial_started": true
  },
  "industry": "technology",
  "employee_count": 500
}
```

Returns: Score (0-100), tier (hot/warm/cold), feature attributions, explanation

#### 2. `get_conversion_insights`
Predict trial-to-paid conversion probability.

```json
{
  "account_id": "acc_002"
}
```

Returns: Conversion probability, engagement signals, recommended actions

#### 3. `detect_churn_risk`
Analyze account health and identify churn risk.

```json
{
  "account_id": "acc_006"
}
```

Returns: Risk score, risk tier, declining signals, intervention suggestions

#### 4. `check_model_health`
Monitor ML system health and performance.

```json
{}
```

Returns: Model version, uptime, prediction count, drift status, accuracy

#### 5. `log_prediction`
Manually log a prediction for monitoring.

```json
{
  "prediction_data": {
    "prediction_type": "lead_score",
    "input_data": {...},
    "prediction_result": {...}
  }
}
```

Returns: Log ID, timestamp, success status

### Available Prompts

Pre-built templates for common workflows:

1. **`analyze-account-expansion`** - CS team upsell analysis
   - Argument: `account_id`
   - Use case: Assess account readiness for tier upgrade

2. **`weekly-lead-report`** - Sales leadership pipeline report
   - Argument: `week_number` (optional)
   - Use case: Weekly lead quality and velocity analysis

3. **`explain-low-score`** - Lead score explanation
   - Argument: `lead_id`
   - Use case: Understand why a lead scored poorly and how to improve

## Example Prompts to Try

Once connected to Claude Desktop, try these:

### Lead Scoring
> "Score this lead for me: Acme Corp, technology industry, 500 employees. They've visited our site 50 times, requested a demo, downloaded 3 whitepapers, have an email engagement score of 90, engaged on LinkedIn, and started a free trial."

### Churn Detection
> "Check the churn risk for account acc_006"

### Conversion Analysis
> "What's the conversion probability for trial account acc_002? What should we do to increase it?"

### Model Health
> "Check the health of the lead scoring model"

### Data Exploration
> "Show me all the trial accounts and analyze which ones are most likely to convert"

### Structured Analysis
> "Use the analyze-account-expansion prompt for account acc_001"

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_scoring.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Coverage:**
- ✅ Lead scoring (hot/warm/cold tiers)
- ✅ Churn risk detection
- ✅ Conversion probability calculation
- ✅ Feature attribution generation
- ✅ Prediction logging
- ✅ Data access layer
- ✅ Edge cases (missing data, invalid inputs)
- ✅ Mock data integrity

## Project Structure

```
revenue-intel-mcp/
├── server.py              # MCP server with resources, tools, prompts
├── scoring.py             # ML scoring logic (lead score, churn, conversion)
├── models.py              # Data models with type hints (Account, Lead, etc.)
├── data_store.py          # Data access layer (get/store operations)
├── mock_data.py           # Sample accounts, leads, prediction logs
├── config.py              # Model config, thresholds, feature weights
├── tests/
│   ├── __init__.py
│   ├── test_scoring.py    # Scoring logic tests
│   └── test_tools.py      # Data access and integration tests
├── pyproject.toml         # Python package configuration
├── .gitignore
└── README.md
```

## Configuration

Key configuration in `config.py`:

- **Model Version**: `v1.2.3`
- **Lead Tier Thresholds**: Hot (≥70), Warm (40-70), Cold (<40)
- **Feature Weights**: Company size (20%), Engagement (40%), Industry (20%), Intent (20%)
- **Industry Fit Scores**: Technology (90), SaaS (85), Finance (80), etc.
- **Churn Risk Thresholds**: Critical (≥70), High (50-70), Medium (30-50), Low (<30)

## Sample Data

**20 Accounts** across industries:
- 3 trial accounts (exploring product)
- 3 at-risk accounts (declining usage)
- 14 active accounts (various tiers: starter, professional, enterprise)

**30 Leads** with varying quality:
- Hot leads: High engagement, demo requested, enterprise size
- Warm leads: Moderate engagement, mid-market
- Cold leads: Low engagement, small companies

## Production Deployment Notes

**This demo uses in-memory storage.** For production deployment:

### Data Layer
- Replace `mock_data.py` with connections to:
  - **Snowflake/BigQuery** for historical data and feature store
  - **PostgreSQL/MySQL** for operational CRM data
  - **Redis** for real-time feature caching

### Model Serving
- Deploy scoring logic as:
  - **FastAPI/Flask** service for REST API
  - **AWS Lambda/Cloud Functions** for serverless
  - **SageMaker/Vertex AI** for managed ML serving

### Monitoring
- Implement production monitoring:
  - **Datadog/New Relic** for application metrics
  - **MLflow/Weights & Biases** for ML experiment tracking
  - **Grafana/Kibana** for prediction drift dashboards
  - **PagerDuty** for alert routing

### MLOps Pipeline
- Establish model lifecycle management:
  - **Feature pipelines** (dbt, Airflow) for data freshness
  - **Training pipelines** with version control (Git, DVC)
  - **A/B testing** framework for model evaluation
  - **Automated retraining** based on drift detection
  - **Shadow deployments** for validation before rollout

### Data Quality
- Add comprehensive data validation:
  - **Great Expectations** for input data quality checks
  - **Schema evolution** handling with Pydantic
  - **Feature drift monitoring** against training distributions

### Security & Compliance
- Implement security controls:
  - **Authentication/authorization** for API access
  - **PII handling** and data anonymization
  - **Audit logging** for regulatory compliance (GDPR, SOC2)
  - **Rate limiting** and DDoS protection

## License

MIT License - feel free to use as a template for your own ML systems.

## Contributing

This is a demonstration project. For production use, adapt the patterns to your specific:
- Data infrastructure (warehouse, feature store, CRM)
- ML frameworks (scikit-learn, XGBoost, PyTorch)
- Deployment environment (cloud provider, Kubernetes, serverless)
- Monitoring and observability stack

---

**Built with:** Python 3.10+ | MCP SDK | Type hints | Structured logging | pytest

**Demonstrates:** Production ML patterns | Business integration | Observability | Explainability
