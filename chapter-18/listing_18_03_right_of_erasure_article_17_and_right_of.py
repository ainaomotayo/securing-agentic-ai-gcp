#!/usr/bin/env python3
"""
Right of Erasure (Article 17) and Right of Portability (Article 20)
Chapter 18 — Governance Compliance

Companion code for:
  Securing Autonomous AI on Google Cloud
  Omotayo Aina (https://ainaomotayo.com)
  Repository: https://github.com/ainaomotayo/securing-agentic-ai-gcp
"""

async def gdpr_right_of_erasure(
    session_service,
    memory_service,
    artifact_service,
    app_name: str,
    user_id: str,
) -> dict:
    """Erase all data for a user across all ADK data stores. Returns erasure evidence."""
    evidence = {
        "user_id_hash": hashlib.sha256(user_id.encode()).hexdigest(),
        "erasure_timestamp": datetime.utcnow().isoformat(),
        "stores_cleared": [],
    }

    # 1. Delete all sessions for this user
    sessions = await session_service.list_sessions(app_name=app_name, user_id=user_id)
    for session in sessions.sessions:
        await session_service.delete_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session.id,
        )
    evidence["stores_cleared"].append(f"sessions: {len(sessions.sessions)} deleted")

    # 2. Delete memories associated with this user
    if memory_service:
        corpus_name = f"{app_name}_memory_corpus"
        deleted_memories = await purge_user_memories(memory_service, corpus_name, user_id)
        evidence["stores_cleared"].append(f"memories: {deleted_memories} deleted")

    # 3. Delete user-scoped artifacts
    # GCS artifact files in user:/ namespace
    bucket_name = f"{app_name}-artifacts"
    blobs = storage_client.list_blobs(
        bucket_name,
        prefix=f"apps/{app_name}/users/{user_id}/",
    )
    deleted_artifacts = 0
    for blob in blobs:
        blob.delete()
        deleted_artifacts += 1
    evidence["stores_cleared"].append(f"artifacts: {deleted_artifacts} deleted")

    # Log the erasure event to Cloud Logging for GDPR Article 30 records
    logging.getLogger("gdpr").info(json.dumps({
        "event_type": "right_of_erasure",
        "user_id_hash": evidence["user_id_hash"],
        "timestamp": evidence["erasure_timestamp"],
        "stores_cleared": evidence["stores_cleared"],
    }))

    return evidence
