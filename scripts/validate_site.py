from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ROOT / "index.html",
    ROOT / "privacy/index.html",
    ROOT / "support/index.html",
    ROOT / "404.html",
]
REQUIRED_POLICY_TOKENS = {
    # プライバシーポリシーは App Store Connect の「プライバシーポリシー URL」に登録する。
    # アプリが実際に使う SDK と権限の説明が消えると、審査での説明と食い違う。
    "privacy/index.html": [
        "プライバシーポリシー",
        "Privacy Policy",
        "2026年9月14日",
        "September 14, 2026",
        "Vlogue 開発者",
        "Vlogue Developer",
        "koachan.dev@gmail.com",
        "AdMob",
        "MapKit",
        "WeatherKit",
        "ヘルスケア",
        "Health",
        "カメラ",
        "Camera",
        "位置情報",
        "Location",
    ],
    # サポートページは App Store Connect の「サポート URL」に登録する。
    # 連絡先が消えると審査で落ちるので、載っていることを見張る。
    "support/index.html": [
        "サポート",
        "Support",
        "koachan.dev@gmail.com",
        "購入を復元",
        "Restore Purchases",
        "Vlogue Pro",
        "3回",
        "three times",
        "モザイク",
        "mosaic",
        "Vlogue 開発者",
        "Vlogue Developer",
    ],
}
FORBIDDEN = [
    "google-analytics",
    "googletagmanager",
    "facebook.net",
    "<script",
    "document.cookie",
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_depth = 0
        self.title = ""
        self.links: list[str] = []
        self.lang_values: set[str] = set()

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        if tag == "title":
            self.title_depth += 1
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if values.get("lang"):
            self.lang_values.add(values["lang"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title += data


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def resolve_link(page: Path, href: str) -> Path | None:
    parsed = urlparse(href)
    if parsed.scheme in {"https", "mailto"} or href.startswith("#"):
        return None
    if parsed.scheme or href.startswith("//"):
        fail(f"unsupported link in {page.relative_to(ROOT)}: {href}")
    target = (page.parent / parsed.path).resolve()
    if parsed.path.endswith("/"):
        target /= "index.html"
    return target


def validate() -> None:
    for page in PAGES:
        if not page.is_file():
            fail(f"missing {page.relative_to(ROOT)}")
        source = page.read_text(encoding="utf-8")
        lowered = source.lower()
        for token in FORBIDDEN:
            if token in lowered:
                fail(
                    f"forbidden tracker/script token {token} "
                    f"in {page.relative_to(ROOT)}"
                )
        parser = PageParser()
        parser.feed(source)
        if not parser.title.strip():
            fail(f"missing title in {page.relative_to(ROOT)}")
        for href in parser.links:
            target = resolve_link(page, href)
            if target is not None and not target.exists():
                fail(f"broken link in {page.relative_to(ROOT)}: {href}")
        key = str(page.relative_to(ROOT))
        for token in REQUIRED_POLICY_TOKENS.get(key, []):
            if token not in source:
                fail(f"missing policy token {token!r} in {key}")

    css = ROOT / "assets/site.css"
    if not css.is_file():
        fail("missing assets/site.css")
    print("Legal site validation passed")


if __name__ == "__main__":
    validate()
