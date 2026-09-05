# 50-Persona Audit — Round 1

Date: 2026-09-06
Protocol: `Reese-max/autodev-ng/docs/portfolio-audit/2026-09-06-50-persona-audit.md`

> Fixed 50-persona model simulation plus repository evidence review; not 50 human participants.

## Round 1 result

Status: **STATIC PASS / REDIRECT RUNTIME-PENDING — NOT CLEAN**

No new reproducible P0/P1/P2 finding was confirmed from the current static evidence.

The repository now has a clear compatibility-only contract: all authoritative question data/features live in `police-exam-archive`, while this repository preserves legacy URLs and forwards users to the canonical quiz/site. This addresses the historical two-source drift risk rather than duplicating the question bank.

## Evidence reviewed

- README explicitly identifies the canonical repository and public entry points.
- Query string and URL hash preservation are part of the compatibility contract.
- Pull requests are expected to pass `Fusion compatibility check`.
- The old monolithic site is retained only in Git history, not as a competing live data source.

## Fixed-persona scenarios still requiring runtime evidence

- A01/A04: legacy links reach the expected canonical destination.
- I01/I05: query/hash parameters survive redirects and malformed parameters fail safely.
- G05: redirect does not introduce unnecessary loops or large compatibility payloads.
- H05: a maintainer can verify canonical-vs-compatibility ownership from a clean checkout.

## CLEAN gate

1. Execute the compatibility test suite and real redirect checks for representative old URLs/query/hash combinations.
2. Re-run the fixed personas on current/recent code.
3. Require two consecutive rounds with no new P0/P1/P2 before CLEAN.

## Runtime status

**Pending.** This Round 1 did not browse the deployed legacy URL or execute the redirect tests.

---

# Round 2 continuation — 2026-09-06

Status: **NO NEW P0/P1/P2 / REDIRECT RUNTIME-PENDING — NOT CLEAN**

No compatibility-code change landed after the Round 1 audit commit. The static redirect contract was rechecked:

- the JavaScript target copies `window.location.search` and `window.location.hash` to the canonical `quiz.html` URL before `location.replace()`;
- the visible fallback link is updated to the same preserved target;
- the repository contains no competing question-bank copy in the live page.

The HTML `meta refresh` fallback points to the canonical quiz without query/hash. That difference matters only if the JavaScript compatibility path does not execute; it is recorded as a low-frequency fallback limitation rather than promoted to P0/P1/P2 without evidence that supported clients depend on script-disabled redirect state.

## CLEAN status

Still **NOT CLEAN**. Representative deployed legacy URLs, malformed parameters, redirect-loop behavior and query/hash preservation still require real browser/runtime verification before the two-round CLEAN condition can be satisfied.