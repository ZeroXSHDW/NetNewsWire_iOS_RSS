# GitHub publication guide

This repository is ready to be reviewed for GitHub publication. It contains the manifest, generated NetNewsWire OPML bundles, validation reports, digest-preparation tooling and an automated validation workflow.

## Release goal

Prepare and publish a clean, reproducible GitHub repository for the NetNewsWire Finance + Cyber bundle, with the manifest as the source of truth, all generated artifacts synchronized, offline and live validation passing, no local runtime state or credentials tracked, and clear instructions for importing and maintaining the profiles.

The goal is complete when:

- `make check` and `git diff --check` pass.
- `make validate`, `make validate-lite` and `make validate-air` pass when live network validation is run.
- The generated OPML, source tables, notification matrix and AirDrop handoff match the manifest.
- README, contributing and publishing instructions explain the project without relying on local machine paths.
- The GitHub owner/repository, visibility and license have been explicitly chosen.
- A confirmed `origin` remote is configured and the intended commit or draft PR is pushed deliberately.

The current checkout has no configured Git remote. That is the only repository-connection step still outside this workspace; do not invent a GitHub URL.

## Reusable publishing prompt

Copy and adapt the following prompt for a future release task:

```text
Act as a careful GitHub release engineer for the current checked-out repository.

Objective: prepare and publish this NetNewsWire Finance + Cyber RSS bundle as [PUBLIC OR PRIVATE] repository [OWNER/REPOSITORY]. Preserve the manifest-driven design and publish only an intentional, reproducible change set.

Before writing anything:
1. Inspect git status, the current branch, the full diff, the repository files, and the configured remotes.
2. Treat feed-manifest.json as the source of truth. Regenerate all OPML, source-table, notification-matrix and AirDrop artifacts from it.
3. Run make check, git diff --check, and the three live audits when network access is available.
4. Check for credentials, personal paths, caches, digest state, validation history, lock files and temporary files. Do not publish any of them.
5. Confirm the GitHub owner/repository, visibility, base branch and license with me before creating or using a remote. Do not infer a license.

Publishing rules:
- Preserve unrelated user changes; if the worktree is mixed or the intended scope is unclear, stop and ask.
- Do not reset, delete, force-push, or overwrite user work.
- Create a focused codex/ release branch if the current branch is the default branch and a branch is needed.
- Commit only the reviewed project changes with a concise message.
- Configure origin only after the repository target is confirmed.
- Push with tracking and open a draft PR unless I explicitly ask for a direct release.

Final response: report the files changed, validation results, branch, commit, remote, push result, PR URL, and any remaining decision such as the license.
```

## Safe publishing sequence

After the owner, repository name, visibility and license are confirmed:

```sh
git status -sb
make check
git diff --check
git remote add origin https://github.com/OWNER/REPOSITORY.git
git switch -c codex/github-release
git add .
git commit -m "Prepare NetNewsWire RSS bundle for GitHub"
git push -u origin codex/github-release
```

Review the staged diff before committing. If the repository already has a remote or the intended branch is different, adapt the sequence rather than adding a second remote or pushing to the default branch by assumption. Open a draft pull request after the push when review is desired.

## License decision

No license is included in this repository because selecting one is an ownership and usage-rights decision. GitHub can host the project without a license, but public users should not be given implied reuse rights. Choose and add the intended license before treating the repository as a finished public release.
