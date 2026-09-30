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
        self.meta_refresh_targets: list[str] = []
        self.noscript_links: list[str] = []
        self.noscript_text: list[str] = []
        self._noscript_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "noscript":
            self._noscript_depth += 1
        if tag == "a" and values.get("href"):
            self.links.append(str(values["href"]))
            if self._noscript_depth:
                self.noscript_links.append(str(values["href"]))
        if tag == "meta" and str(values.get("http-equiv") or "").lower() == "refresh":
            self.meta_refresh_targets.append(str(values.get("content") or ""))
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
        if tag == "noscript" and self._noscript_depth:
            self._noscript_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._noscript_depth:
            self.noscript_text.append(data)


class FusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = INDEX.read_text(encoding="utf-8")
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.readme = README.read_text(encoding="utf-8")
        cls.parser = LinkParser()
        cls.parser.feed(cls.index)
        cls.parser.close()

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
        self.assertTrue(self.manifest["preserve_query_and_hash"])
        self.assertIn("target.search = window.location.search", self.index)
        self.assertIn("target.hash = window.location.hash", self.index)
        self.assertIn("window.location.replace(target.href)", self.index)

    def test_no_parameter_dropping_meta_refresh(self) -> None:
        self.assertEqual(self.parser.meta_refresh_targets, [])
        self.assertNotRegex(self.index, r'(?i)http-equiv\s*=\s*["\']?\s*refresh')

    def test_noscript_recovery_message_and_link(self) -> None:
        self.assertIn("<noscript>", self.index)
        self.assertTrue(self.parser.noscript_links)
        self.assertIn(self.manifest["canonical_quiz"], self.parser.noscript_links)
        message = "".join(self.parser.noscript_text)
        self.assertIn("JavaScript", message)
        self.assertIn("重新", message)

    def test_preservation_scope_is_documented_as_javascript_only(self) -> None:
        self.assertEqual(
            self.manifest.get("preserve_query_and_hash_scope"),
            "javascript_enabled",
        )
        self.assertNotIn("Query string 與 URL hash 會在重新導向時保留。", self.readme)
        for claim in re.findall(r"[^。]*保留[^。]*", self.readme):
            self.assertIn("JavaScript", claim, claim)

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
