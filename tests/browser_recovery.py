"""Opt-in isolated Chromium acceptance tests; no requests reach the canonical site.

Run with the locally available Playwright package and Chromium:
    python tests/browser_recovery.py --report /tmp/browser-recovery.json
"""
from __future__ import annotations

import argparse
import json
import re
import unittest
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "https://reese-max.github.io/police-exam-archive/quiz.html"
LEGACY = "http://127.0.0.1:8765/index.html"
STATE = "?subject=police-law#question-12"


class BrowserRecoveryTests(unittest.TestCase):
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    observations: list[dict] = []

    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(
            executable_path="/usr/bin/chromium", headless=True, args=["--no-sandbox"]
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = None

    def tearDown(self):
        if self.context:
            self.context.close()

    def open_page(self, *, javascript=True, blocked=False, init=None, replace=None, state=STATE):
        html = self.html
        if replace:
            # Location.replace is non-configurable in Chromium. Inject only at
            # this call site in the served test copy; keep real DOM/timers intact.
            call = "window.location.replace(target.href);"
            self.assertEqual(html.count(call), 1)
            replacement = "window.__replaceTarget = target.href;"
            if replace == "throw":
                replacement += ' throw new Error("injected replace failure");'
            html = html.replace(call, replacement)
        self.context = self.browser.new_context(java_script_enabled=javascript)
        requests = []

        def intercept(route):
            url = route.request.url
            requests.append(url)
            if url.startswith(LEGACY):
                headers = {"Content-Type": "text/html; charset=utf-8"}
                if blocked:
                    headers["Content-Security-Policy"] = "script-src 'none'; style-src 'unsafe-inline'"
                route.fulfill(status=200, headers=headers, body=html)
            elif url.startswith(CANONICAL):
                route.fulfill(status=200, content_type="text/html", body="<p>Isolated canonical stub</p>")
            else:
                route.abort()

        self.context.route("**/*", intercept)
        if init:
            self.context.add_init_script(init)
        page = self.context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(LEGACY + state, wait_until="domcontentloaded")
        self.page = page
        self.requests = requests
        self.errors = errors
        return page

    def recovery(self, *, stateful=False):
        self.page.wait_for_timeout(1450)
        self.assertEqual(self.page.url, LEGACY + STATE)
        note = self.page.locator("#recovery-note")
        self.assertTrue(note.is_visible(), "default recovery must survive unavailable or failed scripts")
        text = note.inner_text()
        self.assertRegex(text, r"查詢|錨點")
        self.assertRegex(text, r"重新選擇|已保留")
        expected = CANONICAL + (STATE if stateful else "")
        link = self.page.locator("#continue-link")
        self.assertTrue(link.is_visible())
        self.assertEqual(link.get_attribute("href"), expected)
        if "location_replace" in self._testMethodName:
            self.assertEqual(self.page.evaluate("window.__replaceTarget"), expected)
        self.observations.append({"scenario": self._testMethodName, "legacy_url": self.page.url,
                                  "manual_target": expected, "recovery": text, "page_errors": self.errors})
        # Tab/Enter exercises the actual focusable anchor and browser navigation.
        self.page.keyboard.press("Tab")
        if not link.evaluate("node => node === document.activeElement"):
            # The preserved noscript anchor precedes the primary link when JS is disabled.
            self.page.keyboard.press("Tab")
        self.assertTrue(link.evaluate("node => node === document.activeElement"))
        self.page.keyboard.press("Enter")
        self.page.wait_for_url(expected)
        self.assertEqual(self.page.url, expected)

    def test_normal_redirect_preserves_exact_state(self):
        states = [STATE, "", "?subject=a&subject=b&empty=&encoded=%2f%2F+%20#%E9%A1%8C-12"]
        for state in states:
            with self.subTest(state=state):
                page = self.open_page(state=state)
                self.assertEqual(page.locator("#continue-link").get_attribute("href"), CANONICAL + state)
                self.assertFalse(page.locator("#recovery-note").is_visible())
                page.wait_for_url(CANONICAL + state)
                self.assertEqual(page.url, CANONICAL + state)
                # replace must remove the legacy entry from browser history.
                self.assertEqual(page.evaluate("history.length"), 2)
                self.assertEqual(self.errors, [])
                self.observations.append({"scenario": self._testMethodName, "final_url": page.url})
                self.context.close()
                self.context = None

    def test_manual_link_preserves_state_before_timer(self):
        page = self.open_page()
        page.locator("#continue-link").click()
        page.wait_for_url(CANONICAL + STATE)
        self.assertEqual(page.url, CANONICAL + STATE)
        self.observations.append({"scenario": self._testMethodName, "final_url": page.url})

    def test_javascript_disabled(self):
        page = self.open_page(javascript=False)
        self.assertTrue(page.locator("noscript .noscript-note").is_visible())
        self.recovery()

    def test_inline_script_blocked_by_csp(self):
        self.open_page(blocked=True)
        self.recovery()

    def test_throw_before_initialization(self):
        original = self.html
        try:
            self.html = re.sub(r"(<script[^>]*>)", r'\1throw new Error("injected early failure");', original, count=1)
            self.open_page()
            self.recovery()
            self.assertTrue(any("injected early failure" in error for error in self.errors))
        finally:
            self.html = original

    def test_url_initialization_throws(self):
        self.open_page(init='window.URL = function () { throw new Error("injected URL failure"); };')
        self.recovery()
        self.assertEqual(self.errors, [])

    def test_timer_scheduling_throws_after_link_ready(self):
        self.open_page(init='window.setTimeout = function () { throw new Error("injected timer failure"); };')
        self.recovery(stateful=True)
        self.assertEqual(self.errors, [])

    def test_location_replace_throws(self):
        self.open_page(replace="throw")
        self.recovery(stateful=True)
        self.assertEqual(self.errors, [])

    def test_location_replace_does_not_navigate(self):
        self.open_page(replace="noop")
        self.recovery(stateful=True)
        self.assertEqual(self.errors, [])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, default=ROOT / "index.html")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    BrowserRecoveryTests.html = args.html.read_text(encoding="utf-8")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BrowserRecoveryTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.report:
        args.report.write_text(json.dumps({"source": str(args.html), "browser": "/usr/bin/chromium",
            "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
            "network": "all requests intercepted; no live canonical requests",
            "observations": BrowserRecoveryTests.observations}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise SystemExit(not result.wasSuccessful())
