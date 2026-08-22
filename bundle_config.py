"""Shared manifest configuration helpers for bundle generation and validation."""

from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


NOTIFICATION_DISPLAY = {
    "on": "**On**",
    "optional": "Optional on",
    "optional-french": "Optional on; French",
    "off": "Off; summarize",
}

VALIDATION_DEFAULTS = {
    "max_age_days": 180.0,
    "duplicate_title_rate_limit": 0.50,
    "min_items_for_noise": 10,
    "stale_review_default_days": 365.0,
    "mobile_review_bytes": 256 * 1024,
    "mobile_large_bytes": 1024 * 1024,
    "mobile_slow_seconds": 2.0,
    "max_response_bytes": 16 * 1024 * 1024,
    "duplicate_story_window_days": 3.0,
    "future_date_tolerance_minutes": 90,
    "validated_max_age_days": 180.0,
}

ITEM_LINK_POLICIES = {"default", "structured-alert", "catalogue-update", "scheduled-calendar"}

REQUIRED_FEED_FIELDS = (
    "id",
    "section",
    "folder",
    "title",
    "url",
    "html_url",
    "purpose",
    "signal_type",
    "access",
    "cadence",
    "validated",
)

REQUIRED_PROFILE_FIELDS = (
    "label",
    "opml_title",
    "note",
    "opml_file",
    "source_table_file",
)

DEVICE_BUDGET_FIELDS = (
    "max_feeds",
    "max_total_payload_bytes",
    "max_single_payload_bytes",
    "max_review_feeds",
    "max_notifications_on",
)

DIGEST_BUDGET_FIELDS = (
    "max_items",
    "max_item_chars",
    "max_total_chars",
    "max_seen_items",
    "duplicate_window_days",
)


