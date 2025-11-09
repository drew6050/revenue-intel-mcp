"""
Mock data for the Revenue Intelligence MCP server.
Contains realistic sample accounts, leads, and prediction logs.
In production, this would be replaced with database/data warehouse connections.
"""

from typing import List, Dict, Any

# In-memory storage for accounts (simulates CRM data)
ACCOUNTS: List[Dict[str, Any]] = [
    {
        "id": "acc_001",
        "company": "Acme Corp",
        "plan": "enterprise",
        "mrr": 5000,
        "created_date": "2024-01-15",
        "industry": "technology",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 45,
            "features_adopted": 8,
            "api_calls_per_day": 1200,
            "support_tickets_30d": 2,
            "nps_score": 9,
            "login_frequency_7d": 28
        }
    },
    {
        "id": "acc_002",
        "company": "TechStart Inc",
        "plan": "trial",
        "mrr": 0,
        "created_date": "2024-10-20",
        "industry": "saas",
        "status": "trial",
        "usage_signals": {
            "daily_active_users": 8,
            "features_adopted": 3,
            "api_calls_per_day": 150,
            "support_tickets_30d": 0,
            "nps_score": None,
            "login_frequency_7d": 12
        }
    },
    {
        "id": "acc_003",
        "company": "Global Finance Ltd",
        "plan": "professional",
        "mrr": 1200,
        "created_date": "2023-08-10",
        "industry": "finance",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 22,
            "features_adopted": 6,
            "api_calls_per_day": 600,
            "support_tickets_30d": 1,
            "nps_score": 8,
            "login_frequency_7d": 20
        }
    },
    {
        "id": "acc_004",
        "company": "RetailMax Systems",
        "plan": "starter",
        "mrr": 299,
        "created_date": "2024-06-01",
        "industry": "retail",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 5,
            "features_adopted": 2,
            "api_calls_per_day": 80,
            "support_tickets_30d": 3,
            "nps_score": 6,
            "login_frequency_7d": 8
        }
    },
    {
        "id": "acc_005",
        "company": "HealthTech Solutions",
        "plan": "enterprise",
        "mrr": 8500,
        "created_date": "2023-03-20",
        "industry": "healthcare",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 120,
            "features_adopted": 10,
            "api_calls_per_day": 2500,
            "support_tickets_30d": 4,
            "nps_score": 9,
            "login_frequency_7d": 35
        }
    },
    {
        "id": "acc_006",
        "company": "EduLearn Platform",
        "plan": "professional",
        "mrr": 950,
        "created_date": "2024-02-14",
        "industry": "education",
        "status": "at_risk",
        "usage_signals": {
            "daily_active_users": 12,
            "features_adopted": 4,
            "api_calls_per_day": 200,
            "support_tickets_30d": 8,
            "nps_score": 4,
            "login_frequency_7d": 5
        }
    },
    {
        "id": "acc_007",
        "company": "Manufacturing Pro",
        "plan": "enterprise",
        "mrr": 6200,
        "created_date": "2023-11-05",
        "industry": "manufacturing",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 65,
            "features_adopted": 9,
            "api_calls_per_day": 1800,
            "support_tickets_30d": 2,
            "nps_score": 8,
            "login_frequency_7d": 30
        }
    },
    {
        "id": "acc_008",
        "company": "SmallBiz Tools",
        "plan": "starter",
        "mrr": 199,
        "created_date": "2024-09-10",
        "industry": "consulting",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 3,
            "features_adopted": 2,
            "api_calls_per_day": 45,
            "support_tickets_30d": 1,
            "nps_score": 7,
            "login_frequency_7d": 10
        }
    },
    {
        "id": "acc_009",
        "company": "CloudScale Ventures",
        "plan": "trial",
        "mrr": 0,
        "created_date": "2024-10-28",
        "industry": "technology",
        "status": "trial",
        "usage_signals": {
            "daily_active_users": 15,
            "features_adopted": 5,
            "api_calls_per_day": 350,
            "support_tickets_30d": 0,
            "nps_score": None,
            "login_frequency_7d": 18
        }
    },
    {
        "id": "acc_010",
        "company": "Legal Partners LLP",
        "plan": "professional",
        "mrr": 1500,
        "created_date": "2024-04-22",
        "industry": "legal",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 18,
            "features_adopted": 5,
            "api_calls_per_day": 400,
            "support_tickets_30d": 2,
            "nps_score": 8,
            "login_frequency_7d": 22
        }
    },
    {
        "id": "acc_011",
        "company": "Marketing Wizards",
        "plan": "professional",
        "mrr": 899,
        "created_date": "2023-12-01",
        "industry": "marketing",
        "status": "at_risk",
        "usage_signals": {
            "daily_active_users": 6,
            "features_adopted": 3,
            "api_calls_per_day": 120,
            "support_tickets_30d": 5,
            "nps_score": 5,
            "login_frequency_7d": 4
        }
    },
    {
        "id": "acc_012",
        "company": "DataDriven Analytics",
        "plan": "enterprise",
        "mrr": 12000,
        "created_date": "2023-05-15",
        "industry": "data_analytics",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 200,
            "features_adopted": 12,
            "api_calls_per_day": 5000,
            "support_tickets_30d": 3,
            "nps_score": 10,
            "login_frequency_7d": 42
        }
    },
    {
        "id": "acc_013",
        "company": "Logistics Express",
        "plan": "starter",
        "mrr": 249,
        "created_date": "2024-08-05",
        "industry": "logistics",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 7,
            "features_adopted": 3,
            "api_calls_per_day": 100,
            "support_tickets_30d": 2,
            "nps_score": 7,
            "login_frequency_7d": 12
        }
    },
    {
        "id": "acc_014",
        "company": "AgriTech Farms",
        "plan": "professional",
        "mrr": 1100,
        "created_date": "2024-03-10",
        "industry": "agriculture",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 14,
            "features_adopted": 5,
            "api_calls_per_day": 280,
            "support_tickets_30d": 1,
            "nps_score": 8,
            "login_frequency_7d": 18
        }
    },
    {
        "id": "acc_015",
        "company": "PropTech Realty",
        "plan": "trial",
        "mrr": 0,
        "created_date": "2024-10-25",
        "industry": "real_estate",
        "status": "trial",
        "usage_signals": {
            "daily_active_users": 4,
            "features_adopted": 2,
            "api_calls_per_day": 60,
            "support_tickets_30d": 1,
            "nps_score": None,
            "login_frequency_7d": 8
        }
    },
    {
        "id": "acc_016",
        "company": "InsureTech Global",
        "plan": "enterprise",
        "mrr": 7500,
        "created_date": "2023-07-20",
        "industry": "insurance",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 95,
            "features_adopted": 11,
            "api_calls_per_day": 2200,
            "support_tickets_30d": 3,
            "nps_score": 9,
            "login_frequency_7d": 33
        }
    },
    {
        "id": "acc_017",
        "company": "MediaStream Co",
        "plan": "professional",
        "mrr": 1300,
        "created_date": "2024-01-08",
        "industry": "media",
        "status": "at_risk",
        "usage_signals": {
            "daily_active_users": 10,
            "features_adopted": 4,
            "api_calls_per_day": 180,
            "support_tickets_30d": 7,
            "nps_score": 5,
            "login_frequency_7d": 6
        }
    },
    {
        "id": "acc_018",
        "company": "EnergyGrid Solutions",
        "plan": "enterprise",
        "mrr": 9800,
        "created_date": "2023-09-12",
        "industry": "energy",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 140,
            "features_adopted": 10,
            "api_calls_per_day": 3500,
            "support_tickets_30d": 2,
            "nps_score": 9,
            "login_frequency_7d": 38
        }
    },
    {
        "id": "acc_019",
        "company": "FoodDelivery Hub",
        "plan": "starter",
        "mrr": 299,
        "created_date": "2024-07-15",
        "industry": "food_delivery",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 9,
            "features_adopted": 3,
            "api_calls_per_day": 200,
            "support_tickets_30d": 1,
            "nps_score": 7,
            "login_frequency_7d": 14
        }
    },
    {
        "id": "acc_020",
        "company": "TravelTech Bookings",
        "plan": "professional",
        "mrr": 1750,
        "created_date": "2024-05-20",
        "industry": "travel",
        "status": "active",
        "usage_signals": {
            "daily_active_users": 28,
            "features_adopted": 7,
            "api_calls_per_day": 850,
            "support_tickets_30d": 2,
            "nps_score": 8,
            "login_frequency_7d": 24
        }
    }
]

