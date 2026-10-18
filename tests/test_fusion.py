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
        self.meta_refreshes: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
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
        if tag == "meta" and str(values.get("http-equiv") or "").strip().lower() == "refresh":
            self.meta_refreshes.append(str(values.get("content") or ""))

    def handle_data(self, data: str) -> None:
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
        self.assertTrue(self.manifest["preserve_query_and_hash"])
        self.assertIn("target.search = window.location.search", self.index)
        self.assertIn("target.hash = window.location.hash", self.index)
        self.assertIn("window.location.replace(target.href)", self.index)

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

    def test_no_parameter_dropping_meta_refresh(self) -> None:
        self.assertEqual(self.parser.meta_refreshes, [])

    def test_nojs_recovery_message_and_link(self) -> None:
        recovery = re.search(r"<noscript\b[^>]*>(.*?)</noscript\s*>", self.index, re.S | re.I)
        self.assertIsNotNone(recovery)
        parser = LinkParser()
        parser.feed(recovery.group(1))
        self.assertIn(self.manifest["canonical_quiz"], parser.links)
        for text in ("JavaScript", "深度連結", "重新設定", "新版模擬考"):
            self.assertIn(text, "".join(parser.text))

    def test_script_failure_has_static_recovery_warning(self) -> None:
        status = re.search(
            r'<p\b[^>]*id="redirect-status"[^>]*>(.*?)</p>', self.index, re.S
        )
        self.assertIsNotNone(status)
        for text in ("JavaScript", "深度連結", "重新設定"):
            self.assertIn(text, status.group(1))

    def test_fallback_checks_reject_regressions(self) -> None:
        nojs = "<noscript><p>JavaScript 無法執行時，搜尋條件與深度連結須重新設定。</p></noscript>"
        mutations = [
            ("test_nojs_recovery_message_and_link", "<noscript></noscript>"),
            ("test_nojs_recovery_message_and_link", nojs),
            (
                "test_nojs_recovery_message_and_link",
                '<noscript><a href="' + self.manifest["canonical_quiz"] + '">新版模擬考</a></noscript>',
            ),
            (
                "test_no_parameter_dropping_meta_refresh",
                "<meta http-equiv='refresh' content='2;url=" + self.manifest["canonical_quiz"] + "'>",
            ),
            (
                "test_no_parameter_dropping_meta_refresh",
                '<META HTTP-EQUIV="Refresh" CONTENT="2;url=' + self.manifest["canonical_quiz"] + '">',
            ),
        ]
        for test_name, replacement in mutations:
            with self.subTest(test=test_name, replacement=replacement):
                case = FusionTests(test_name)
                if test_name == "test_nojs_recovery_message_and_link":
                    case.index = re.sub(r"<noscript>.*?</noscript>", replacement, self.index, flags=re.S)
                else:
                    case.index = self.index.replace("<head>", "<head>" + replacement)
                case.parser = LinkParser()
                case.parser.feed(case.index)
                with self.assertRaises(AssertionError):
                    getattr(case, test_name)()


if __name__ == "__main__":
    unittest.main()
