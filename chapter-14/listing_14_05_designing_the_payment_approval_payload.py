#!/usr/bin/env python3
"""
Designing the Payment Approval Payload
Chapter 14 — Human In The Loop

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

from google.adk.tools import ToolContext
import hashlib

def initiate_wire_transfer(
    recipient_name: str,
    recipient_account: str,
    bank_routing: str,
    amount_usd: float,
    invoice_id: str,
    tool_context: ToolContext,
) -> dict:
    """Initiate a wire transfer with advanced HITL confirmation."""

    tool_confirmation = tool_context.tool_confirmation

    if not tool_confirmation:
        # First invocation: request approval with full context
        # Look up the expected vendor account from verified records
        expected_account = tool_context.state.get(
            f"app:vendor_account:{recipient_name}", None
        )
        account_matches_records = (
            expected_account == recipient_account
            if expected_account else None
        )

        # Check for anomalies
        risk_signals = []
        if amount_usd > 10000:
            risk_signals.append(f"Amount ${amount_usd:,.2f} exceeds $10,000 threshold")
        if not account_matches_records and expected_account:
            risk_signals.append("Recipient account does not match verified vendor records")
        if not expected_account:
            risk_signals.append("Recipient account is not in verified vendor records")

        risk_level = "HIGH" if risk_signals else "NORMAL"

        tool_context.request_confirmation(
            hint=f"""
WIRE TRANSFER APPROVAL REQUIRED

Vendor: {recipient_name}
Amount: ${amount_usd:,.2f} USD
Recipient account: {recipient_account[-4:].rjust(len(recipient_account), '*')}
Routing number: {bank_routing[-4:].rjust(len(bank_routing), '*')}
Invoice: {invoice_id}

RISK LEVEL: {risk_level}
{"RISK SIGNALS: " + " | ".join(risk_signals) if risk_signals else "No anomalies detected."}

Verify the vendor, amount, and account match the invoice before approving.
""",
            payload={
                "approved": False,
                "reviewer_notes": "",
                "risk_acknowledged": False if risk_signals else None,
            },
        )
        return {"status": "Pending approval", "invoice_id": invoice_id}

    # Second invocation: process the approval response
    if not tool_confirmation.payload.get("approved"):
        return {
            "status": "rejected",
            "invoice_id": invoice_id,
            "reviewer_notes": tool_confirmation.payload.get("reviewer_notes", ""),
        }

    # For high-risk payments, require explicit risk acknowledgment
    risk_signals = []  # Re-check (same logic as above, omitted for brevity)
    if risk_signals and not tool_confirmation.payload.get("risk_acknowledged"):
        return {
            "status": "rejected",
            "reason": "High-risk payment requires explicit risk acknowledgment",
            "invoice_id": invoice_id,
        }

    # Execute the transfer
    return _execute_transfer(recipient_name, recipient_account, bank_routing, amount_usd)


def _execute_transfer(name, account, routing, amount) -> dict:
    """Execute the actual wire transfer after approval."""
    # Call the payment system API
    return {"status": "transferred", "amount": amount}
