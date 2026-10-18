from __future__ import annotations

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
MANIFEST = ROOT / "fusion-manifest.json"
README = ROOT / "README.md"
CANONICAL_ORIGIN = "https://reese-max.github.io"
CANONICAL_PATH = "/police-exam-archive/quiz.html"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.canonicals: list[str] = []
        self.external_scripts: list[str] = []
        self.external_styles: list[str] = []
        self.text: list[str] = []
        self.links_by_id: dict[str, str] = {}
        self.ignored_tag: str | None = None
        self.meta_refreshes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if self.ignored_tag is None and tag in {"script", "style", "noscript"}:
            self.ignored_tag = tag
        if tag == "meta" and str(values.get("http-equiv") or "").strip().lower() == "refresh":
            self.meta_refreshes.append(str(values.get("content") or ""))
        if tag == "a" and values.get("href"):
            self.links.append(str(values["href"]))
            if self.ignored_tag is None and values.get("id"):
                self.links_by_id[str(values["id"])] = str(values["href"])
        if tag == "link":
            rel = str(values.get("rel") or "")
            href = str(values.get("href") or "")
            if "canonical" in rel:
                self.canonicals.append(href)
            if "stylesheet" in rel and href:
                self.external_styles.append(href)
        if tag == "script" and values.get("src"):
            self.external_scripts.append(str(values["src"]))

    def handle_endtag(self, tag: str) -> None:
        if tag == self.ignored_tag:
            self.ignored_tag = None

    def handle_data(self, data: str) -> None:
        if self.ignored_tag is None:
            self.text.append(data)


class FusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = INDEX.read_text(encoding="utf-8")
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.readme = README.read_text(encoding="utf-8")
        cls.parser = LinkParser()
        cls.parser.feed(cls.index)

    def test_entry_is_small_and_no_embedded_question_bank(self) -> None:
        self.assertLess(INDEX.stat().st_size, 30_000)
        self.assertNotRegex(self.index, r'"questions"\s*:\s*\[')
        self.assertFalse(self.manifest["embedded_question_bank"])

    def test_canonical_quiz_is_consistent(self) -> None:
        target = self.manifest["canonical_quiz"]
        parsed = urlparse(target)
        self.assertEqual(parsed.scheme + "://" + parsed.netloc, CANONICAL_ORIGIN)
        self.assertEqual(parsed.path, CANONICAL_PATH)
        self.assertEqual(self.parser.canonicals, [target])
        self.assertIn(target, self.index)

    def test_redirect_preserves_query_and_hash(self) -> None:
        # JS 執行時才保留參數；manifest 與 README 必須誠實標記 js-only
        self.assertEqual(self.manifest["preserve_query_and_hash"], "js-only")
        self.assertIn("target.search = window.location.search", self.index)
        self.assertIn("target.hash = window.location.hash", self.index)
        self.assertIn("window.location.replace(target.href)", self.index)
        self.assertIn("js-only", self.readme)

    def test_no_javascript_fallback_is_truthful(self) -> None:
        self.assert_fallback_contract(self.index)

    def assert_fallback_contract(self, index: str) -> None:
        parser = LinkParser()
        parser.feed(index)
        self.assertEqual(parser.meta_refreshes, [], "meta refresh 會丟掉 query/hash")
        # noscript 無法涵蓋腳本遭封鎖或初始化失敗，復原說明必須預設可讀。
        text = " ".join(parser.text)
        for phrase in ("JavaScript", "查詢參數", "網址片段", "重新選擇"):
            self.assertIn(phrase, text)
        self.assertEqual(parser.links_by_id.get("continue-link"), self.manifest["canonical_quiz"])

    def test_recovery_is_visible_when_inline_script_does_not_run(self) -> None:
        text = " ".join(self.parser.text)
        for phrase in ("JavaScript", "查詢參數", "網址片段", "重新選擇"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertNotIn("即將前往", text)

    def test_fallback_guard_rejects_meta_refresh_variants(self) -> None:
        target = self.manifest["canonical_quiz"]
        for meta in (
            f'<META HTTP-EQUIV="REFRESH" CONTENT="0;url={target}">',
            f'<meta content="0;url={target}" http-equiv="refresh">',
            f'<meta http-equiv = "Refresh" content="0;url={target}">',
        ):
            with self.subTest(meta=meta), self.assertRaises(AssertionError):
                self.assert_fallback_contract(self.index.replace("</head>", meta + "</head>"))

    def test_fallback_guard_rejects_missing_warning_or_wrong_link(self) -> None:
        warning = re.search(
            r'<noscript>.*?</noscript>|<p id="redirect-fallback"[^>]*>.*?</p>',
            self.index,
            re.DOTALL,
        )
        self.assertIsNotNone(warning)
        for name, broken in (
            ("commented warning", self.index.replace(warning[0], "<!--" + warning[0] + "-->")),
            (
                "missing manual href",
                re.sub(
                    r'(<a\b[^>]*id="continue-link")\s+href="[^"]+"',
                    r'\g<1>',
                    self.index,
                ),
            ),
            (
                "wrong manual destination",
                re.sub(
                    r'(<a\b[^>]*id="continue-link"\s+href=")[^"]+',
                    r'\g<1>https://github.com/Reese-max/police-exam-archive',
                    self.index,
                ),
            ),
        ):
            with self.subTest(mutation=name), self.assertRaises(AssertionError):
                self.assert_fallback_contract(broken)

    def test_page_is_accessible_fallback_not_blank_redirect(self) -> None:
        self.assertIn('role="status"', self.index)
        self.assertIn('id="continue-link"', self.index)
        self.assertIn("進入新版模擬考", self.index)
        self.assertIn("題庫首頁", self.index)
        self.assertIn("全文搜尋", self.index)
        self.assertIn("出題統計", self.index)

    def test_search_engines_do_not_index_duplicate_entry(self) -> None:
        self.assertRegex(self.index, r'<meta\s+name="robots"\s+content="noindex,follow">')

    def test_all_product_links_are_canonical_or_github(self) -> None:
        allowed_hosts = {"reese-max.github.io", "github.com"}
        for href in self.parser.links:
            parsed = urlparse(href)
            self.assertEqual(parsed.scheme, "https", href)
            self.assertIn(parsed.netloc, allowed_hosts, href)

    def test_no_external_runtime_dependencies(self) -> None:
        self.assertEqual(self.parser.external_scripts, [])
        self.assertEqual(self.parser.external_styles, [])

    def test_no_stale_year_range_or_old_product_claim(self) -> None:
        self.assertNotRegex(self.index + self.readme, r"110\s*[–-]\s*114")
        self.assertNotIn("唯一正式題庫：police-exam-practice", self.readme)

    def test_manifest_and_readme_point_to_same_repository(self) -> None:
        self.assertEqual(
            self.manifest["canonical_repository"],
            "Reese-max/police-exam-archive",
        )
        self.assertIn("Reese-max/police-exam-archive", self.readme)
        self.assertTrue(self.manifest["legacy_version_available_in_git_history"])


if __name__ == "__main__":
    unittest.main()
