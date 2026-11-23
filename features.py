import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = ["login", "verify", "secure", "account", "update",
                    "bank", "paypal", "signin", "confirm", "password"]

def extract_features(url):
    url = str(url).strip()
    full = url if "://" in url else "http://" + url
    try:
        host = urlparse(full).netloc.lower()
    except ValueError:
        host = ""
    lower = url.lower()

    return {
        "url_length": len(url),
        "host_length": len(host),
        "dots": url.count("."),
        "hyphens": url.count("-"),
        "slashes": url.count("/"),
        "digits": sum(c.isdigit() for c in url),
        "question_marks": url.count("?"),
        "equals": url.count("="),
        "has_at": int("@" in url),
        "has_https": int(lower.startswith("https")),
        "has_ip": int(bool(re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}(:\d+)?", host))),
        "subdomains": max(host.count(".") - 1, 0),
        "suspicious_words": sum(w in lower for w in SUSPICIOUS_WORDS),
    }