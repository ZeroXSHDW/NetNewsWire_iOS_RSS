## Summary

<!-- What changed, and why is it useful? -->

## Scope

- [ ] Feed manifest or profile policy
- [ ] Generated OPML/source tables/notification matrix
- [ ] Digest preparation or Apple Intelligence workflow
- [ ] Validation or CI
- [ ] Documentation only

## Feed changes

<!-- For feed changes, explain the coverage gap, endpoint choice and profile impact. -->

- Coverage gap or reason:
- Direct RSS/Atom endpoint:
- Expected profile impact:
- Notification impact:

## Validation

- [ ] `make check`
- [ ] `git diff --check`
- [ ] `make validate` (when live network validation is available)
- [ ] `make validate-lite` (when live network validation is available)
- [ ] `make validate-air` (when live network validation is available)

## Generated files and repository hygiene

- [ ] Generated artifacts were rebuilt from `feed-manifest.json`.
- [ ] No caches, digest state, lock files, credentials or local paths are included.
- [ ] README and public documentation still describe the current behavior.
- [ ] Any license decision is explicit and intentional.
