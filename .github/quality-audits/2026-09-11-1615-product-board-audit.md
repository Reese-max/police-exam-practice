# Product Board Audit — 2026-09-11 16:15 (Asia/Taipei)

> Scope: incremental regression audit of `Reese-max/police-exam-practice`.
> Evidence labels: **CONFIRMED** = repository/CI evidence; **LIKELY** = static inference; **UNKNOWN** = requires runtime, owner, or user evidence.
> The 50-persona work below is a **synthetic simulation**, not human research, market share, or observed behavior.

## Executive Summary

**Decision: MAINTAIN / SIMPLIFY.** This repository is no longer an independent exam product; it is a deliberately small compatibility shell that sends legacy URLs to the canonical `police-exam-archive` quiz. Its highest-value job is therefore lossless, honest redirection—not feature growth.

One Quality-Gate finding remains **STILL REPRODUCIBLE / NEEDS_RUNTIME_VERIFICATION** and maps to the existing open [#3](https://github.com/Reese-max/police-exam-practice/issues/3). The JavaScript path preserves query and hash state, but the timed `meta refresh` and initial static link do not. README and manifest promises remain unconditional. No product-code commit has landed since the previous audit; successful CI and Pages deployment demonstrate the current implementation was built, not that the no-JavaScript preservation promise is true.

CEO top three:

1. Complete #3 with a non-destructive no-JavaScript fallback and executable regression contract.
2. Keep `police-exam-archive` as the sole owner of exam data, practice UX, and future learning features.
3. Maintain a retirement contract for this legacy entry point: minimal surface, no tracking, no duplicate product logic.

Do not build accounts, AI tutoring, spaced repetition, analytics, a backend, a native app, or another quiz UI here.

## Project Discovery

### Product, users, and job

- **CONFIRMED — repository/code:** a static legacy compatibility entry point whose only product task is redirecting users to `https://reese-max.github.io/police-exam-archive/quiz.html`.
- **CONFIRMED — README/manifest:** the public contract promises preservation of query strings and URL fragments.
- **CONFIRMED — code:** inline JavaScript constructs `targetUrl + window.location.search + window.location.hash` and calls `window.location.replace()`.
- **CONFIRMED — code:** `meta refresh` and the initial `continue-link` use the bare target URL.
- **CONFIRMED — tests:** nine source-contract tests assert the JavaScript preservation strings, canonical/noindex metadata, a visible fallback, and no external dependencies. They do not assert safe behavior when JavaScript is unavailable.
- **CONFIRMED — CI:** Fusion compatibility run [#7](https://github.com/Reese-max/police-exam-practice/actions/runs/34273586849) and Pages deployment [#7](https://github.com/Reese-max/police-exam-practice/actions/runs/34273585490) succeeded for `07144e944ba12fcae81054321ab94a030e9ae183`.
- **CONFIRMED — history:** the default branch remains at that audit-only SHA; no product-code change has addressed #3 since the 2026-09-09 audit.
- **LIKELY — static inference:** users with JavaScript disabled or blocked, restrictive webviews, interrupted script execution, or assistive workflows that activate the link before script mutation can lose deep-link state.
- **UNKNOWN — runtime:** actual legacy traffic, JavaScript-disabled behavior across browsers/webviews, encoded or malformed URL handling, and assistive-technology announcements. No live browser, CLI, API, or human usability test was performed this round.

### Maturity and value

Maturity is **maintenance/compatibility mode**. The principal value is preserving old bookmarks and links while eliminating duplicated exam data and UX. The maximum weakness is a contract that is correct only on the primary JavaScript path but is documented as unconditional.

### Repository activity, Issues, PRs, Actions

- Open root issue: #3 (same fingerprint as this finding).
- Open pull requests: none at the write checkpoints.
- No `github-3` branch was present. Residual integration/fusion and Claude branches were last updated in March or August 2026 and did not show an active issue goal.
- Historical #3 lock was released. This audit acquired a new 90-minute product-board lease and re-read comments before writing.
- Actions are green for the existing contract; no evidence supports calling #3 fixed.

## Competitive Intelligence

Sources rechecked on **2026-09-11**:

- Canonical first-party replacement: [police-exam-archive](https://github.com/Reese-max/police-exam-archive)
- Official source: [考選部試題查詢](https://wwwq.moex.gov.tw/exam/wFrmExamQandASearch.aspx)
- Direct preparation platform: [阿摩線上測驗](https://play.google.com/store/apps/details?id=com.yamol.exam&hl=zh_TW)
- General study platform: [Quizlet](https://play.google.com/store/apps/details?id=com.quizlet.quizletandroid&hl=zh_TW)
- Spaced-repetition substitute: [Anki](https://apps.ankiweb.net/)

Public product details and dates can change; this matrix reflects the linked official/product pages as checked on 2026-09-11.

| Dimension | Compatibility shell | Canonical archive | MOEX | Yamol | Quizlet | Anki |
|---|---|---|---|---|---|---|
| Target user | Holder of a legacy link | Taiwan police-exam learner | Candidate seeking official papers | Exam-prep community | General learners | Self-directed power users |
| Value proposition | Preserve access during consolidation | Search and practice one maintained corpus | Authoritative source PDFs | Large social question bank | Fast study-set creation and practice | Durable customizable recall |
| Core / killer feature | Lossless redirect | First-party corpus + quiz | Official provenance | Community scale | Cross-device study modes | Scheduling and extensibility |
| Onboarding / UX | Zero-account, one hop | Direct web access | Form/PDF workflow | Account/app-led | Polished account-led | Setup-heavy, powerful |
| Automation / AI | None—and should stay none | Product-owned only | None | Platform features | Adaptive/scoring features | Scheduling, add-ons |
| Integrations / API | URL contract only | Shared data/product owner | Linkable official documents | Closed platform | Sharing/app ecosystem | Add-ons/sync/export |
| Mobile | Browser redirect | Responsive web intent | Web/PDF | Android/iOS distribution | Android/iOS/web | Desktop/mobile ecosystem |
| Performance | Tiny and dependency-free | Larger application | Document service | App/network dependent | App/network dependent | Strong local workflow |
| Reliability | Simple, but fallback state loss | Must own end-to-end contract | Authority, limited practice UX | Third-party service dependency | Third-party service dependency | Local durability depends on setup |
| Security / privacy | No account or tracking | First-party static posture | Government service | Listing declares data practices | Listing declares collection/sharing | Local-first options plus sync choices |
| Pricing | Free | Free | Free | Ads / in-app purchases | Freemium / Plus | Desktop free; platform-specific clients |
| Open / closed | Public repository | Public repository | Public service | Closed product | Closed product | Open-source core/community |
| Community / docs | Minimal by design | Repository documentation | Official notices | Large exam community | Very large global distribution | Mature open community/docs |
| Distribution | Legacy links/search | GitHub Pages/current links | Official search | App stores/web | App stores/web | Official downloads/app stores |
| Typical strength | Smallest migration surface | Product ownership | Authority | Breadth/social proof | Convenience and polish | Control and longevity |
| Typical weakness | Cannot be a study product | Must maintain data trust | Weak practice loop | Ads/account/privacy tradeoffs | Generic and platform-dependent | Learning curve |

### Gap classification

- **MUST MATCH:** redirects must never silently discard meaningful legacy URL state; documentation and executable behavior must agree.
- **SHOULD BE BETTER:** remain faster, smaller, account-free, tracking-free, and easier to reason about than a general study platform.
- **DIFFERENTIATOR:** a stable preservation contract for historical links while one canonical repository owns the product.
- **DO NOT COPY:** social feeds, AI tutor, content creation, subscriptions, gamification, analytics, cloud accounts, or native apps. Those features conflict with the shell’s job.

## Virtual Executive Board

| Role | Question | Opportunity | Priority |
|---|---|---|---|
| CEO | Does this repository still earn its maintenance cost? | Make it a trustworthy bridge, then keep it nearly frozen. | Finish #3; avoid product expansion. |
| CPO | Is the promise the same in every execution mode? | Define one legacy-link preservation contract. | Align README, manifest, HTML, and tests. |
| CTO | Can the behavior be proven without a browser-specific assumption? | Prefer standards-based, dependency-free fallback behavior. | Add a deterministic no-JS contract test. |
| Staff / Principal Engineer | What is the root cause rather than each symptom? | Remove parameter-dropping fallback paths, not merely wording. | One root issue, no duplicate symptoms. |
| UX Lead | What does a user see when automation fails? | Provide an honest, operable continuation path. | Clear `noscript` guidance and preserved destination. |
| UX Researcher | Who actually arrives through deep links? | Measure only if privacy-safe and decision-changing. | Do not add analytics by default; runtime scenarios first. |
| Growth Lead | Could the shell capture or market to traffic? | Preserve trust and transfer users cleanly. | No funnel experiments in the legacy shell. |
| CFO / Business Analyst | What is the cheapest reliable architecture? | A static page with one contract and minimal upkeep. | Avoid backend, account, and app costs. |
| Security / Privacy Lead | Does migration introduce data collection? | Keep the shell credential-free and tracking-free. | Reject telemetry and third-party scripts. |
| QA Lead | Which boundary is untested? | Encode JavaScript-disabled and malformed/encoded URL cases. | Regression matrix before closing #3. |
| SRE Lead | What does green deployment actually prove? | Separate deploy success from behavioral acceptance. | Keep #3 open until scenario evidence passes. |
| Accessibility Specialist | Can non-pointer and assistive users understand the transition? | Use semantic, focusable fallback content. | Keyboard/screen-reader runtime check after change. |
| Customer Support Lead | Can support explain where state went? | Make the destination and limitations explicit. | Never silently drop filters or question anchors. |

### Cross-review and minority opinion

The board agrees that the shell should remain minimal and that #3 is the only current Quality-Gate finding. The Growth Lead’s minority opinion is to add privacy-preserving legacy-traffic measurement before eventual archival. The Security/Privacy Lead and CFO reject that by default: traffic data is not currently required to repair the known contract, and instrumentation would create a new operating surface. Revisit only if an explicit archive decision depends on traffic evidence.

A second minority view is to remove query/hash preservation from documentation instead of implementing it. CPO, Support, and Staff Engineering reject that shortcut because preservation is the repository’s core migration value and the JavaScript implementation already establishes user intent.

## 50 Synthetic Personas

Thirty personas are regression-baseline archetypes; twenty rotate edge contexts. Each journey is a modelled scenario, **not an observed session or human interview**.

| # | Cohort / background | Goal & expectation | Task / journey | Friction / outcome / comment | Severity | Suggestion |
|---:|---|---|---|---|---|---|
| 1 | Baseline, police candidate, Android, average skill | Resume filtered law practice | Open old `?subject=police-law` bookmark | JS path preserves state; likely success | Low | Keep JS contract tested |
| 2 | Baseline, candidate, iPhone | Return to question 12 | Open `#question-12` legacy link | JS path likely succeeds | Low | Test hash transfer |
| 3 | Baseline, desktop Chrome power user | Resume filter and anchor | Open query+hash bookmark | JS concatenation appears correct | Low | Keep representative test |
| 4 | Baseline, first-time visitor | Understand migration | Open bare legacy URL | Visible message then redirect | Low | Keep plain-language destination |
| 5 | Baseline, low digital skill | Continue without choices | Open shared bare link | Automatic hop is simple | Low | Avoid new controls |
| 6 | Baseline, slow mobile network | Reach current quiz quickly | Load tiny static page | Dependency-free shell is resilient | Low | Preserve tiny bundle |
| 7 | Baseline, school Wi-Fi | Use an old QR code | Open legacy path | Likely reaches canonical quiz | Low | Maintain stable Pages URL |
| 8 | Baseline, privacy-sensitive user | Avoid account/tracking | Follow old link | No external dependency confirmed | Low | Do not add analytics |
| 9 | Baseline, returning candidate | Reuse subject bookmark | Open query link | Primary path succeeds | Low | Regression-test parameters |
| 10 | Baseline, desktop Firefox | Continue study | Open bare link | Likely success | Low | Cross-browser smoke after fix |
| 11 | Baseline, Edge on managed PC | Follow departmental bookmark | Open policy-filter link | Script policy may be restrictive; unknown | Medium | Safe no-JS fallback |
| 12 | Baseline, Android WebView | Open chat-shared deep link | In-app browser loads page | Script execution unknown | Medium | Test representative webview |
| 13 | Baseline, iOS webview | Resume anchored item | Open message deep link | Hash loss possible if script blocked | Medium | Preserve link without JS |
| 14 | Baseline, candidate using reader mode | Understand destination | Open and simplify page | Timed refresh may pre-empt reading | Medium | Honest semantic fallback |
| 15 | Baseline, keyboard-only user | Activate continuation link | Tab then Enter | Initial href lacks state before mutation | Medium | Make fallback intrinsically correct |
| 16 | Baseline, screen-reader user | Hear migration and continue | Navigate heading/link | Announcement behavior unverified | Medium | Runtime AT verification |
| 17 | Baseline, JavaScript disabled | Keep subject selection | Open query bookmark | Meta refresh drops state; simulated failure | High | Remove destructive timed refresh |
| 18 | Baseline, script blocked by policy | Keep question anchor | Open hash bookmark | Static href drops anchor; simulated failure | High | Non-JS preserved destination/guidance |
| 19 | Baseline, script interrupted | Continue manually | Activate link before mutation | Race can use bare href; likely failure | Medium | Eliminate mutable-only correctness |
| 20 | Baseline, offline then reconnect | Reach canonical quiz | Reload old link | Shell itself tiny; target requires network | Medium | Clear retry/target URL |
| 21 | Baseline, copied URL with query | Share exact practice state | Recipient opens link | Primary path likely preserves | Low | Keep share regression |
| 22 | Baseline, URL with encoded Chinese | Preserve filter | Open encoded query | Behavior not runtime-verified | Medium | Encoded-value test |
| 23 | Baseline, multiple query parameters | Preserve all state | Open `?a=1&b=2` | Source copies raw search | Low | Exact-string test |
| 24 | Baseline, empty query marker | Avoid malformed destination | Open URL ending `?` | Browser normalization unknown | Low | Boundary test |
| 25 | Baseline, malformed percent encoding | Fail safely | Open malformed query | Runtime behavior unknown | Medium | Malformed-input matrix |
| 26 | Baseline, old search-engine result | Reach current product | Open bare result | Likely success | Low | Maintain canonical/noindex |
| 27 | Baseline, support agent | Reproduce reported lost state | Disable JS and open deep link | Static evidence predicts loss | High | Use #3 scenario verbatim |
| 28 | Baseline, maintainer | Change destination safely | Update target and tests | Contract duplicated in files | Medium | One declared target/contract |
| 29 | Baseline, QA engineer | Prove redirect once | Inspect/execute representative URL | Existing tests inspect source only | Medium | Behavioral fixture/test |
| 30 | Baseline, SRE | Distinguish deploy from correctness | Review successful Actions | Green run masks uncovered mode | Medium | Acceptance-specific check |
| 31 | Rotating, elderly learner, low vision | Read migration text before moving | Zoom to 200% | Timed redirect may remove context; unknown | Medium | Manual zoom/runtime check |
| 32 | Rotating, motor-impaired switch user | Use focusable link | Reach and activate control | Link is semantic, but state mutable | Medium | Correct href without timing race |
| 33 | Rotating, cognitive accessibility need | Understand one clear action | Read page slowly | Two-second move may be disorienting | Medium | Avoid forced timed redirect in fallback |
| 34 | Rotating, text-only browser | Follow legacy link | Render without script/style | Bare target loses state | High | Textual state-safe continuation |
| 35 | Rotating, corporate content filter | Reach exam during break | External script absent; inline may be blocked | Mode is unknown | Medium | CSP-restricted smoke |
| 36 | Rotating, data saver mode | Minimize transfer | Open old bookmark | Tiny page is strong | Low | Do not add assets |
| 37 | Rotating, unstable 3G | Retry after target timeout | Return/back/reopen | `replace` affects history by design | Low | Document one-way migration |
| 38 | Rotating, no-JS privacy extension | Preserve exact anchor | Open old deep link | Deterministic simulated failure | High | Fix before claiming universal preservation |
| 39 | Rotating, examiner verifying source | Find official provenance | Follow redirect then source | Shell adds no provenance | Low | Keep provenance in canonical repo |
| 40 | Rotating, teacher sharing a filtered set | Send old subject URL to class | Students use mixed devices | Blocked-script subgroup may diverge | High | Cross-mode equivalence test |
| 41 | Rotating, candidate preferring official PDFs | Obtain authoritative original | Compare redirect with MOEX | Chooses MOEX for authority | None | Do not replicate official archive |
| 42 | Rotating, Yamol community user | Discuss answers | Compare destinations | Chooses Yamol community | None | Do not add social features |
| 43 | Rotating, Quizlet subscriber | Use polished study modes | Compare shell with Quizlet | Chooses Quizlet | None | Keep scope narrow |
| 44 | Rotating, Anki power user | Schedule long-term recall | Export/manual workflow | Chooses Anki | None | Avoid SRS duplication here |
| 45 | Rotating, canonical-product user | Practice current corpus | Use direct canonical bookmark | Bypasses shell successfully | None | Promote canonical URL |
| 46 | Rotating, maintainer after one year | Decide whether to archive | Review traffic and link obligations | Traffic evidence unavailable | Medium | Explicit retirement criteria |
| 47 | Rotating, search crawler | Index only canonical product | Crawl compatibility page | Canonical/noindex confirmed | Low | Preserve metadata |
| 48 | Rotating, security reviewer | Check tracking and secrets | Inspect page dependencies | No external dependencies confirmed | Low | Keep zero-secret surface |
| 49 | Rotating, localization user | Understand Traditional Chinese copy | Read transition | Current message is localized | Low | Keep concise language |
| 50 | Rotating, future contributor | Avoid feature creep | Read README/issues | Scope is clear but contract inconsistent | Medium | Add “compatibility only” invariant |

### Synthetic switching test

| Choice | Personas | Synthetic preference share | Why the simulated personas choose it |
|---|---:|---:|---|
| `police-exam-archive` | 22 | 44% | Current first-party corpus and practice flow |
| This compatibility shell | 10 | 20% | Existing bookmarks, zero onboarding, fast transfer |
| Yamol | 8 | 16% | Community and broad exam-prep distribution |
| Quizlet | 4 | 8% | Polished general study modes and cross-device use |
| Anki | 4 | 8% | Durable customizable spaced repetition |
| MOEX | 2 | 4% | Official provenance and original papers |

These are scenario allocations from synthetic personas, not real market share, traffic, satisfaction, or survey results.

## Red Team

- **Persona bias:** the sample intentionally overrepresents legacy-link users because that is the repository’s only job. It cannot estimate total exam-prep demand.
- **Competitor-selection risk:** Yamol, Quizlet, and Anki compete with the canonical product, not with a redirect shell. They are included to prevent accidental product expansion, not to justify feature matching.
- **Evidence limit:** source inspection proves divergent paths; it does not prove how many real users disable JavaScript or lose state.
- **CI interpretation:** green source-contract tests and deployment do not cover the failing mode; they are not contradictory evidence.
- **Overengineering check:** a backend or server-side redirect would add operational risk. The preferred repair is a small static-contract change.
- **Feature-bloat check:** every proposed study feature belongs in the canonical repository or should be rejected.
- **Confirmation-bias check:** the normal JavaScript journey appears correct. The issue is specifically the unconditional promise and fallback, not the whole redirect.
- **Growth check:** adding tracking for a sunset decision may create more cost and privacy risk than the shell warrants.
- **Delete/simplify alternative:** removing the parameter-dropping timed fallback and presenting one honest continuation path is preferable to adding modes.
- **Archive challenge:** immediate archival could break old links; retirement requires evidence or an explicit owner decision.

## Findings and Quality Gate

Stable fingerprint: `Reese-max/police-exam-practice + compatibility redirect + JavaScript unavailable/interrupted + query/hash silently lost + preservation implemented only by inline JavaScript while static fallback is parameterless`.

| ID | Type | Priority | Evidence | Distinctness | Actionability / acceptance | Impact | Confidence | Effort | Mapping |
|---|---|---|---|---|---|---|---|---|---|
| F1 | RELIABILITY / DOCUMENTATION | P3 | HTML, README, manifest, tests, unchanged SHA | Same fingerprint as open #3; no duplicate | Existing #3 has explicit no-destructive-fallback, `noscript`, representative URL, and regression criteria | Affected fallback users lose navigation state | High static; runtime pending | Small | UPDATED EXISTING [#3](https://github.com/Reese-max/police-exam-practice/issues/3) |

Quality Gate: **PASS** for F1. Evidence, root-cause distinctness, actionability, impact, acceptance criteria, duplicate check, and confidence are present. Mapping completeness: **1/1**.

## Issue Mapping and Regression

### Updated existing issue

- [#3 — `[P3][RELIABILITY][DOCUMENTATION] Make query/hash preservation truthful for the no-JavaScript fallback`](https://github.com/Reese-max/police-exam-practice/issues/3)
- Status: **STILL REPRODUCIBLE / NEEDS_RUNTIME_VERIFICATION**
- New evidence added this round: unchanged product SHA, exact fallback/contract divergence, limitations of the nine current tests, latest successful CI/deploy receipts, and refreshed competitive boundaries.
- The issue remains open. It was not duplicated or reprioritized.

### Runtime pending

After a repair, verify:

1. JavaScript-disabled navigation does not silently drop query or hash.
2. Keyboard-only activation reaches the promised destination.
3. Screen-reader users receive understandable transition/continuation messaging.
4. Bare, query-only, hash-only, combined, encoded, empty, and malformed inputs follow an explicit safe contract.
5. The canonical product receives representative legacy state exactly once.

Until those scenarios pass with inspectable evidence, do not label #3 VERIFIED FIXED.

## Roadmap

### NOW — FIX / SIMPLIFY

- Complete #3 using the smallest static solution.
- Add a regression that detects a parameter-dropping no-JavaScript fallback.
- Make README, manifest, HTML, and tests express the same conditional or unconditional promise.

### NEXT — MAINTAIN

- Keep target ownership and product behavior in `police-exam-archive`.
- Preserve canonical/noindex metadata and the no-dependency posture.
- Define a minimal maintenance/retirement contract for legacy links.

### LATER

- Consider archival only after the owner determines legacy-link obligations are negligible or another durable redirect layer replaces this page.
- If that decision truly needs traffic evidence, research a privacy-minimal, time-bounded measurement plan first; do not silently add analytics.

### DON'T

- Do not rebuild question search, mock exams, learning state, AI tutoring, accounts, social features, payments, analytics, a backend, PWA, or native applications in this repository.

Priority order applied: **REMOVE > SIMPLIFY > FIX > IMPROVE > ADD**.

## Rejected Findings

1. Rebuild the quiz here — rejected as duplicate product logic and contrary to the completed consolidation.
2. Add accounts or cross-device sync — rejected for scope, privacy, and maintenance cost.
3. Add an AI tutor — rejected as feature bloat without evidence; belongs nowhere in a redirect shell.
4. Add spaced repetition — rejected here; existing substitutes and the canonical product own learning workflows.
5. Add legacy-user analytics — rejected absent a concrete archive decision that requires it.
6. Build a native app or PWA — rejected because distribution is a one-hop web compatibility problem.
7. Add a backend/server redirect service — rejected as unnecessary operational surface for a static repair.
8. Declare the normal JavaScript redirect broken — rejected because static code and existing tests support the primary path.
9. Declare a confirmed accessibility failure — rejected because no assistive-technology runtime was performed; keep it as post-fix verification.
10. Archive immediately — rejected because current legacy traffic and external-link obligations are UNKNOWN.
11. Create a new issue for each affected persona — rejected because all symptoms share #3’s root cause.
12. Copy competitor community, monetization, or study features — rejected because comparison is a boundary check, not a feature shopping list.

## Difference from Previous Audit

- Product source: no change.
- Default branch: still `07144e944ba12fcae81054321ab94a030e9ae183`, whose changes were prior audit documentation.
- Issue #3: still open and statically reproducible; updated with fresh evidence.
- CI/deployment: latest relevant runs remain successful for the current SHA, but the missing fallback scenario remains outside their coverage.
- Competitive pages: refreshed on 2026-09-11.
- Regression outcome: unchanged; no VERIFIED FIXED result.

## Decision Memo

- **What this product should become:** a nearly frozen, standards-based compatibility bridge to the canonical exam product.
- **Who it should serve:** users and external links that still arrive through historical `police-exam-practice` URLs.
- **Why users would choose it:** usually they do not choose it; an old bookmark, QR code, search result, or shared URL chooses it for them.
- **Why users choose competitors:** the canonical archive provides the current first-party practice flow; MOEX provides authority; Yamol provides community; Quizlet provides polished study modes; Anki provides customizable recall.
- **Biggest competitive gaps:** lossless fallback behavior and truthful contract—not feature breadth.
- **Potential moat:** durable historical-link continuity backed by one canonical, maintained dataset.
- **Top strategic / engineering / UX priorities:** finish #3; prevent duplicated product logic; make fallback messaging explicit and accessible.
- **What NOT to build:** accounts, AI tutor, social/community, payments, analytics, native app, backend, or duplicated exam content.
- **Features worth removing:** the parameter-dropping timed fallback; any future non-redirect behavior.
- **Biggest risks:** silent loss of deep-link context, false confidence from green CI, and feature creep that reverses consolidation.
- **Next experiments:** post-fix no-JS/browser/webview matrix and keyboard/screen-reader checks; only then consider retirement evidence.
- **Portfolio decision:** **MAINTAIN / SIMPLIFY**. The logical merge into `police-exam-archive` is already complete; this repository remains only as the compatibility surface.

## Portfolio CEO Review

### Portfolio relationship

- `police-exam-practice`, `exam-archive`, and `police-exam-archive` overlap in Taiwan exam access. New data, quiz UX, study state, and accessibility work should converge on `police-exam-archive`; compatibility repositories should not regrow product features.
- Shared component opportunity: a single versioned dataset/quality contract and a small reusable legacy-link redirect test, not a new framework.
- Auth, AI gateway, and server data layers are deliberately unnecessary for this shell.
- `claude-mem` was identified as an upstream fork/mirror with Issues disabled, not an independent Reese-max product to receive upstream defect Issues in this round.
- Other candidate repositories with active PRs, issue branches, or goals were not touched under the mutex rule.

### Incremental portfolio ranking

1. `police-exam-archive` — INVEST; canonical first-party exam product and data owner.
2. `cyber-prep-coach` — INVEST with public-release calibration gate.
3. `92-duty-scheduler` — INVEST after reliability/authorization gates.
4. `academic-mcp` — INVEST / SIMPLIFY after recovery and isolation evidence.
5. `autodev-ng` — INVEST / SIMPLIFY after configuration and repair-loop reliability.
6. `police-exam-practice` — MAINTAIN / SIMPLIFY as compatibility infrastructure, not a standalone growth product.
7. `exam-archive` — SIMPLIFY / MAINTAIN and converge shared data/UX with the canonical archive.
8. Empty placeholders and upstream mirrors — DEFINE, MERGE, or ARCHIVE rather than inventing products.

This is an incremental portfolio view using prior audit baselines; repositories other than `police-exam-practice` were not re-audited end-to-end in this report.

## Mandatory Verification

- **Total Findings:** 1
- **New Issues Created:** 0
- **Updated Existing Issues:** 1 — [Reese-max/police-exam-practice #3](https://github.com/Reese-max/police-exam-practice/issues/3), `[P3][RELIABILITY][DOCUMENTATION] Make query/hash preservation truthful for the no-JavaScript fallback`
- **Reopened Issues:** 0
- **Research Issues:** 0
- **Duplicate Avoided:** 8 symptom groups — query-only loss, hash-only loss, combined state loss, keyboard-early activation, blocked inline script, text-only browser, mixed classroom devices, and support reproducibility all map to #3.
- **Issue Write Blocked:** 0
- **SKIPPED_LOCKED:** candidate repositories with active PRs/issue branches were not written, including `ppt-studio`, `flux-image-gen`, `soundbox-offline`, `minideck`, `prompt-autoresearch`, `note-filler`, `lplrs-judicial-sync`, `adng-memory`, `taichung-police-intel`, `video-timeline-pipeline`, `ai-novel-workstation`, `clinical-scribe-worker`, `MaterialYouNewTab`, `tick-stock-panel`, `ninax-line-hermes`, `cf-mcp-server`, `herdr-skills`, `skill-foundry`, `project-doctor-web`, `lobsterpulse`, and `ai-flight-radar`.
- **Rejected Findings:** 12, with reasons listed above.
- **Verified Fixed:** 0
- **Priority distribution:** P0 0 / P1 0 / P2 0 / P3 1 / STRATEGIC 0
- **Highest Priority Finding:** #3
- **Mapping validation:** 1/1 Quality-Gate findings mapped to UPDATED EXISTING — **PASS**
- **Runtime Pending:** JavaScript-disabled navigation, representative webviews, encoded/malformed input matrix, keyboard, and screen-reader verification.
