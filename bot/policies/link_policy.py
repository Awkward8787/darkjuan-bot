import re
from dataclasses import dataclass
from typing import List


URL_REGEX = re.compile(r"https?://[^\s]+", re.IGNORECASE)
SUSPICIOUS_TLDS = {".ru", ".tk", ".cn", ".top", ".gq", ".ml", ".ga", ".cf"}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "cutt.ly"}


@dataclass
class LinkCheckResult:
    urls: List[str]
    suspicious: bool
    reason: str | None = None


def inspect_links(text: str) -> LinkCheckResult:
    urls = URL_REGEX.findall(text)
    if not urls:
        return LinkCheckResult(urls=[], suspicious=False, reason=None)

    for url in urls:
        host_match = re.search(r"https?://([^/]+)/?", url, re.IGNORECASE)
        host = host_match.group(1).lower() if host_match else ""
        if any(host.endswith(tld) for tld in SUSPICIOUS_TLDS):
            return LinkCheckResult(urls=urls, suspicious=True, reason="Suspicious TLD")
        if host in SHORTENERS:
            return LinkCheckResult(urls=urls, suspicious=True, reason="URL shortener")

    return LinkCheckResult(urls=urls, suspicious=False, reason=None)