# In-memory storage for leads (simulates marketing automation/CRM data)
LEADS: List[Dict[str, Any]] = [
    {
        "id": "lead_001",
        "company": "FutureTech Innovations",
        "industry": "technology",
        "employee_count": 250,
        "contact_name": "Sarah Johnson",
        "contact_title": "VP of Engineering",
        "signals": {
            "website_visits_30d": 45,
            "demo_requested": True,
            "whitepaper_downloads": 3,
            "email_engagement_score": 85,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_002",
        "company": "StartupHub",
        "industry": "saas",
        "employee_count": 15,
        "contact_name": "Mike Chen",
        "contact_title": "CEO",
        "signals": {
            "website_visits_30d": 8,
            "demo_requested": False,
            "whitepaper_downloads": 1,
            "email_engagement_score": 35,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_003",
        "company": "Enterprise Solutions Corp",
        "industry": "finance",
        "employee_count": 5000,
        "contact_name": "Jennifer Williams",
        "contact_title": "CTO",
        "signals": {
            "website_visits_30d": 62,
            "demo_requested": True,
            "whitepaper_downloads": 5,
            "email_engagement_score": 92,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_004",
        "company": "LocalRetail Co",
        "industry": "retail",
        "employee_count": 50,
        "contact_name": "Robert Martinez",
        "contact_title": "IT Manager",
        "signals": {
            "website_visits_30d": 3,
            "demo_requested": False,
            "whitepaper_downloads": 0,
            "email_engagement_score": 15,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_005",
        "company": "HealthCare Systems Inc",
        "industry": "healthcare",
        "employee_count": 1200,
        "contact_name": "Dr. Emily Brown",
        "contact_title": "Chief Medical Information Officer",
        "signals": {
            "website_visits_30d": 38,
            "demo_requested": True,
            "whitepaper_downloads": 4,
            "email_engagement_score": 78,
            "linkedin_engagement": True,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_006",
        "company": "EduTech Learning",
        "industry": "education",
        "employee_count": 180,
        "contact_name": "David Kim",
        "contact_title": "Director of Technology",
        "signals": {
            "website_visits_30d": 22,
            "demo_requested": True,
            "whitepaper_downloads": 2,
            "email_engagement_score": 65,
            "linkedin_engagement": False,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_007",
        "company": "ManufacturePlus",
        "industry": "manufacturing",
        "employee_count": 800,
        "contact_name": "Lisa Anderson",
        "contact_title": "VP of Operations",
        "signals": {
            "website_visits_30d": 18,
            "demo_requested": False,
            "whitepaper_downloads": 2,
            "email_engagement_score": 52,
            "linkedin_engagement": True,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_008",
        "company": "ConsultPro Group",
        "industry": "consulting",
        "employee_count": 45,
        "contact_name": "Tom Wilson",
        "contact_title": "Managing Partner",
        "signals": {
            "website_visits_30d": 12,
            "demo_requested": False,
            "whitepaper_downloads": 1,
            "email_engagement_score": 42,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_009",
        "company": "CloudNative Systems",
        "industry": "technology",
        "employee_count": 320,
        "contact_name": "Amanda Lee",
        "contact_title": "Engineering Manager",
        "signals": {
            "website_visits_30d": 55,
            "demo_requested": True,
            "whitepaper_downloads": 4,
            "email_engagement_score": 88,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_010",
        "company": "LegalTech Partners",
        "industry": "legal",
        "employee_count": 95,
        "contact_name": "James Taylor",
        "contact_title": "Senior Partner",
        "signals": {
            "website_visits_30d": 28,
            "demo_requested": True,
            "whitepaper_downloads": 3,
            "email_engagement_score": 70,
            "linkedin_engagement": True,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_011",
        "company": "MarketingGrowth Co",
        "industry": "marketing",
        "employee_count": 60,
        "contact_name": "Rachel Green",
        "contact_title": "CMO",
        "signals": {
            "website_visits_30d": 15,
            "demo_requested": False,
            "whitepaper_downloads": 1,
            "email_engagement_score": 48,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_012",
        "company": "DataScience Labs",
        "industry": "data_analytics",
        "employee_count": 450,
        "contact_name": "Alex Turner",
        "contact_title": "Head of Data",
        "signals": {
            "website_visits_30d": 72,
            "demo_requested": True,
            "whitepaper_downloads": 6,
            "email_engagement_score": 95,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_013",
        "company": "LogisticsFlow Inc",
        "industry": "logistics",
        "employee_count": 220,
        "contact_name": "Kevin Brown",
        "contact_title": "Operations Director",
        "signals": {
            "website_visits_30d": 10,
            "demo_requested": False,
            "whitepaper_downloads": 1,
            "email_engagement_score": 38,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_014",
        "company": "AgriSolutions Tech",
        "industry": "agriculture",
        "employee_count": 140,
        "contact_name": "Maria Garcia",
        "contact_title": "Head of Innovation",
        "signals": {
            "website_visits_30d": 25,
            "demo_requested": True,
            "whitepaper_downloads": 2,
            "email_engagement_score": 68,
            "linkedin_engagement": True,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_015",
        "company": "RealEstateDigital",
        "industry": "real_estate",
        "employee_count": 85,
        "contact_name": "Chris Robinson",
        "contact_title": "CIO",
        "signals": {
            "website_visits_30d": 6,
            "demo_requested": False,
            "whitepaper_downloads": 0,
            "email_engagement_score": 22,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_016",
        "company": "InsuranceAI Corp",
        "industry": "insurance",
        "employee_count": 1500,
        "contact_name": "Patricia Moore",
        "contact_title": "SVP of Technology",
        "signals": {
            "website_visits_30d": 48,
            "demo_requested": True,
            "whitepaper_downloads": 5,
            "email_engagement_score": 82,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_017",
        "company": "ContentMedia Group",
        "industry": "media",
        "employee_count": 200,
        "contact_name": "Brian Clark",
        "contact_title": "VP of Digital",
        "signals": {
            "website_visits_30d": 20,
            "demo_requested": False,
            "whitepaper_downloads": 2,
            "email_engagement_score": 55,
            "linkedin_engagement": True,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_018",
        "company": "EnergyOptimize Systems",
        "industry": "energy",
        "employee_count": 650,
        "contact_name": "Susan White",
        "contact_title": "Chief Innovation Officer",
        "signals": {
            "website_visits_30d": 42,
            "demo_requested": True,
            "whitepaper_downloads": 4,
            "email_engagement_score": 80,
            "linkedin_engagement": True,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_019",
        "company": "FoodTech Delivery",
        "industry": "food_delivery",
        "employee_count": 110,
        "contact_name": "Daniel Nguyen",
        "contact_title": "Tech Lead",
        "signals": {
            "website_visits_30d": 14,
            "demo_requested": False,
            "whitepaper_downloads": 1,
            "email_engagement_score": 45,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_020",
        "company": "TravelCloud Platforms",
        "industry": "travel",
        "employee_count": 380,
        "contact_name": "Michelle Davis",
        "contact_title": "Director of Engineering",
        "signals": {
            "website_visits_30d": 35,
            "demo_requested": True,
            "whitepaper_downloads": 3,
            "email_engagement_score": 75,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_021",
        "company": "SmallOffice Tools",
        "industry": "technology",
        "employee_count": 8,
        "contact_name": "John Smith",
        "contact_title": "Founder",
        "signals": {
            "website_visits_30d": 2,
            "demo_requested": False,
            "whitepaper_downloads": 0,
            "email_engagement_score": 10,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_022",
        "company": "MidMarket Dynamics",
        "industry": "saas",
        "employee_count": 420,
        "contact_name": "Karen Johnson",
        "contact_title": "VP of Product",
        "signals": {
            "website_visits_30d": 58,
            "demo_requested": True,
            "whitepaper_downloads": 5,
            "email_engagement_score": 90,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_023",
        "company": "BioTech Research",
        "industry": "healthcare",
        "employee_count": 280,
        "contact_name": "Dr. Richard Evans",
        "contact_title": "Director of IT",
        "signals": {
            "website_visits_30d": 30,
            "demo_requested": True,
            "whitepaper_downloads": 3,
            "email_engagement_score": 72,
            "linkedin_engagement": True,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_024",
        "company": "AutoParts Distribution",
        "industry": "manufacturing",
        "employee_count": 550,
        "contact_name": "Mark Thompson",
        "contact_title": "COO",
        "signals": {
            "website_visits_30d": 16,
            "demo_requested": False,
            "whitepaper_downloads": 1,
            "email_engagement_score": 50,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_025",
        "company": "FinanceAI Solutions",
        "industry": "finance",
        "employee_count": 920,
        "contact_name": "Angela Martinez",
        "contact_title": "Chief Data Officer",
        "signals": {
            "website_visits_30d": 68,
            "demo_requested": True,
            "whitepaper_downloads": 7,
            "email_engagement_score": 94,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_026",
        "company": "RetailChain Plus",
        "industry": "retail",
        "employee_count": 2500,
        "contact_name": "Steven Parker",
        "contact_title": "SVP of Technology",
        "signals": {
            "website_visits_30d": 52,
            "demo_requested": True,
            "whitepaper_downloads": 4,
            "email_engagement_score": 84,
            "linkedin_engagement": True,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_027",
        "company": "NonprofitTech Org",
        "industry": "nonprofit",
        "employee_count": 75,
        "contact_name": "Laura Wilson",
        "contact_title": "Technology Director",
        "signals": {
            "website_visits_30d": 9,
            "demo_requested": False,
            "whitepaper_downloads": 1,
            "email_engagement_score": 32,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_028",
        "company": "CyberSecurity Pro",
        "industry": "technology",
        "employee_count": 340,
        "contact_name": "Michael Chang",
        "contact_title": "CISO",
        "signals": {
            "website_visits_30d": 46,
            "demo_requested": True,
            "whitepaper_downloads": 5,
            "email_engagement_score": 86,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    },
    {
        "id": "lead_029",
        "company": "HospitalityTech Inc",
        "industry": "hospitality",
        "employee_count": 190,
        "contact_name": "Jessica Adams",
        "contact_title": "IT Manager",
        "signals": {
            "website_visits_30d": 11,
            "demo_requested": False,
            "whitepaper_downloads": 1,
            "email_engagement_score": 40,
            "linkedin_engagement": False,
            "free_trial_started": False
        }
    },
    {
        "id": "lead_030",
        "company": "GreenEnergy Ventures",
        "industry": "energy",
        "employee_count": 410,
        "contact_name": "Andrew Miller",
        "contact_title": "VP of Engineering",
        "signals": {
            "website_visits_30d": 40,
            "demo_requested": True,
            "whitepaper_downloads": 4,
            "email_engagement_score": 79,
            "linkedin_engagement": True,
            "free_trial_started": True
        }
    }
]

# In-memory storage for prediction logs (append-only)
# In production, this would be written to a data warehouse with proper partitioning
PREDICTION_LOGS: List[Dict[str, Any]] = []
