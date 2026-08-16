# Contributing

This repository is a manifest-driven NetNewsWire bundle with small standard-library validation tools. Keep the source data, generated subscription files and validation rules aligned.

## Source of truth

Edit `feed-manifest.json` for feed identity, folder placement, profile membership, freshness policy, notification policy and device/digest budgets. Do not hand-edit generated OPML, source tables or the notification matrix.

After a manifest change, regenerate everything with:

```sh
make package
```

The `AirDrop/` copy is a generated handoff artifact for the recommended iPhone Air profile.

## Required checks

Run the offline gate before opening a pull request:

```sh
make check
git diff --check
```

When network access is available, run all live profile audits as well:

```sh
make validate
make validate-lite
make validate-air
```

Live reports are Dublin-time snapshots. Review failed feeds, metadata mismatches, stale-review deadlines, future-dated items, noisy feeds, drift warnings and device-budget failures before committing refreshed reports.

## Adding or changing a feed

1. Document the coverage gap or operational reason in `Coverage-Gap-Assessment.md`.
2. Use a direct, public HTTPS RSS or Atom endpoint; keep the HTML page in `html_url`.
3. Record the feed’s purpose, signal type, access model, cadence, validation date and profile membership in the manifest.
4. Regenerate the artifacts and inspect the source table and notification matrix.
5. Run the deterministic and live checks that apply to the change.

Do not add HTML pages, placeholder URLs, private feeds, API-key URLs or duplicate endpoints as RSS sources.

## Pull requests

Explain what changed, why the source or rule is appropriate, which generated artifacts changed, and which checks passed. Do not commit local caches, digest state, validation history, lock files, temporary files or credentials.

The repository does not currently declare a license. Choose one with the project owner before public publication; do not infer or add a license as part of an unrelated feed change.
