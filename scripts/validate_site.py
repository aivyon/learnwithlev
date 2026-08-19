#!/usr/bin/env python3
"""Fast, dependency-free checks for the static GitHub Pages site."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = (ROOT / "index.html", ROOT / "404.html")


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.links: list[tuple[str, str]] = []
        self.json_ld: list[str] = []
        self._in_json_ld = False
        self._json_chunks: list[str] = []
        self.html_attributes: dict[str, str | None] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_attributes = values
        if value := values.get("id"):
            if value in self.ids:
                self.duplicate_ids.add(value)
            self.ids.add(value)
        for attribute in ("href", "src"):
            if value := values.get(attribute):
                self.links.append((attribute, value))
        if tag == "script" and values.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_chunks = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_json_ld:
            self.json_ld.append("".join(self._json_chunks))
            self._in_json_ld = False

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._json_chunks.append(data)


def assert_local_target(source: Path, target: str, ids: set[str]) -> None:
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto", "tel"} or target.startswith("//"):
        return
    if parsed.path:
        path = ROOT / unquote(parsed.path.lstrip("/")) if parsed.path.startswith("/") else source.parent / unquote(parsed.path)
        if path.is_dir():
            path /= "index.html"
        assert path.exists(), f"Broken local target in {source.name}: {target}"
    if parsed.fragment and not parsed.path:
        assert parsed.fragment in ids, f"Missing fragment in {source.name}: #{parsed.fragment}"


def main() -> None:
    assert (ROOT / "CNAME").read_bytes() == b"learnwithlev.com", "CNAME changed"

    for page in HTML_FILES:
        source = page.read_text(encoding="utf-8")
        parser = SiteParser()
        parser.feed(source)

        assert parser.html_attributes.get("lang") == "he", f"{page.name}: lang must be he"
        assert parser.html_attributes.get("dir") == "rtl", f"{page.name}: dir must be rtl"
        assert not parser.duplicate_ids, f"{page.name}: duplicate IDs: {sorted(parser.duplicate_ids)}"

        for _, target in parser.links:
            assert_local_target(page, target, parser.ids)

        for payload in parser.json_ld:
            json.loads(payload)

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    required = (
        'rel="canonical"',
        'property="og:title"',
        'name="twitter:card"',
        'href="tel:+972523772425"',
        'href="mailto:contact@learnwithlev.com',
        'id="contact"',
    )
    for marker in required:
        assert marker in index, f"Missing required marker: {marker}"

    forbidden = ("lorem ipsum", "מאות תלמידים", "100%", "★★★★★")
    lowered = index.lower()
    for phrase in forbidden:
        assert phrase.lower() not in lowered, f"Forbidden placeholder or claim: {phrase}"

    print("Site validation passed: local links, anchors, metadata, JSON-LD, claims, and CNAME.")


if __name__ == "__main__":
    main()
