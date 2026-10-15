# police-exam-practice

本 Repository 已融合至 [`Reese-max/police-exam-archive`](https://github.com/Reese-max/police-exam-archive)。

## 現在的分工

| Repository | 定位 |
|---|---|
| `police-exam-archive` | 唯一正式題庫、資料管線、搜尋、模擬考、統計與 GitHub Pages |
| `police-exam-practice` | 舊網址相容入口，導向正式模擬考 |

正式入口：

- 題庫首頁：https://reese-max.github.io/police-exam-archive/
- 模擬考：https://reese-max.github.io/police-exam-archive/quiz.html
- 全文搜尋：https://reese-max.github.io/police-exam-archive/search.html
- 出題統計：https://reese-max.github.io/police-exam-archive/analytics.html

## 為什麼融合

舊版把介面、程式邏輯與大量題庫資料放在單一 `index.html`，
容易造成兩個 Repository 的年度、答案與功能不同步。

融合後採單一來源：

```text
考選部官方資料
       ↓
police-exam-archive
  ├─ JSON 題庫
  ├─ 匯入與稽核
  ├─ 搜尋索引
  ├─ 模擬考
  └─ GitHub Pages
       ↑
police-exam-practice
  └─ 相容入口
```

## 維護原則

1. 題庫與功能修改只進 `police-exam-archive`。
2. 本 Repository 不再內嵌或複製題庫。
3. 舊版 2.56 MB 單頁網站仍可從 Git 歷史查閱或還原。
4. 啟用 JavaScript 且相容程式成功建立目標連結時，Query string 與 URL hash 會在自動重新導向與手動連結中保留；
   JavaScript 未啟用、遭封鎖或在建立連結前初始化失敗時，本頁不自動跳轉，
   預設可見的復原說明會提醒使用手動連結，進入新版後需重新選擇科目與題目。
   連結建立後，若計時器初始化失敗或自動導向未成功，復原說明會顯示，並指出手動連結已攜帶原網址狀態。
5. Pull Request 必須通過 `Fusion compatibility check`。

## 本地驗證

```bash
python -m unittest discover -s tests -v
```

已備有 Playwright 與 `/usr/bin/chromium` 的環境可另跑隔離瀏覽器驗收：

```bash
python tests/browser_recovery.py --report /tmp/browser-recovery.json
```

此驗收涵蓋正常與手動導向、停用 JavaScript、CSP 封鎖、早期拋錯、URL／計時器初始化失敗，
以及 `location.replace()` 拋錯或未導向。後兩者僅替換測試回應中的該呼叫，使用真實 DOM 與計時器。
所有請求均由測試攔截，正式題庫以靜態回應替代，不會存取正式網站、帳號或使用者資料。
