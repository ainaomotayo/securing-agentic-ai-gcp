# securing-agentic-ai-gcp

> Companion code repository for **"Securing Autonomous AI on Google Cloud: ADK, Multi-Agent Systems, and Production Security for Enterprise and Startup"**

---

## About This Repository

This repository contains all code examples from the book, organised by chapter. Each example has been tested against the versions listed in `requirements/requirements.txt`. A `CHANGELOG.md` in the root tracks any corrections or updates introduced by ADK version changes after publication.

**Book ISBN:** 978-0-000-00000-0 *(Sample, to be replaced)*
**Author:** Omotayo Aina
**Publisher:** Google Cloud Press
**Errata page:** https://ainaomotayo.com/errata/securing-agentic-ai-gcp

---

## Prerequisites

- Python 3.11 or 3.12
- A Google Cloud project with billing enabled
- The `gcloud` CLI installed and authenticated (`gcloud auth application-default login`)
- ADK Python v1.26.0+

Verify your environment before starting:

```bash
python -m pip install -r requirements/requirements.txt
python scripts/verify_environment.py
```

---

## Repository Structure

```
securing-agentic-ai-gcp/
│
├── README.md                        # This file
├── CHANGELOG.md                     # Version-specific corrections and updates
├── ERRATA.md                        # Book errata (corrections to printed text)
│
├── requirements/
│   ├── requirements.txt             # All dependencies: production extras
│   └── requirements-dev.txt         # Development and testing dependencies
│
├── scripts/
│   ├── verify_environment.py        # Checks installed versions against book requirements
│   └── setup_gcp.sh                 # Creates the GCP resources needed to run examples
│
├── chapter-01/                      # Chapter 1: The Agentic Paradigm Shift
│   ├── README.md
│   └── (conceptual chapter; no code examples)
│
├── chapter-02/                      # Chapter 2: The Google Agentic Stack
│   ├── README.md
│   ├── listing_02_01_hello_agent.py
│   └── listing_02_02_runner_basic.py
│
├── chapter-03/                      # Chapter 3: The Threat Landscape
│   ├── README.md
│   └── (conceptual chapter; see threat model worksheet in Appendix B)
│
├── chapter-04/                      # Chapter 4: Agent Identity and IAM
│   ├── README.md
│   ├── listing_04_01_service_account_setup.sh
│   ├── listing_04_02_workload_identity.sh
│   ├── listing_04_03_secret_manager.py
│   └── listing_04_04_iam_conditions.sh
│
├── chapter-05/                      # Chapter 5: Authentication Patterns
│   ├── README.md
│   ├── listing_05_01_oauth2_tool.py
│   ├── listing_05_02_api_key_tool.py
│   └── listing_05_03_service_to_service.py
│
├── chapter-06/                      # Chapter 6: Zero Trust Architecture
│   ├── README.md
│   ├── listing_06_01_vpc_sc_setup.sh
│   └── listing_06_02_private_service_connect.sh
│
├── chapter-07/                      # Chapter 7: Secure Single-Agent Architecture
│   ├── README.md
│   ├── listing_07_01_minimal_agent.py
│   ├── listing_07_02_tool_allowlist.py
│   └── listing_07_03_system_instruction_pattern.py
│
├── chapter-08/                      # Chapter 8: Guardrails, Callbacks, and Model Armor
│   ├── README.md
│   ├── listing_08_01_before_model_callback.py
│   ├── listing_08_02_after_model_callback.py
│   ├── listing_08_03_model_armor_template.py
│   ├── listing_08_04_sanitize_input.py
│   └── listing_08_05_combined_guardrails.py
│
├── chapter-09/                      # Chapter 9: Securing Multi-Agent Systems
│   ├── README.md
│   ├── listing_09_01_orchestrator_agent.py
│   ├── listing_09_02_sub_agent_hardened.py
│   ├── listing_09_03_a2a_auth_client.py
│   ├── listing_09_04_agent_registry_discovery.py
│   └── listing_09_05_mcp_gcpauthprovider.py
│
├── chapter-10/                      # Chapter 10: Tool Security
│   ├── README.md
│   ├── listing_10_01_before_tool_callback.py
│   ├── listing_10_02_after_tool_callback.py
│   ├── listing_10_03_parameter_validation.py
│   └── listing_10_04_mcp_allowlist.py
│
├── chapter-11/                      # Chapter 11: Session, State, Memory, and Data Governance
│   ├── README.md
│   ├── listing_11_01_vertexai_session_service.py
│   ├── listing_11_02_session_ttl.py
│   ├── listing_11_03_memory_bank_service.py
│   ├── listing_11_04_corpus_isolation.py
│   └── listing_11_05_cmek_setup.sh
│
├── chapter-12/                      # Chapter 12: Secure Code Execution
│   ├── README.md
│   ├── listing_12_01_code_execution_tool.py
│   └── listing_12_02_sandbox_configuration.py
│
├── chapter-13/                      # Chapter 13: Observability, Events, and Audit
│   ├── README.md
│   ├── listing_13_01_cloud_trace_setup.py
│   ├── listing_13_02_structured_logging.py
│   ├── listing_13_03_audit_log_queries.sh
│   └── listing_13_04_alert_policies.sh
│
├── chapter-14/                      # Chapter 14: Human-in-the-Loop
│   ├── README.md
│   ├── listing_14_01_human_tool.py
│   └── listing_14_02_approval_gate.py
│
├── chapter-15/                      # Chapter 15: Evaluation and Red Teaming
│   ├── README.md
│   ├── listing_15_01_evaluation_dataset.py
│   ├── listing_15_02_auto_sxs.py
│   ├── listing_15_03_example_store.py
│   └── listing_15_04_red_team_prompts.txt
│
├── chapter-16/                      # Chapter 16: Secure Deployment
│   ├── README.md
│   ├── listing_16_01_deploy_agent_engine.sh
│   ├── listing_16_02_binary_authorisation.sh
│   ├── listing_16_03_cloud_build_pipeline.yaml
│   └── listing_16_04_rollback_procedure.sh
│
├── chapter-17/                      # Chapter 17: Incident Response
│   ├── README.md
│   ├── listing_17_01_isolate_agent.sh
│   ├── listing_17_02_forensic_log_export.sh
│   └── listing_17_03_scc_alert_policy.sh
│
├── chapter-18/                      # Chapter 18: Governance and Compliance
│   ├── README.md
│   └── listing_18_01_org_policy.sh
│
├── appendix-a/                      # Appendix A: Security Quick Reference
│   ├── README.md
│   └── verify_environment.py        # Also at scripts/verify_environment.py
│
├── appendix-b/                      # Appendix B: Threat Model Templates
│   ├── README.md
│   └── threat_model_worksheet.md    # Blank worksheet for your own systems
│
├── appendix-c/                      # Appendix C: Compliance Mapping
│   ├── README.md
│   └── pre_audit_checklist.md       # Evidence collection checklist
│
└── appendix-d/                      # Appendix D: Version Matrix
    ├── README.md
    └── verify_environment.py        # Environment verification script
```

