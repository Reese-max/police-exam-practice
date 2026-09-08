# Product Board Audit — police-exam-practice

**Audit date:** 2026-09-09 (Asia/Taipei)  
**Scope:** deep incremental audit of `Reese-max/police-exam-practice` at `eded2d976e44f52030a8395bccd5c253ed321ad5`.  
**Method:** repository/CI evidence, public-runtime observation, current public competitor evidence, 13-role virtual board, 50 synthetic personas, switching simulation, red team, fingerprint duplicate check, and GitHub Issue closure.  
**Important:** persona results are synthetic simulations, not human interviews, market research, or market share.

## Executive Summary

**Decision: MAINTAIN / SIMPLIFY.** This repository is no longer an independent exam-prep product. It is a deliberately tiny legacy-URL compatibility surface whose only valuable job is to route old visitors into `police-exam-archive` without reviving a second question bank.

The standard path is healthy and is now runtime-verified: a legacy URL with `?subject=police-law#question-12` reached the canonical quiz with the exact query and fragment intact. Fusion check [run 33990786606](https://github.com/Reese-max/police-exam-practice/actions/runs/33990786606) and Pages deployment [run 33990785832](https://github.com/Reese-max/police-exam-practice/actions/runs/33990785832) both completed successfully for the current head.

One distinct P3 finding passed the Quality Gate: when JavaScript is unavailable, the HTML meta refresh and original static button silently drop query/hash, while README and the manifest claim preservation without qualification. This maps to [Issue #3](https://github.com/Reese-max/police-exam-practice/issues/3). The smallest correct change is transparent no-JavaScript degradation, not new infrastructure.

CEO resource constraint — do only three things:

1. Close #3 with an honest no-JavaScript recovery contract and regression test.
2. Keep all question data and feature work exclusively in `police-exam-archive`.
3. After deployment, verify the JS and no-JS paths and require two consecutive clean compatibility rounds.

Do **not** rebuild quizzes, accounts, AI tutoring, analytics, mobile apps, or a second data pipeline here.

## Project Discovery

| Area | Evidence | Assessment |
|---|---|---|
| Product type | **CONFIRMED — code/docs** | Legacy compatibility entry, not a standalone product |
| Maturity | **CONFIRMED — code/CI/runtime** | Stable maintenance shell; live deployment and CI succeed |
| Target user | **LIKELY — product inference** | Returning candidates, shared links, and bookmarks pointing at the retired practice site |
| Core task | **CONFIRMED — code/runtime** | Reach canonical quiz; preserve URL query/fragment when JavaScript runs |
| Core value | **CONFIRMED — architecture** | Avoid broken legacy links while preventing two-source question-bank drift |
| Main weakness | **CONFIRMED — static code** | No-JavaScript fallback silently loses state and contradicts unconditional documentation |
| Runtime | **CONFIRMED** | Standard JS redirect and canonical quiz observed on 2026-09-09; final URL preserved query/hash |
| Runtime pending | **UNKNOWN until tested** | JavaScript-disabled browser behavior after #3 is implemented |
| Security/privacy | **CONFIRMED — static** | No external scripts/styles, no account or telemetry surface, `noindex,follow` |
| Tests | **CONFIRMED — code/CI** | Nine unit assertions; no no-JavaScript acceptance |
| Issues/PRs | **CONFIRMED — GitHub** | No prior Issues; no open PR; #3 newly created |
| Source freshness | **CONFIRMED — runtime** | Canonical quiz displayed 115–106 years and 36,579 matching-choice questions; this is observed UI text, not independently audited data accuracy |

Repository inventory reviewed: `README.md`, `index.html`, `fusion-manifest.json`, `.github/workflows/fusion-check.yml`, `tests/test_fusion.py`, prior persona audit, recent commits, all Issues/PRs, branches, Actions, Pages output, and related `autodev-ng` status/search surfaces.

## Regression Closure

Previous audit state: **STATIC PASS / REDIRECT RUNTIME-PENDING — NOT CLEAN**.

| Prior gate | Current result | Classification |
|---|---|---|
| Legacy URL reaches canonical quiz | Observed | VERIFIED for standard JS path |
| Query/hash survive redirect | Exact final URL observed | VERIFIED for representative case |
| Redirect loop | One navigation ended at canonical quiz | VERIFIED for representative case |
| Fusion unit suite | Latest head workflow succeeded | VERIFIED |
| Pages deployment | Latest head deployment succeeded | VERIFIED |
| No-JavaScript fallback | Static evidence shows state loss | STILL REPRODUCIBLE / NEEDS_RUNTIME_VERIFICATION after fix |
| Two consecutive clean rounds | New P3 found | NOT CLEAN |

No existing Issue qualifies as VERIFIED FIXED because there was no prior Issue in this repository.

## Competitive Intelligence

Evidence refreshed on 2026-09-09:

- Canonical first-party replacement: [police-exam-archive quiz](https://reese-max.github.io/police-exam-archive/quiz.html).
- Direct commercial competitor: [阿摩警察法規試卷列表](https://yamol.tw/cat-%E8%AD%A6%E5%AF%9F%E2%97%86%E8%AD%A6%E5%AF%9F%E6%B3%95%E8%A6%8F-131.htm), showing 65 papers including 115-year content at crawl time; [Android listing](https://play.google.com/store/apps/details?hl=zh_TW&id=com.yamol.exam) showed 100K+ downloads, ads/IAP, and an update dated 2026-08-06.
- Indirect study platform: [Quizlet Android listing](https://play.google.com/store/apps/details?hl=en_US&id=com.quizlet.quizletandroid), advertising flashcards and interactive practice tests; updated 2026-08-31.
- Indirect offline/spaced-repetition alternative: [AnkiDroid listing](https://play.google.com/store/apps/details?hl=en_US&id=com.ichi2.anki), describing synchronized spaced repetition and offline/mobile use; updated 2026-05-03.
- Authoritative-source alternative: 考選部考畢試題查詢平臺, identified by the canonical product itself as its data source. Exact source-file accuracy was not independently re-audited in this round.

### Capability Matrix

| Product / alternative | Target user & value | Core / killer feature | Onboarding & UX | AI / automation | Integrations / API | Mobile / performance | Reliability / security / privacy | Pricing / source / community / docs / distribution |
|---|---|---|---|---|---|---|---|---|
| police-exam-practice | Old-link visitor; continuity | Tiny compatibility redirect | Automatic; readable fallback page | Deterministic JS only | Hard link to canonical site | Responsive, ~4 KB shell | No external runtime deps; P3 no-JS truth gap | Free/public; minimal docs; distributed via historical URLs |
| police-exam-archive | Taiwan police-exam candidate; unified official-source corpus | Search, quiz, analytics, 36,579 displayed matching questions | Dense but task-complete | Static data pipeline; no confirmed AI | GitHub/data pipeline | Responsive web; larger payload | Single source reduces drift; public code | Free/public; repository/Page distribution |
| 阿摩 | Broad Taiwan exam candidate | Large exam bank, explanations, discussion/course ecosystem | Familiar commercial search/categories | Automation not confirmed in this round | No API confirmed | Web + Android; 100K+ listing | Account/ads/IAP trade-offs; privacy not audited | Commercial closed source; strong community/discovery |
| Quizlet | Global learner/teacher | User-generated sets, flashcards, practice tests | Strong general onboarding | Personalized tools marketed; exact AI tier not audited | App ecosystem; API not assessed | Mature mobile apps | Cloud/account dependency | Freemium closed source; very broad distribution/docs |
| Anki/AnkiDroid | Power learner wanting control/offline | Spaced repetition, offline decks | Steeper setup; flexible | Scheduling automation, not generative AI | Deck/add-on ecosystem | Strong offline/mobile | Local-first options; sync trade-offs | Open-source clients/ecosystem; strong community docs |
| 考選部 source | Candidate or auditor needing authority | Official exam materials | Download/search, not a study journey | None confirmed | Data ingestion is downstream responsibility | Web/document-oriented | Highest provenance; weaker practice UX | Public authority; not a commercial product |

### Gap Classification

- **MUST MATCH:** honest redirect behavior; canonical target availability; no broken legacy URLs; accessible recovery.
- **SHOULD BE BETTER:** this shell should be smaller, faster, and more privacy-minimal than commercial study products.
- **DIFFERENTIATOR:** trustworthy migration to a public, inspectable, official-source corpus without account or duplicated question bank.
- **DO NOT COPY:** social feed, ads, courses, AI tutor, account system, spaced-repetition engine, mobile app, marketplace, or analytics inside the legacy shell.
- Competitor features belong in a separate canonical-product strategy discussion only after user evidence; they are not justification for expanding this repository.

## Virtual Executive Board

| Role | Question | Opportunity | Priority |
|---|---|---|---|
| CEO | Does this repo deserve independent investment? | Preserve link equity at near-zero complexity | #3, then maintenance only |
| CPO | What promise does the shell make? | One truthful promise: reach canonical content | Qualify no-JS behavior |
| CTO | Can compatibility stay static? | Yes; no server or data duplication needed | Remove destructive meta fallback |
| Staff/Principal Engineer | What invariant prevents divergence? | CI enforces tiny shell, canonical URLs, no embedded bank | Add no-JS invariant |
| UX Lead | What happens when automation fails? | Explicit recovery beats silent state loss | `noscript` notice and link |
| UX Researcher | Is affected population known? | It is not; treat impact as synthetic/edge | P3, not P1/P2 |
| Growth Lead | Should old traffic be measured? | Measurement could answer archive timing | Minority: avoid analytics unless a privacy case exists |
| CFO/Business Analyst | What is the lowest-cost path? | Static Pages + current CI | No new service |
| Security/Privacy Lead | Does fixing this require weaker CSP? | No; make fallback truthful | No third-party JS/telemetry |
| QA Lead | What is missing from test coverage? | No-JS and deployed deep-link matrix | Acceptance test for #3 |
| SRE Lead | Is production observable enough? | Actions + Pages deployment receipts are sufficient for shell | Periodic representative smoke only |
| Accessibility Specialist | Can a script-disabled user recover? | Not clearly today | Visible keyboard-readable recovery |
| Customer Support Lead | Can support explain migration? | README is clear; fallback copy can be clearer | Keep a single canonical support answer |

Cross-review consensus: **MAINTAIN/SIMPLIFY**. Minority opinion favored leaving meta refresh untouched because incidence is likely low. The board rejected that opinion because compatibility is the sole product job and the current unconditional claim is objectively false for the fallback.

## 50 Synthetic Personas

30 regression-baseline personas (R01–R30, 60%) and 20 rotating exploratory personas (E31–E50, 40%). Every row is a modelled journey, not a human participant.

| # | Background | Goal | Expectation | Task | Journey | Friction | Result | Comment | Severity | Suggestion / switch |
|---:|---|---|---|---|---|---|---|---|---|---|
| 01 | R01 | 19・警專考生・中熟練・Android/5G・首次 | 從舊收藏回到模擬考 | 自動保留篩選 | 開啟含 subject/hash 的舊連結 | 舊網址→redirect→新版 quiz | 無 | 成功 | 連結可直接續用 | None | 維持 redirect regression；Switch=legacy |
| 02 | R02 | 27・重考生・高熟練・iPhone/Wi‑Fi・熟練 | 續做警察法規 | 不重新找入口 | 開啟主畫面舊書籤 | 舊網址→新版 quiz | 短暫跳轉 | 成功 | 1.2 秒可接受 | P3 | 保留清楚狀態文案；legacy |
| 03 | R03 | 34・在職員警・中熟練・Windows/企業網路・熟練 | 利用休息時間刷題 | 舊連結不中斷 | 開啟 query 深連結 | redirect→quiz | 無 | 成功 | 查詢字串保留 | None | 持續自動測試；legacy |
| 04 | R04 | 22・法律系學生・高熟練・macOS/Wi‑Fi・首次 | 確認題庫範圍 | 可返回首頁/搜尋 | 先到舊入口再點 nav | redirect→quiz→首頁 | 看不到舊頁 nav（快速跳轉） | 成功 | 直接到測驗合理 | P3 | README 提供替代入口；archive |
| 05 | R05 | 41・輪班考生・低熟練・Android/4G・首次 | 快速開始十題 | 一鍵開始 | 舊網址→quiz→設定 | 進入新版並選題 | 設定很多 | 成功 | 相容殼不是根因 | P2 | 歸 canonical backlog，不在本 repo；archive |
| 06 | R06 | 30・補習班助教・高熟練・Desktop/LAN・熟練 | 分享指定篩選 | 網址狀態保留 | 貼上 query/hash | legacy→canonical | 無 | 成功 | 分享可用 | None | 保留精確 URL；legacy |
| 07 | R07 | 25・一般警察考生・中熟練・Android/5G・熟練 | 查看 115 年題 | 到最新版 | 舊入口 | redirect→115 年列表 | 無 | 成功 | 不再停在 114 年 | None | canonical 單一資料源；archive |
| 08 | R08 | 38・考生家長・低熟練・iPad/Wi‑Fi・首次 | 協助找到正式入口 | 標示清楚 | 開舊首頁 | 自動到模擬考 | 未讀到融合說明 | 成功 | 結果比說明重要 | P3 | 保留 README 對維護者說明；legacy |
| 09 | R09 | 29・刑警考生・高熟練・Linux/Wi‑Fi・熟練 | 批量驗證舊 URL | 無 loop | 多次開啟 | 每次單次 replace | 無 | 成功 | 沒有 history 污染 | None | 保留 location.replace；legacy |
| 10 | R10 | 24・低頻回訪者・中熟練・Android/4G・首次 | 找回半年前收藏 | 不要 404 | 開收藏 | 舊頁→新版 | 網域路徑改變 | 成功 | 仍能抵達 | None | 維持 Pages；legacy |
| 11 | R11 | 31・行政警察考生・中熟練・Windows/Wi‑Fi・熟練 | 長期刷題 | 需要統計/搜尋 | 直接開 canonical | 首頁→quiz/analytics | 類科清單長 | 成功 | 偏好正式站 | P2 | 問題屬 archive；archive |
| 12 | R12 | 20・大學生・高熟練・iPhone/5G・首次 | 快速體驗 | 現代行動 UX | 搜尋→canonical | quiz 設定→開始 | 選項密集 | 成功 | 仍勝過舊殼 | P2 | canonical UX 研究；archive |
| 13 | R13 | 45・轉職考生・低熟練・Windows/ADSL・首次 | 準備法規 | 頁面快且免費 | canonical quiz | 載入設定 | 題庫分類多 | 成功 | 免費是關鍵 | P2 | 維持靜態低成本；archive |
| 14 | R14 | 28・英文弱項考生・中熟練・Android/4G・熟練 | 練專業英文 | 精準科目 | canonical 搜尋→quiz | 選類科/科目 | 名稱近似 | 成功 | 仍選自有平台 | P2 | canonical normalization；archive |
| 15 | R15 | 36・補教老師・高熟練・Desktop/LAN・Power | 檢查歷年覆蓋 | 可稽核來源 | canonical analytics | 統計→題目 | 缺真人驗證 | 成功 | 開源可查 | P2 | 維持來源證據；archive |
| 16 | R16 | 23・首次國考生・中熟練・Chromebook/Wi‑Fi・首次 | 探索考科 | 需要引導 | canonical 首頁 | 搜尋→試卷 | 資訊量大 | 成功 | 偏好專門題庫 | P2 | 不在 legacy 加 onboarding；archive |
| 17 | R17 | 32・消防警察考生・高熟練・Android/5G・熟練 | 特定類科組卷 | 保留條件 | 直接 canonical | 設定→組卷 | 類科名稱重複 | 成功 | 功能存在 | P2 | canonical issue candidate，未在本 repo 建；archive |
| 18 | R18 | 26・國境警察考生・中熟練・iPhone/4G・熟練 | 通勤刷題 | 行動穩定 | canonical quiz | 設定→作答 | 無離線證據 | 成功 | 線上可用 | P3 | 不要在殼做 PWA；archive |
| 19 | R19 | 39・法律工作者・高熟練・macOS/Wi‑Fi・Power | 核對原題 | 官方來源可追 | canonical→來源說明 | 查看題目 | 來源連結可見性未知 | 成功 | 接受開源資料 | P2 | 屬 canonical 文件；archive |
| 20 | R20 | 21・警專學生・高熟練・Android/校園網路・熟練 | 模考計時 | 像正式測驗 | canonical quiz | 選 50 題/時間 | 未實跑完整交卷 | 部分 | 需後續 runtime | P2 | canonical runtime suite；archive |
| 21 | R21 | 44・重考生・低熟練・Windows/Wi‑Fi・熟練 | 看解析 | 逐題回饋 | Yamol 試卷 | 搜尋→作答→討論 | 廣告/登入摩擦 | 成功 | 內容社群較強 | P2 | Switch=Yamol |
| 22 | R22 | 33・補習班學員・中熟練・Android/5G・熟練 | 找 115 最新題 | 更新快 | Yamol 類別 | 類別→115 試卷 | 分類也複雜 | 成功 | 熟悉阿摩 | P2 | Yamol |
| 23 | R23 | 29・社群型考生・高熟練・iPhone/5G・Power | 看其他人解法 | 討論與詳解 | Yamol | 試卷→討論 | 品質不一 | 成功 | 社群是主因 | P2 | Yamol |
| 24 | R24 | 48・公職講師・中熟練・Desktop/LAN・Power | 整理課程 | 大量試卷 | Yamol | 科目→歷年 | 商業內容混合 | 成功 | 覆蓋廣 | P2 | Yamol |
| 25 | R25 | 18・學習卡使用者・高熟練・Android/5G・首次 | 把錯題變卡片 | 自訂複習 | Quizlet | 匯入→卡片→測驗 | 需整理內容 | 成功 | 個人化優先 | P2 | Quizlet |
| 26 | R26 | 35・跨考試考生・高熟練・iPhone/Wi‑Fi・熟練 | 多科共用工具 | 一套學習工具 | Quizlet | 建立集→practice | 非台灣警考專用 | 成功 | 通用性勝出 | P2 | Quizlet |
| 27 | R27 | 42・記憶導向考生・高熟練・Desktop/離線・Power | 長期記憶法條 | 排程複習 | Anki | 建卡→FSRS 複習 | 內容建置成本 | 成功 | 離線和控制權重要 | P2 | Anki |
| 28 | R28 | 24・開源愛好者・高熟練・Linux/不穩網路・Power | 離線刷自製卡 | 可攜/同步 | AnkiDroid | 同步→離線學習 | 非現成題庫 | 成功 | 自主性優先 | P2 | Anki |
| 29 | R29 | 50・審題人員・中熟練・Desktop/政府網路・專業 | 取得原始試題 | 官方權威 | 考選部 | 查年度→下載 | 缺互動練習 | 成功 | 來源最可信 | P2 | MOEX |
| 30 | R30 | 37・資料工程師・高熟練・Linux/LAN・Power | 核對 ingest | 官方檔案可下載 | 考選部 | 下載→比對 archive | 手工流程 | 成功 | 不用 legacy 殼 | P2 | MOEX |
| 31 | E31 | 28・隱私強化使用者・高熟練・Firefox/5G・腳本封鎖 | 續用深連結 | 無 JS 也不靜默丟狀態 | 關 JS 開 query/hash | meta refresh→bare quiz | query/hash 丟失 | 失敗 | 承諾不完整 | P3 | #3 移除破壞性 meta refresh；legacy |
| 32 | E32 | 46・企業受管制瀏覽器・中熟練・Windows/LAN・inline script 禁止 | 開單位書籤 | 得到可理解降級 | 開舊深連結 | 靜態 fallback | 無提示即換頁 | 失敗 | 需要 noscript 說明 | P3 | #3；legacy |
| 33 | E33 | 54・螢幕閱讀器使用者・中熟練・Desktop/Wi‑Fi・JS 關閉 | 保留題目位置 | 狀態與連結可讀 | 舊 URL | meta refresh | 無機會理解狀態 | 失敗 | 應停留並說明 | P3 | #3 accessible noscript；legacy |
| 34 | E34 | 31・低記憶體手機・中熟練・Android/3G・部分載入 | 恢復指定題 | 失敗時可救援 | 載入中 script 未執行 | HTML fallback | 狀態丟失 | 失敗 | 靜默降級不好 | P3 | #3 no silent loss；legacy |
| 35 | E35 | 40・Privacy Browser 使用者・高熟練・iOS/4G・腳本限制 | 打開收藏 | 至少知道需重選 | 舊深連結 | meta refresh | 條件消失 | 失敗 | 可接受透明重選 | P3 | #3 truthful copy；legacy |
| 36 | E36 | 23・鍵盤使用者・中熟練・Windows/Wi‑Fi・Accessibility | 使用 fallback link | 清楚 focus target | 正常載入 | 自動 redirect 前嘗試 Tab | 時間很短 | 成功 | 按鈕至少 48px | P3 | 修後驗證鍵盤；archive |
| 37 | E37 | 62・低視力考生・低熟練・iPad/Wi‑Fi・Accessibility | 閱讀入口說明 | 高對比/放大 | 舊首頁 | 1.2 秒後轉址 | 來不及閱讀 | 成功 | 結果頁可用但提示短 | P3 | 不延長一般流程；archive |
| 38 | E38 | 27・低頻寬通勤者・中熟練・Android/2G・Edge | 快速到題庫 | 小 payload | 舊殼→archive | 3.8KB shell→quiz | 後段題庫較大 | 成功 | 殼很輕 | None | 維持 <30KB；archive |
| 39 | E39 | 34・分享連結接收者・高熟練・iPhone/5G・Edge | 開含 Unicode 參數 URL | 不重編碼 | encoded query/hash | replace→canonical | 未驗證所有編碼 | 成功 | 代表案例通過 | P3 | 加入編碼矩陣；archive |
| 40 | E40 | 30・錯誤參數使用者・高熟練・Desktop/Wi‑Fi・Edge | 安全失敗 | 不 loop/不 crash | malformed query | redirect→canonical | 目的頁忽略未知值 | 成功 | fail soft | P3 | runtime 測 malformed；archive |
| 41 | E41 | 22・無痕模式考生・中熟練・Android/5G・Edge | 不依 cookie | 直接開始 | legacy deep link | redirect→quiz | 狀態只在 URL | 成功 | 隱私友善 | None | 不加 analytics；legacy |
| 42 | E42 | 38・內容安全政策維護者・高熟練・Desktop/LAN・專業 | 最小攻擊面 | 無第三方 runtime | 檢查頁面 | 本地 CSS/JS only | inline script 可能被 CSP 擋 | 部分 | 外部依賴為零 | P3 | #3 transparent CSP degradation；legacy |
| 43 | E43 | 55・舊 Android WebView・低熟練・3G・Edge | 開舊收藏 | 有標準 fallback | 載入 legacy | URL API 支援未知 | 需要裝置測試 | 未知 | 不可宣稱全支援 | P3 | Research runtime，未另開 issue；legacy |
| 44 | E44 | 26・雙語使用者・高熟練・macOS/Wi‑Fi・Edge | 理解入口 | 中文足夠 | 開舊頁 | 快速轉址 | 沒有英文說明 | 成功 | 目標市場中文 | None | 不做雙語殼；archive |
| 45 | E45 | 43・客服協助者・中熟練・Desktop/LAN・專業 | 解釋網址變更 | 有單一文件 | README | 查定位/入口 | 需要 GitHub 閱讀 | 成功 | 文件明確 | P3 | 維持 README；archive |
| 46 | E46 | 32・維護者・高熟練・Linux/LAN・Power | 防止題庫回流 | CI fail closed | 本地 unittest | 9 tests | 未含 no-JS | 部分 | 核心契約有測試 | P3 | #3 擴充 test；archive |
| 47 | E47 | 29・SRE・高熟練・Desktop/LAN・專業 | 確認 deploy | 成功 run 可追 | Actions | 查 Fusion/Pages runs | 無 synthetic monitor | 成功 | 兩個 run 綠 | None | 不加監控後端；archive |
| 48 | E48 | 35・SEO 維護者・高熟練・Desktop/LAN・專業 | 避免重複索引 | canonical/noindex | 檢查 head | noindex,follow + canonical | 無 | 成功 | 設定正確 | None | 保留 regression；archive |
| 49 | E49 | 47・產品負責人・高熟練・Desktop/LAN・專業 | 決定是否封存 | 保留舊流量 | 比較殼與正式站 | 舊 URL 仍可用 | 無流量數據 | 部分 | 先維持相容 | P3 | 不要自動 archive；archive |
| 50 | E50 | 25・離線旅行考生・中熟練・Android/無網路・Edge | 離線刷題 | 離線可用 | 開舊書籤 | 無網路 | 兩站都不可達 | 失敗 | 不屬 redirect 根因 | P3 | 改用 Anki；Switch=Anki |

Coverage summary:

- Ages 18–62; candidates, repeat candidates, officers, instructors, maintainers, auditors, parents/support roles.
- Low/medium/high digital fluency; first-time, returning, professional, and power users.
- Android, iOS, Windows, macOS, Linux, iPad, Chromebook, managed browsers.
- Offline, 2G/3G/4G/5G, Wi‑Fi, enterprise and campus networks.
- Keyboard, screen reader, low vision, script blocking, CSP, privacy browser, partial-load, malformed/encoded URL, SEO and operational edge cases.
- Standard JS compatibility success: 45/50 simulated journeys.
- No-JavaScript/partial-script state-loss group: 5/50 simulated journeys, all sharing the #3 root cause.
- This 90%/10% split is a scenario allocation, **not** an observed failure rate.

## Competitor Switching Test

Scenario: “Start or resume police-exam preparation from the user’s current context.”

| Choice | Personas | Synthetic preference share | Main reason |
|---|---:|---:|---|
| police-exam-archive direct | 22 | 44% | Canonical current corpus, quiz/search/analytics |
| police-exam-practice legacy shell | 10 | 20% | Existing bookmark/share link continuity |
| 阿摩 | 8 | 16% | Broad bank, explanations, community familiarity |
| Quizlet | 4 | 8% | Flexible personal study sets/practice |
| Anki | 4 | 8% | Offline control and spaced repetition |
| 考選部 raw source | 2 | 4% | Authoritative original material |

These are synthetic choices, not market share or survey results. The shell’s 20% is not evidence for growth investment; it validates its narrow role as a migration surface.

## Red Team

- Persona allocation may overrepresent technically unusual no-JS cases; severity remains P3.
- Competitor comparison can mislead because a redirect shell is not a full exam product; only the canonical archive should compete on learning outcomes.
- The observed query value was preserved in the URL but not proven to be interpreted by the canonical quiz; this audit claims transport preservation only.
- Displayed “36,579 questions” was observed, not independently reconciled to source files.
- A redirect backend would over-engineer a low-impact static edge case.
- Removing the repository would simplify the portfolio but would break the legacy URL contract; do not archive without evidence that compatibility value has expired.
- Adding analytics to decide archive timing creates privacy/governance cost disproportionate to this shell.
- Feature parity with Yamol/Quizlet/Anki is a confirmation-bias trap.
- The prior audit already mentioned meta-refresh state loss; this round turns that same root cause into one Issue rather than inventing multiple persona defects.
- Best action order remains **REMOVE destructive fallback → SIMPLIFY promise → FIX tests → VERIFY → do not add**.

## Findings and Quality Gate

| ID | Type | Priority | Impact | Strategic value | Gap / risk reduction | Confidence | Effort | Gate | Mapping |
|---|---|---:|---|---|---|---|---|---|---|
| F1 | RELIABILITY / DOCUMENTATION | P3 | Edge users silently lose deep-link state | High relative to shell’s single job | Removes false guarantee; explicit recovery | High root cause / medium population | Small | PASS: confirmed, distinct, actionable, measurable AC, duplicate checked | NEW [#3](https://github.com/Reese-max/police-exam-practice/issues/3) |

Stable fingerprint: `police-exam-practice + compatibility redirect + JavaScript unavailable + query/hash silently dropped + preservation implemented only in inline JS while static fallback is parameterless`.

Duplicate search: all open/closed Issues, merged/open PRs, historical audit, current code, roadmap/radar evidence, target branches, and related `autodev-ng` search. No Issue with the same fingerprint existed.

## Issue Mapping

- **NEW:** [police-exam-practice #3 — [P3][RELIABILITY][DOCUMENTATION] Make query/hash preservation truthful for the no-JavaScript fallback](https://github.com/Reese-max/police-exam-practice/issues/3)
- **UPDATED:** none
- **REOPENED:** none
- **RESEARCH:** none
- **DUPLICATE AVOIDED:** six symptom clusters (script blocker, enterprise CSP, assistive no-JS, partial load, privacy browser, prior meta-refresh audit note) consolidated into #3.
- **ISSUE_WRITE_BLOCKED:** none
- **SKIPPED_LOCKED:** none; lock ownership was created, re-read, and verified before report write.

## Roadmap

### NOW

- Close #3 with transparent no-JS degradation and test coverage.
- Preserve the current small payload, canonical/noindex behavior, and zero external dependency.

### NEXT

- Deploy the fix; runtime-test representative normal, encoded, malformed, and no-JS cases.
- Re-run the fixed persona baseline twice; only then mark compatibility CLEAN.

### LATER

- Revisit whether the shell is still needed only with a defensible migration/traffic signal that does not introduce disproportionate tracking.
- If the canonical URL changes, update manifest, README, page, and tests atomically.

### DON'T

- Do not copy question data or features back.
- Do not add accounts, AI tutor, social/community, subscriptions, analytics, PWA/offline cache, native mobile app, or redirect backend.
- Do not archive while legacy compatibility remains an explicit promise.
- Do not file canonical quiz taxonomy/UX issues in this repository.

## Rejected Findings

1. **Rebuild the quiz here** — violates fusion architecture and duplicates root data.
2. **Add accounts/progress sync** — feature bloat; belongs, if ever, in canonical product.
3. **Add AI explanations/tutor** — no user evidence; cost/privacy risk.
4. **Add spaced repetition** — competitor copying; not compatible-shell scope.
5. **Create a native app/PWA** — distribution overreach for a redirect.
6. **Add traffic analytics** — privacy/governance cost not justified.
7. **Archive immediately** — would break the only confirmed value.
8. **Escalate #3 to P1/P2** — no evidence of broad incidence or critical harm.
9. **Create a second Issue for each affected persona** — same root cause; consolidated.
10. **Create an Issue here for the canonical quiz’s long/duplicated filter labels** — wrong repository/root-cause owner and insufficient focused evidence in this audit.
11. **Claim all legacy parameters are semantically honored** — only URL transport was verified.
12. **Claim no-JS runtime failure as directly observed** — current result is code-confirmed/static; browser-disabled acceptance remains pending.

## Decision Memo

- **What this product should become:** a durable, minimal compatibility endpoint with an explicit degradation contract.
- **Who it should serve:** people and links still pointing to the legacy practice URL.
- **Why users would choose it:** they do not actively choose it; existing bookmarks continue to work.
- **Why users choose competitors:** richer banks, explanations/community, personalization, offline/spaced repetition, or official provenance.
- **Biggest competitive gaps:** none that should be closed here; only fallback truthfulness matters.
- **Potential moat:** trustworthy public migration into a single inspectable official-source corpus.
- **Top strategic/engineering/UX priorities:** #3; preserve fusion invariants; deployed regression verification.
- **What NOT to build:** any standalone learning feature or new infrastructure.
- **Features worth removing:** parameter-dropping meta refresh; any future duplicated bank.
- **Biggest risks:** silent state loss, canonical URL drift, accidental product divergence, premature archive.
- **Next experiments:** no-JS acceptance, encoded/malformed URL matrix, two clean rounds.
- **Portfolio decision:** **MAINTAIN / SIMPLIFY**.

## Portfolio CEO Review (Incremental)

This run did not re-audit every repository. Portfolio baseline plus this repo’s evidence supports:

1. **police-exam-archive — INVEST selectively:** canonical exam data/product surface.
2. **autodev-ng — INVEST selectively:** reusable agent orchestration/governance.
3. **taichung-police-intel — MAINTAIN:** operational intelligence pipeline after runtime evidence.
4. **UkePack — INVEST after release gate:** differentiated teacher workflow, privacy-minimal research.
5. **cf-ai-router — MAINTAIN / RESEARCH:** focused cost-safe AI gateway.
6. **police-exam-practice — MAINTAIN / SIMPLIFY:** compatibility only.
7. **gooaye — ARCHIVE candidate:** no distinct product identity yet.

Portfolio consolidation:

- Exam data, import, search, quiz, analytics, and future learning UX stay in `police-exam-archive`.
- `police-exam-practice` shares no auth, AI gateway, data layer, design system, or agent framework; forcing shared infrastructure would add coupling without value.
- The only shared contract needed is canonical URLs plus a small compatibility regression suite.
- Do not merge the shell’s repository history into the canonical runtime again; preserve it as a migration receipt and link endpoint.

## Mandatory End Validation

- **Total Findings:** 1
- **New Issues Created:** 1 — [Reese-max/police-exam-practice #3](https://github.com/Reese-max/police-exam-practice/issues/3), `[P3][RELIABILITY][DOCUMENTATION] Make query/hash preservation truthful for the no-JavaScript fallback`
- **Updated Existing Issues:** 0
- **Reopened Issues:** 0
- **Research Issues:** 0
- **Duplicate Avoided:** 6 symptom clusters → #3
- **Issue Write Blocked:** 0
- **Rejected Findings:** 12, with reasons above
- **Verified Fixed Issues:** 0
- **Verified prior runtime gates:** standard redirect, representative query/hash transport, one-hop navigation, latest Fusion CI, latest Pages deployment
- **Priority distribution:** P0 0 / P1 0 / P2 0 / P3 1 / STRATEGIC 0
- **Highest Priority:** #3 (P3)
- **Runtime Pending:** no-JavaScript acceptance after implementation; encoded/malformed matrix
- **Quality-Gate mapping:** 1/1 findings mapped (NEW #3)
- **Execution completeness:** COMPLETE for this repository’s deep incremental audit and GitHub write loop. Other repositories retain the existing portfolio baseline and were not claimed as re-audited in this round.
