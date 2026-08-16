# Security policy

This repository is a static NetNewsWire bundle plus local Python and shell tooling. It does not provide a hosted service, accept credentials or execute remote code from feed contents.

## Reporting a security problem

For a vulnerability in the validation tools, unsafe input handling or accidental secret exposure, use a private GitHub Security Advisory if that feature is enabled for the repository:

[Open a private security advisory](https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS/security/advisories/new)

Do not publish credentials, private feed URLs or exploit details in a public issue. If private advisories are unavailable, open a non-sensitive issue asking the maintainer for a private contact path.

## Feed and content reports

Broken feeds, stale sources, noisy coverage and profile-budget regressions belong in the public [validation failure issue template](https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS/issues/new?template=validation-failure.md). New source suggestions belong in the [feed request template](https://github.com/ZeroXSHDW/NetNewsWire_iOS_RSS/issues/new?template=feed-request.md).

Never include API keys, account data, personal article exports, digest state or local validation cache files in an issue or pull request.
