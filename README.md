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
4. Query string 與 URL hash 僅在 JavaScript 啟用時才會隨重新導向保留（`preserve_query_and_hash: "js-only"`）；停用 JavaScript 時，靜態連結仍可前往新版網站但不攜帶參數，頁面會以 `noscript` 說明此情況。
5. Pull Request 必須通過 `Fusion compatibility check`。

## 本地驗證

```bash
python -m unittest discover -s tests -v
```
