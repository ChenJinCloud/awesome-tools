#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import socket
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import ProxyHandler, build_opener


OPENER = build_opener(ProxyHandler({}))


@dataclass
class ProbeResult:
    status: str
    reason: str
    endpoint: str | None = None
    http_status: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason": self.reason,
            "endpoint": self.endpoint,
            "http_status": self.http_status,
        }


def is_loopback_host(host: str | None) -> bool:
    if not host:
        return False
    normalized = host.strip("[]").lower()
    if normalized in {"localhost", "127.0.0.1", "::1"}:
        return True
    try:
        return socket.gethostbyname(normalized).startswith("127.")
    except socket.gaierror:
        return False


def request_json(base_url: str, path: str, params: dict[str, str], timeout: int) -> Any:
    url = base_url.rstrip("/") + path
    if params:
        url += "?" + urlencode(params)
    with OPENER.open(url, timeout=timeout) as resp:
        data = resp.read()
    return json.loads(data.decode("utf-8-sig"))


def probe(base_url: str, timeout: int = 10) -> ProbeResult:
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"}:
        return ProbeResult("not_ready", "base_url must use http or https")
    if not is_loopback_host(parsed.hostname):
        return ProbeResult("unsafe_target", "service URL must point to loopback")

    probes = [
        ("/api/v1/session", {"format": "json", "limit": "1"}),
        ("/api/v1/contact", {"format": "json", "limit": "1"}),
    ]
    last_error = "no probe attempted"
    for endpoint, params in probes:
        try:
            payload = request_json(base_url, endpoint, params, timeout)
            if isinstance(payload, (dict, list)):
                return ProbeResult("ready", "harmless API probe returned JSON", endpoint=endpoint)
            last_error = "API returned non-JSON-shaped payload"
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace").lower()
            if exc.code == 503 and "decrypt" in body:
                return ProbeResult("decrypting", "database is still decrypting", endpoint=endpoint, http_status=exc.code)
            if exc.code in {400, 401, 403, 404, 500, 503}:
                last_error = f"HTTP {exc.code} from {endpoint}"
            else:
                last_error = f"unexpected HTTP {exc.code} from {endpoint}"
        except (URLError, TimeoutError) as exc:
            last_error = f"connection failed: {exc}"
        except json.JSONDecodeError:
            last_error = f"{endpoint} did not return JSON"
    return ProbeResult("not_ready", last_error)


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe a local chatlog-compatible HTTP service.")
    parser.add_argument("--base-url", default="http://127.0.0.1:5030")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()

    result = probe(args.base_url, timeout=args.timeout)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0 if result.status == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
