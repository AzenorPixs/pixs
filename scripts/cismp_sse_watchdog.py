#!/usr/bin/env python3
"""Surveille l'état SSE agrégé du RUN CISMP sans prendre de décision CAB."""

from __future__ import annotations

import json
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen


CONTROLLER_STATUS_URL = "http://127.0.0.1:8788/status"
OPENCODE_SESSION_URL = (
    "http://127.0.0.1:4096/session/"
    "ses_f383393baffeH1bDdJtOxSSYi3"
)
OPENCODE_MESSAGES_URL = (
    f"{OPENCODE_SESSION_URL}/message?directory=/home/devops/datas/pixs&limit=1"
)
PROJECT_DIRECTORY = "/home/devops/datas/pixs"


def request_json(url: str, payload: dict[str, object] | None = None) -> object:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=data,
        headers={"content-type": "application/json"},
        method="POST" if data is not None else "GET",
    )
    with urlopen(request, timeout=10) as response:
        return json.load(response)


def latest_text() -> str:
    messages = request_json(OPENCODE_MESSAGES_URL)
    if not isinstance(messages, list) or not messages:
        return ""
    parts = messages[-1].get("parts", [])
    return "\n".join(
        part.get("text", "")
        for part in parts
        if isinstance(part, dict) and part.get("type") == "text"
    )


def main() -> int:
    try:
        status = request_json(CONTROLLER_STATUS_URL)
        readiness = status["brokerReadiness"]
        broker_status = readiness["status"]
        pending_count = readiness["pending_count"]
        session_state = readiness["session_state"]
    except (KeyError, TypeError, URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"CISMP_SSE_WATCHDOG_ERROR: {error}", file=sys.stderr)
        return 1

    if broker_status != "READY":
        print(f"CISMP_SSE_WATCHDOG_WAIT_CAB: broker={broker_status}")
        return 0
    if pending_count:
        print(f"CISMP_SSE_WATCHDOG_WAIT_CAB: pending={pending_count}")
        return 0
    if session_state != "IDLE":
        print(f"CISMP_SSE_WATCHDOG_ACTIVE: session_state={session_state}")
        return 0

    try:
        text = latest_text()
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"CISMP_SSE_WATCHDOG_ERROR: {error}", file=sys.stderr)
        return 1

    if "WAIT_CGPT" in text or "NFDOC" in text or "NDOC" in text:
        print("CISMP_SSE_WATCHDOG_WAIT_CGPT")
        return 0

    payload = {
        "agent": "build",
        "parts": [
            {
                "type": "text",
                "text": (
                    "Reprise CISMP watchdog : relis l'état réel, applique CAB et "
                    "reprends uniquement le premier état non prouvé. Si une décision "
                    "CGPT ou CAB est nécessaire, attends le mandat corrélé."
                ),
            }
        ],
    }
    try:
        request_json(
            f"{OPENCODE_SESSION_URL}/message?directory={PROJECT_DIRECTORY}", payload
        )
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"CISMP_SSE_WATCHDOG_ERROR: {error}", file=sys.stderr)
        return 1

    print("CISMP_SSE_WATCHDOG_RESUMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
