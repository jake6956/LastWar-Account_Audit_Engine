"""Deterministic model for LWAI automatic consumer engine updates."""
from __future__ import annotations

from dataclasses import dataclass

ENGINE_FRESHNESS_TTL_HOURS = 6


def version_key(value: str) -> tuple[int, ...]:
    date_part, release_part = value.rsplit(".", 1)
    year, month, day = (int(x) for x in date_part.split("-"))
    return year, month, day, int(release_part)


@dataclass
class EngineMetadata:
    installed_engine_version: str
    last_known_good_engine_version: str
    last_successful_update_check: float | None = None
    last_successful_engine_update: float | None = None
    update_policy: str = "AUTOMATIC"
    update_health: str = "HEALTHY"
    last_update_error_summary: str | None = None


@dataclass(frozen=True)
class Candidate:
    version: str
    channel: str = "Production"
    sanitized: bool = True
    account_state_included: bool = False
    engine_api_compatible: bool = True
    workspace_compatible: bool = True
    migration_chain_valid: bool = True
    integrity_valid: bool = True
    health_check_valid: bool = True


@dataclass(frozen=True)
class UpdateResult:
    checked: bool
    updated: bool
    active_version: str
    resumed_action: str
    degraded: bool = False


def should_auto_check(
    *,
    web_available: bool,
    startup: bool = False,
    reload: bool = False,
    schema_sensitive: bool = False,
    consequential: bool = False,
    hours_since_last_success: float | None = None,
    force: bool = False,
) -> bool:
    if not web_available:
        return False
    if force or startup or reload or schema_sensitive:
        return True
    if not consequential:
        return False
    if hours_since_last_success is None:
        return True
    return hours_since_last_success >= ENGINE_FRESHNESS_TTL_HOURS


def candidate_is_acceptable(current_version: str, candidate: Candidate) -> bool:
    if candidate.channel != "Production":
        return False
    if not candidate.sanitized or candidate.account_state_included:
        return False
    if not (
        candidate.engine_api_compatible
        and candidate.workspace_compatible
        and candidate.migration_chain_valid
        and candidate.integrity_valid
        and candidate.health_check_valid
    ):
        return False
    return version_key(candidate.version) > version_key(current_version)


def run_update_transaction(
    *,
    metadata: EngineMetadata,
    candidate: Candidate | None,
    original_action: str,
    now: float,
    check_required: bool,
) -> UpdateResult:
    """Adopt only a fully verified newer Production candidate; preserve last-known-good otherwise."""
    if not check_required:
        return UpdateResult(False, False, metadata.installed_engine_version, original_action)

    current = metadata.installed_engine_version
    if candidate is None:
        metadata.update_health = "DEGRADED"
        metadata.last_update_error_summary = "canonical update verification unavailable"
        return UpdateResult(True, False, current, original_action, degraded=True)

    if version_key(candidate.version) <= version_key(current):
        metadata.last_successful_update_check = now
        metadata.update_health = "HEALTHY"
        metadata.last_update_error_summary = None
        return UpdateResult(True, False, current, original_action)

    if not candidate_is_acceptable(current, candidate):
        metadata.update_health = "DEGRADED"
        metadata.last_update_error_summary = "candidate failed Production verification"
        return UpdateResult(True, False, metadata.last_known_good_engine_version, original_action, degraded=True)

    metadata.installed_engine_version = candidate.version
    metadata.last_known_good_engine_version = candidate.version
    metadata.last_successful_update_check = now
    metadata.last_successful_engine_update = now
    metadata.update_health = "HEALTHY"
    metadata.last_update_error_summary = None
    return UpdateResult(True, True, candidate.version, original_action)
