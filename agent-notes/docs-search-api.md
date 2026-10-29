# Document the search API

## Goal

Address issue #4 with a README, search docstring and project README metadata.
Q approved the bounded three-issue plan with "Make it so!" Publication belongs
to the parent; no merge or additional workflow is authorized.

## State

Documentation is implemented locally on docs/search-api, independently of the
session cleanup and timeout branches. No code behavior changed. No tests or
builds ran for this documentation-only change, as instructed.

## Decisions and why

README examples use only the current signature. They install from the repository
because the parent verified the PyPI JSON endpoint returns 404. The documented
defaults, None omission, returned results value, exception propagation and caller
session ownership were checked against this branch's itunes_search.py.
Apple's current Search API documentation confirms podcast searches, parameter
meanings, language values and the documented limit range:
https://performance-partners.apple.com/search-api.
PRs #6 (session cleanup) and #5 (timeout) merged to master before this PR.
Merging master in, the README and docstring now document the keyword-only
timeout and the closing of sessions that search() creates, checked against
master's itunes_search.py.

## Surprises

None beyond the previously verified absence of README and public docstring.

## Next step

Q authorized merging on 2026-10-29. Merge PR #7 after its review gate passes.
There is no hosted CI.
