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
        self.elements: dict[str, dict[str, str | None]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.elements[str(values["id"])] = values
        if tag == "a" and values.get("href"):
            self.links.append(str(values["href"]))
        if tag == "link":
            rel = str(values.get("rel") or "")
            href = str(values.get("href") or "")
            if "canonical" in rel:
                self.canonicals.append(href)
            if "stylesheet" in rel and href:
                self.external_styles.append(href)
        if tag == "script" and values.get("src"):
            self.external_scripts.append(str(values["src"]))


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
        preserve = self.manifest["preserve_query_and_hash"]
        self.assertIsInstance(preserve, dict)
        self.assertTrue(preserve["javascript_redirect"])
        self.assertTrue(preserve["javascript_manual_link"])
        self.assertFalse(preserve["no_javascript"])
        script = re.search(
            r"<script[^>]*>(.*?)</script>",
            self.index,
            re.IGNORECASE | re.DOTALL,
        )
        self.assertIsNotNone(script, "inline compatibility script is missing")
        code = script.group(1)
        self.assertIn("target.search = window.location.search", code)
        self.assertIn("target.hash = window.location.hash", code)
        self.assertIn("window.location.replace(target.href)", code)

    def test_no_meta_refresh_parameter_dropping_redirect(self) -> None:
        self.assertNotRegex(
            self.index,
            r'(?i)http-equiv\s*=\s*["\']?refresh',
        )

    def test_noscript_recovery_links_canonical_and_warns_about_state(self) -> None:
        match = re.search(
            r"<noscript[^>]*>(.*?)</noscript>",
            self.index,
            re.IGNORECASE | re.DOTALL,
        )
        self.assertIsNotNone(match, "index.html must include a <noscript> recovery block")
        block = match.group(1)
        parser = LinkParser()
        parser.feed(block)
        self.assertIn(
            self.manifest["canonical_quiz"],
            parser.links,
            "noscript block must link to the canonical quiz",
        )
        self.assertIn("JavaScript", block)
        self.assertRegex(block, r"查詢參數|深層連結|狀態")
        self.assertRegex(block, r"重新選擇")

    def test_default_recovery_covers_blocked_and_failed_scripts(self) -> None:
        attrs = self.parser.elements.get("recovery-note")
        self.assertIsNotNone(attrs, "recovery must exist outside noscript")
        self.assertNotIn("hidden", attrs)
        self.assertNotRegex(str(attrs.get("style") or ""), r"(?i)display\s*:\s*none|visibility\s*:\s*hidden")
        outside_noscript = re.sub(r"<noscript[^>]*>.*?</noscript>", "", self.index, flags=re.I | re.S)
        note = re.search(r'<p[^>]*id="recovery-note"[^>]*>(.*?)</p>', outside_noscript, re.S)
        self.assertIsNotNone(note)
        self.assertRegex(note.group(1), r"未啟用|停用")
        self.assertIn("封鎖", note.group(1))
        self.assertIn("初始化", note.group(1))
        self.assertIn("查詢條件", note.group(1))
        self.assertIn("錨點", note.group(1))
        self.assertIn("重新選擇", note.group(1))

    def test_manifest_and_readme_describe_failure_recovery(self) -> None:
        preserve = self.manifest["preserve_query_and_hash"]
        self.assertIn("default-visible", preserve["fallback"])
        self.assertIn("stateful link", preserve["script_initialization_failure"])
        self.assertIn("manual link retains query and hash", preserve["navigation_failure"])
        self.assertIn("初始化失敗", self.readme)
        self.assertIn("自動導向未成功", self.readme)
        self.assertIn("手動連結", self.readme)

    def test_readme_scopes_preservation_to_javascript_path(self) -> None:
        self.assertNotIn(
            "Query string 與 URL hash 會在重新導向時保留。",
            self.readme,
        )
        claims = [
            line
            for line in self.readme.splitlines()
            if "保留" in line and re.search(r"query|string|hash|查詢", line, re.IGNORECASE)
        ]
        self.assertTrue(claims, "README must still document query/hash handling")
        for line in claims:
            self.assertIn(
                "JavaScript",
                line,
                "preservation claim must state it only applies with JavaScript",
            )

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
        markup_and_styles = re.sub(r"<script[^>]*>.*?</script>", "", self.index, flags=re.I | re.S)
        self.assertNotRegex(markup_and_styles, r"(?i)@import|url\(|<img|<iframe|srcset")

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
