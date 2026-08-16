#!/usr/bin/env python3
"""Validate the feed manifest and prove generated artifacts are reproducible."""

from __future__ import annotations

import argparse
import importlib.util
import json
import tempfile
from pathlib import Path

from bundle_config import manifest_errors, profile_settings


def load_generator_module():
    path = Path(__file__).with_name("generate-bundle.py")
    spec = importlib.util.spec_from_file_location("generate_bundle", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load generator module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_manifest(data: dict, errors: list[str], generator) -> None:
    errors.extend(
        manifest_errors(
            data,
            check_dates=True,
            require_validation_fields=True,
        )
    )


def compare_generated_artifacts(data: dict, root: Path, errors: list[str], generator) -> None:
    artifacts = [
        (
            profile,
            root / config["opml_file"],
            root / config["source_table_file"],
        )
        for profile, config in profile_settings(data).items()
    ]
    with tempfile.TemporaryDirectory(prefix="nnw-manifest-lint-") as temporary:
        temporary_root = Path(temporary)
        for profile, committed_opml, committed_table in artifacts:
            feeds = generator.selected_feeds(data, profile)
            generated_opml = temporary_root / f"{profile}.opml"
            generated_table = temporary_root / f"{profile}.md"
            generator.write_opml(data, feeds, generated_opml, profile)
            generator.write_source_table(data, feeds, generated_table, profile)
            for generated, committed in ((generated_opml, committed_opml), (generated_table, committed_table)):
                if not committed.exists():
                    errors.append(f"missing generated artifact: {committed.name}")
                elif generated.read_bytes() != committed.read_bytes():
                    errors.append(f"generated artifact is stale: {committed.name}")

        generated_matrix_md = temporary_root / "notifications.md"
        generated_matrix_json = temporary_root / "notifications.json"
        generator.write_notification_matrix(data, generated_matrix_md)
        generator.write_notification_json(data, generated_matrix_json)
        for generated, committed in (
            (generated_matrix_md, root / "NetNewsWire-Notification-Profile.md"),
            (generated_matrix_json, root / "NetNewsWire-Notification-Profile.json"),
        ):
            if not committed.exists():
                errors.append(f"missing generated artifact: {committed.name}")
            elif generated.read_bytes() != committed.read_bytes():
                errors.append(f"generated artifact is stale: {committed.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("feed-manifest.json"))
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    errors: list[str] = []
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("manifest root must be an object")
        generator = load_generator_module()
        check_manifest(data, errors, generator)
        if not errors:
            compare_generated_artifacts(data, args.root, errors, generator)
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"manifest-lint failed errors={len(errors)}")
        return 1
    feeds = len(data.get("feeds", []))
    profile_counts = " ".join(
        f"{profile}={len(generator.selected_feeds(data, profile))}"
        for profile in profile_settings(data)
    )
    print(f"manifest-lint passed feeds={feeds} {profile_counts} generated-artifacts=verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