---

## Getting Started

### Step 1: Clone the repository

```bash
git clone https://github.com/[AUTHOR_GITHUB]/securing-agentic-ai-gcp.git
cd securing-agentic-ai-gcp
```

### Step 2: Create a Python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate          # Linux / macOS
.venv\Scripts\activate             # Windows
```

### Step 3: Install dependencies

```bash
pip install -r requirements/requirements.txt
```

### Step 4: Authenticate with Google Cloud

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### Step 5: Create required GCP resources

The setup script creates the service accounts, enables APIs, and configures the resources needed to run the examples. Review the script before running it, as it will create billable resources in your project.

```bash
bash scripts/setup_gcp.sh YOUR_PROJECT_ID us-central1
```

### Step 6: Verify your environment

```bash
python scripts/verify_environment.py
```

All checks should show `[PASS]`. If any show `[FAIL]`, follow the instructions printed by the script.

---

## Running Examples

Each chapter directory has a `README.md` that explains what the examples demonstrate, in what order to run them, and what GCP resources they require. Start with the chapter README before running any example.

```bash
# Example: run the Model Armor guardrail example from Chapter 8
cd chapter-08
python listing_08_03_model_armor_template.py --project YOUR_PROJECT_ID
```

---

## requirements/requirements.txt

```
# Core ADK with all production extras
google-adk[agent-identity,a2a,eval]>=1.26.0

# Google Cloud client libraries
google-cloud-aiplatform>=1.70.0
google-cloud-secret-manager>=2.20.0
google-cloud-logging>=3.10.0
google-cloud-kms>=2.24.0
google-cloud-dlp>=3.22.0

# Model Armor
google-cloud-modelarmor>=0.3.0

# HTTP client for A2A authentication
httpx>=0.27.0

# Google authentication
google-auth>=2.28.0
google-auth-httplib2>=0.2.0

# Utilities
python-dotenv>=1.0.0
pydantic>=2.6.0
```

---

## Errata

Corrections to the printed text are tracked in `ERRATA.md` in this repository and on the errata page at:

```
https://ainaomotayo.com/errata/securing-agentic-ai-gcp
```

If you find an error not listed there, please open an issue in this repository with the label `errata`. Include the chapter number, page number, and a description of the error.

---

## Version Updates

As ADK and Google Cloud services release new versions, some examples may require updates. All version-related changes are tracked in `CHANGELOG.md`. The version matrix in Appendix D of the book, and in `appendix-d/`, records the versions against which examples were originally verified.

---

## Contributing

This repository is a companion to the book and is not open for general feature contributions. Accepted contributions:

- **Errata reports** via GitHub Issues (label: `errata`)
- **Version compatibility fixes** via Pull Request (label: `version-update`)

Please do not open issues for general ADK questions; those are better addressed in the ADK GitHub Discussions or the Google Cloud Community forums.

---

## License

Code examples in this repository are licensed under the Apache License 2.0. See `LICENSE` for the full text.

The book text itself ("Securing Autonomous AI on Google Cloud") is copyright Omotayo Aina and is not included in this repository.

---

## Contact

**Author:** Omotayo Aina
**Email:** https://ainaomotayo.com
**LinkedIn:** https://www.linkedin.com/in/ainaomotayo/

---

*"The agents we build now will be making decisions that affect real people. Getting the security right is not a competitive advantage; it is a professional obligation."*
