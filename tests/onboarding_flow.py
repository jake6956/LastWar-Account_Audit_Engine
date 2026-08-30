"""Executable high-level onboarding continuity model for LWAI release gates.

This wraps low-level provider recheck primitives with the user-facing handoff contract.
"""
from __future__ import annotations

from reference_runtime import ProviderCapabilities


INFRASTRUCTURE_ONLY_TERMINALS = {
    "recheck_storage_capabilities",
    "locate_or_create_private_workspace",
    "verify_private_workspace",
    "cloud_storage_connected_and_verified",
    "account_loaded",
    "account_created",
    "migration_complete",
    "update_complete",
    "ready",
}


def storage_authorization_return_steps(
    capabilities: ProviderCapabilities,
    *,
    existing_user: bool = False,
    later_persistence_upgrade: bool = False,
) -> list[str]:
    """A returned `connected` message always resolves to a user-visible next state."""
    steps = ["recheck_storage_capabilities"]
    if not capabilities.can_durable_persist:
        return steps + ["storage_verification_failed_offer_retry_other_provider_or_session_only"]

    steps.extend(["locate_or_create_private_workspace", "verify_private_workspace"])
    if later_persistence_upgrade:
        return steps + ["resume_original_user_action"]
    if existing_user:
        return steps + ["existing_account_recovery", "user_facing_loaded_account_resume_or_question"]
    return steps + ["persist_identity_pending", "new_account_guidance"]


ONBOARDING_STAGE_ACTIONS = {
    "PERSISTENCE_DECISION": "ask_cloud_yes_or_no",
    "PROVIDER_SELECTION": "ask_provider_choice",
    "AUTHORIZATION_WAIT": "finish_connection_then_reply_connected",
    "IDENTITY_PENDING": "ask_identity_block",
    "BASELINE_PENDING": "ask_strategic_baseline",
    "FIRST_EVIDENCE_PENDING": "request_first_account_evidence",
    "RUNNING": "resume_pending_objective_or_ask_what_to_work_on",
}


def resume_user_action(stage: str, *, pending_user_input: str | None = None) -> str:
    """Translate durable onboarding/recovery state into the next visible user action."""
    if stage == "WAITING_USER":
        if not pending_user_input:
            raise ValueError("WAITING_USER requires explicit pending_user_input")
        return pending_user_input
    try:
        return ONBOARDING_STAGE_ACTIONS[stage]
    except KeyError as exc:
        raise ValueError(f"unsupported onboarding stage: {stage}") from exc


def terminal_is_user_visible_action(steps: list[str]) -> bool:
    if not steps:
        return False
    return steps[-1] not in INFRASTRUCTURE_ONLY_TERMINALS