class ManifestValidationError(ValueError):
    """A manifest error containing every discovered validation problem."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = tuple(error for error in errors if error)
        super().__init__("; ".join(self.errors) or "manifest validation failed")


def _is_finite_number(value: object) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    return math.isfinite(float(value))


def _is_https_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlsplit(value.strip())
    return parsed.scheme.lower() == "https" and bool(parsed.netloc)


def _canonical_url(value: str) -> str:
    """Canonicalize manifest URLs for duplicate detection."""

    parsed = urlsplit(value.strip())
    if not parsed.scheme or not parsed.netloc:
        return ""
    query = sorted(
        (key, item)
        for key, item in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_")
        and key.lower() not in {"fbclid", "gclid", "mc_cid", "mc_eid"}
    )
    query_text = "&".join(f"{key}={item}" if item else key for key, item in query)
    path = parsed.path.rstrip("/") or "/"
    suffix = f"?{query_text}" if query_text else ""
    return f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}{suffix}"


def load_manifest(path: str | Path) -> dict:
    """Read and structurally validate a manifest for every project consumer."""

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_manifest(data)


def validation_settings(data: dict) -> dict[str, float | int]:
    """Return validated runtime settings with safe defaults for older manifests."""

    raw = data.get("validation", {})
    if not isinstance(raw, dict):
        raise ValueError("manifest validation must be an object")

    settings: dict[str, float | int] = {}
    for key, default in VALIDATION_DEFAULTS.items():
        value = raw.get(key, default)
        if not _is_finite_number(value):
            kind = "an integer" if isinstance(default, int) else "numeric"
            raise ValueError(f"validation.{key} must be {kind}")
        numeric = float(value)
        if numeric <= 0:
            raise ValueError(f"validation.{key} must be positive")
        if isinstance(default, int):
            if numeric != int(numeric):
                raise ValueError(f"validation.{key} must be an integer")
            settings[key] = int(numeric)
        else:
            settings[key] = numeric

    duplicate_limit = settings["duplicate_title_rate_limit"]
    if not 0 <= float(duplicate_limit) <= 1:
        raise ValueError("validation.duplicate_title_rate_limit must be between 0 and 1")
    return settings


def profile_settings(data: dict) -> dict[str, dict]:
    """Return ordered profile definitions from the manifest."""

    raw = data.get("profiles")
    if not isinstance(raw, dict) or not raw:
        raise ValueError("manifest profiles must be a non-empty object")
    profiles: dict[str, dict] = {}
    for name, config in raw.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("profile names must be non-empty strings")
        if not isinstance(config, dict):
            raise ValueError(f"profile configuration must be an object: {name}")
        for key in REQUIRED_PROFILE_FIELDS:
            if not isinstance(config.get(key), str) or not config[key].strip():
                raise ValueError(f"profile {name} is missing {key}")
        if not isinstance(config.get("include_all"), bool):
            raise ValueError(f"profile {name}.include_all must be boolean")
        if "recommended" in config and not isinstance(config["recommended"], bool):
            raise ValueError(f"profile {name}.recommended must be boolean")
        inherits = config.get("inherits", [])
        if not isinstance(inherits, list) or any(
            not isinstance(parent, str) or not parent.strip() for parent in inherits
        ):
            raise ValueError(f"profile {name}.inherits must be a list of profile names")
        device_budget = config.get("device_budget")
        if device_budget is not None:
            if not isinstance(device_budget, dict):
                raise ValueError(f"profile {name}.device_budget must be an object")
            missing = [key for key in DEVICE_BUDGET_FIELDS if key not in device_budget]
            if missing:
                raise ValueError(
                    f"profile {name}.device_budget is missing {', '.join(missing)}"
                )
            for key in DEVICE_BUDGET_FIELDS:
                value = device_budget[key]
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    raise ValueError(
                        f"profile {name}.device_budget.{key} must be a non-negative integer"
                    )
            if device_budget["max_feeds"] == 0:
                raise ValueError(f"profile {name}.device_budget.max_feeds must be positive")
            if device_budget["max_total_payload_bytes"] == 0:
                raise ValueError(
                    f"profile {name}.device_budget.max_total_payload_bytes must be positive"
                )
            if device_budget["max_single_payload_bytes"] == 0:
                raise ValueError(
                    f"profile {name}.device_budget.max_single_payload_bytes must be positive"
                )
            if device_budget["max_single_payload_bytes"] > device_budget["max_total_payload_bytes"]:
                raise ValueError(
                    f"profile {name}.device_budget.max_single_payload_bytes cannot exceed max_total_payload_bytes"
                )
        digest_budget = config.get("digest_budget")
        if digest_budget is not None:
            if not isinstance(digest_budget, dict):
                raise ValueError(f"profile {name}.digest_budget must be an object")
            missing = [key for key in DIGEST_BUDGET_FIELDS if key not in digest_budget]
            if missing:
                raise ValueError(
                    f"profile {name}.digest_budget is missing {', '.join(missing)}"
                )
            for key in DIGEST_BUDGET_FIELDS:
                value = digest_budget[key]
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    raise ValueError(
                        f"profile {name}.digest_budget.{key} must be numeric"
                    )
                if not math.isfinite(float(value)) or float(value) <= 0:
                    raise ValueError(
                        f"profile {name}.digest_budget.{key} must be positive and finite"
                    )
            for key in DIGEST_BUDGET_FIELDS[:-1]:
                value = digest_budget[key]
                if not isinstance(value, int) or isinstance(value, bool):
                    raise ValueError(
                        f"profile {name}.digest_budget.{key} must be an integer"
                    )
        profiles[name] = config
    for name, config in profiles.items():
        for parent in config.get("inherits", []):
            if parent not in profiles:
                raise ValueError(f"profile {name} inherits unknown profile {parent}")
            if parent == name:
                raise ValueError(f"profile {name} cannot inherit itself")

    def visit(name: str, stack: tuple[str, ...] = ()) -> None:
        if name in stack:
            cycle = " -> ".join((*stack, name))
            raise ValueError(f"profile inheritance cycle: {cycle}")
        for parent in profiles[name].get("inherits", []):
            visit(parent, (*stack, name))

    for name in profiles:
        visit(name)
    return profiles


def profile_config(data: dict, profile: str) -> dict:
    profiles = profile_settings(data)
    if profile not in profiles:
        raise ValueError(f"unknown profile: {profile}")
    return profiles[profile]


def profile_device_budget(config: dict) -> dict[str, int]:
    """Return a validated device budget, or an empty mapping when unconfigured."""

    raw = config.get("device_budget")
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError("profile device_budget must be an object")
    return {key: int(raw[key]) for key in DEVICE_BUDGET_FIELDS}


def profile_digest_budget(config: dict) -> dict[str, int | float]:
    """Return a validated digest budget, or an empty mapping when unconfigured."""

    raw = config.get("digest_budget")
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError("profile digest_budget must be an object")
    return {
        key: (int(raw[key]) if key != "duplicate_window_days" else float(raw[key]))
        for key in DIGEST_BUDGET_FIELDS
    }


def profile_inheritance(data: dict, profile: str) -> tuple[str, ...]:
    """Return inherited profiles in parent-first order."""

    profiles = profile_settings(data)
    if profile not in profiles:
        raise ValueError(f"unknown profile: {profile}")
    ordered: list[str] = []
    seen: set[str] = set()

    def visit(name: str) -> None:
        for parent in profiles[name].get("inherits", []):
            if parent not in seen:
                visit(parent)
                seen.add(parent)
                ordered.append(parent)

    visit(profile)
    return tuple(ordered)


def profile_includes_feed(data: dict, profile: str, feed: dict) -> bool:
    """Return whether a feed is selected directly or through profile inheritance."""

    profiles = profile_settings(data)
    names = (profile, *profile_inheritance(data, profile))
    return any(
        profiles[name]["include_all"] or feed.get("profiles", {}).get(name, False)
        for name in names
    )


def item_link_policy(feed: dict) -> str:
    """Return the explicit per-feed item-link policy."""

    policy = str(feed.get("item_link_policy", "default") or "default").strip().lower()
    if policy not in ITEM_LINK_POLICIES:
        raise ValueError(f"invalid item_link_policy: {policy}")
    return policy


def manifest_errors(
    data: object,
    *,
    today: date | None = None,
    check_dates: bool = False,
    require_validation_fields: bool = False,
) -> list[str]:
    """Collect structural and cross-field manifest errors without raising early."""

    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest root must be an object"]

    version = data.get("manifest_version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        errors.append("manifest_version must be a positive integer")

    try:
        profiles = profile_settings(data)
    except ValueError as exc:
        errors.append(str(exc))
        profiles = {}

    include_all_profiles = [
        name for name, config in profiles.items() if config.get("include_all") is True
    ]
    if len(include_all_profiles) != 1:
        errors.append("profiles must contain exactly one include_all profile")
    recommended_profiles = [
        name for name, config in profiles.items() if config.get("recommended") is True
    ]
    if len(recommended_profiles) != 1:
        errors.append("profiles must contain exactly one recommended profile")

    validation = data.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")
        validation = {}
        settings = dict(VALIDATION_DEFAULTS)
    else:
        settings = dict(VALIDATION_DEFAULTS)
        for key, default in VALIDATION_DEFAULTS.items():
            try:
                checked = validation_settings({"validation": {key: validation.get(key, default)}})
            except ValueError as exc:
                errors.append(str(exc))
            else:
                settings[key] = checked[key]
    if require_validation_fields:
        for key in VALIDATION_DEFAULTS:
            if key not in validation:
                errors.append(f"validation.{key} must be explicitly configured")
    validated_max_age_days = float(
        settings.get("validated_max_age_days", VALIDATION_DEFAULTS["validated_max_age_days"])
    )

    feeds = data.get("feeds")
    if not isinstance(feeds, list) or not feeds:
        errors.append("feeds must be a non-empty array")
        return errors

    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    seen_canonical_urls: set[str] = set()
    for index, feed in enumerate(feeds, start=1):
        if not isinstance(feed, dict):
            errors.append(f"feed {index} is not an object")
            continue

        feed_id = feed.get("id") if isinstance(feed.get("id"), str) else ""
        label = feed_id or f"feed {index}"
        for key in REQUIRED_FEED_FIELDS:
            value = feed.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}: feed is missing required field {key!r}")

        if feed_id:
            if feed_id in seen_ids:
                errors.append(f"duplicate feed id: {feed_id}")
            seen_ids.add(feed_id)

        feed_url = feed.get("url", "")
        html_url = feed.get("html_url", "")
        if not _is_https_url(feed_url):
            errors.append(f"{label}: feed URL must be HTTPS")
        if not _is_https_url(html_url):
            errors.append(f"{label}: html_url must be HTTPS")
        if isinstance(feed_url, str):
            if feed_url in seen_urls:
                errors.append(f"duplicate feed URL: {feed_url}")
            seen_urls.add(feed_url)
            canonical_url = _canonical_url(feed_url)
            if canonical_url and canonical_url in seen_canonical_urls:
                errors.append(f"duplicate canonical feed URL: {feed_url}")
            if canonical_url:
                seen_canonical_urls.add(canonical_url)

        if not isinstance(feed.get("event_driven"), bool):
            errors.append(f"{label}: event_driven must be boolean")
        elif feed["event_driven"]:
            if not isinstance(feed.get("freshness_reason"), str) or not feed["freshness_reason"].strip():
                errors.append(f"{label}: event-driven feed needs freshness_reason")
            stale_days = feed.get("stale_review_days")
            if not _is_finite_number(stale_days) or float(stale_days) <= 0:
                errors.append(f"{label}: event-driven feed needs positive stale_review_days")

        date_timezone = feed.get("date_timezone")
        if date_timezone is not None:
            if not isinstance(date_timezone, str) or not date_timezone.strip():
                errors.append(f"{label}: date_timezone must be a non-empty IANA timezone name")
            else:
                try:
                    ZoneInfo(date_timezone)
                except ZoneInfoNotFoundError:
                    errors.append(f"{label}: date_timezone must be a valid IANA timezone name")

        future_date_tolerance = feed.get("future_date_tolerance_minutes")
        future_date_reason = feed.get("future_date_reason")
        if future_date_tolerance is None:
            if future_date_reason is not None:
                errors.append(f"{label}: future_date_reason needs future_date_tolerance_minutes")
        else:
            tolerance_valid = _is_finite_number(future_date_tolerance) and float(future_date_tolerance) > 0
            if not tolerance_valid:
                errors.append(
                    f"{label}: future_date_tolerance_minutes must be a positive finite number"
                )
            if future_date_reason is not None and (
                not isinstance(future_date_reason, str) or not future_date_reason.strip()
            ):
                errors.append(f"{label}: future_date_reason must be a non-empty string")
            if tolerance_valid and float(future_date_tolerance) > float(
                settings["future_date_tolerance_minutes"]
            ) and (not isinstance(future_date_reason, str) or not future_date_reason.strip()):
                errors.append(
                    f"{label}: feed-specific future-date tolerance needs future_date_reason"
                )

        if feed.get("notification") not in NOTIFICATION_DISPLAY:
            errors.append(f"{label}: invalid notification policy")
        try:
            item_link_policy(feed)
        except ValueError as exc:
            errors.append(f"{label}: {exc}")

        validated = feed.get("validated")
        if isinstance(validated, str):
            try:
                validated_date = date.fromisoformat(validated)
            except ValueError:
                errors.append(f"{label}: validated must be YYYY-MM-DD")
            else:
                if check_dates:
                    current_date = today or date.today()
                    if validated_date > current_date:
                        errors.append(f"{label}: validated date is in the future")
                    elif (current_date - validated_date).days > validated_max_age_days:
                        errors.append(f"{label}: validated date is older than the configured review window")

        feed_profiles = feed.get("profiles", {})
        if not isinstance(feed_profiles, dict):
            errors.append(f"{label}: profiles must be an object")
        else:
            for profile, enabled in feed_profiles.items():
                if not isinstance(profile, str) or not isinstance(enabled, bool):
                    errors.append(f"{label}: profile flags must be string/boolean pairs")
                elif profile not in profiles:
                    errors.append(f"{label}: unknown profile flag {profile}")

    if profiles and include_all_profiles and all(isinstance(feed, dict) for feed in feeds):
        all_profile = include_all_profiles[0]
        all_urls = {str(feed.get("url", "")) for feed in feeds}
        for profile, config in profiles.items():
            if config["include_all"]:
                selected_urls = all_urls
            else:
                selected_urls: set[str] = set()
                for feed in feeds:
                    if profile_includes_feed(data, profile, feed):
                        selected_urls.add(str(feed.get("url", "")))
            if not selected_urls:
                errors.append(f"{profile} profile contains no feeds")
            if not config["include_all"] and not selected_urls <= all_urls:
                errors.append(f"{profile} contains a feed outside {all_profile}")

    return errors


def validate_manifest(
    data: object,
    *,
    check_dates: bool = False,
    require_validation_fields: bool = False,
) -> dict:
    """Validate a manifest and raise one controlled error containing all findings."""

    errors = manifest_errors(
        data,
        check_dates=check_dates,
        require_validation_fields=require_validation_fields,
    )
    if errors:
        raise ManifestValidationError(errors)
    return data  # type: ignore[return-value]
