#!/usr/bin/env bash
# 14.5 Remote Confirmation: Async HITL for Enterprise Workflows
# Chapter 14 — Human In The Loop
#
# Companion code for:
#   Securing Autonomous AI on Google Cloud
#   Omotayo Aina (https://ainaomotayo.com)
#   Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp

set -euo pipefail

curl -X POST http://localhost:8000/run_sse \
  -H "Content-Type: application/json" \
  -d '{
     "app_name": "payment_agent",
     "user_id": "user",
     "session_id": "7828f575-2402-489f-8079-74ea95b6a300",
     "new_message": {
         "parts": [
             {
                 "function_response": {
                     "id": "adk-13b84a8c-c95c-4d66-b006-d72b30447e35",
                     "name": "adk_request_confirmation",
                     "response": {
                         "confirmed": true,
                         "payload": {
                             "approved": true,
                             "reviewer_notes": "Verified against invoice INV-2026-4471",
                             "risk_acknowledged": false
                         }
                     }
                 }
             }
         ],
         "role": "user"
     }
  }'
