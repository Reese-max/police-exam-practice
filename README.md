# police-exam-practice

本 Repository 原為單一 `index.html` 的警察特考練習站，題庫、介面與作答邏輯全部內嵌於同一檔案。

自民國 115 年題庫開始，練習功能已整合至：

- 題庫與來源：`Reese-max/police-exam-archive`
- 線上練習：`https://reese-max.github.io/police-exam-archive/practice.html`
- 全文搜尋：`https://reese-max.github.io/police-exam-archive/search.html`

## 為何整合

原本兩個 Repository 各自保存題目，容易出現：

- 年度更新不同步
- 官方更正答案只套用其中一站
- 閱讀題文章與選項在轉換時分岔
- 修正一處後另一站仍維持舊錯誤
- 2.5 MB 單檔 HTML 難以測試及維護

現在 `police-exam-archive` 是唯一資料來源，搜尋與練習均使用同一份建置索引。

## 相容性

本 Repository 保留為舊網址入口：

- `index.html` 自動導向新版練習站
- URL query 與 hash 會一併轉移
- `404.html` 接住舊深層連結

不要再將新題目或作答功能直接寫入本 Repository；所有後續開發應在 `police-exam-archive` 進行。
