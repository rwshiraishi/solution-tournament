#!/usr/bin/env python3
"""Cross-vendor scorer transport for solution-tournament full mode.

Sends a fully assembled scorer packet (the same text a Claude scorer
subagent would receive) to an OpenAI chat model and prints the raw
completion to stdout. This is a dumb transport: all scoring
instructions live in the packet; nothing is added or removed here.

Usage:
    python3 cross_model_score.py PACKET_FILE [--model NAME] [--timeout SECONDS]

Model resolution: --model flag, else ST_CROSS_MODEL env var. There is
deliberately no baked-in default model name.

Exit codes (the skill's fallback rule branches on nonzero):
    0 success (completion printed to stdout)
    2 OPENAI_API_KEY not set
    3 network or HTTP error
    4 unexpected response shape
    5 usage error (bad args, unreadable packet, no model named)
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import NoReturn

API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_TIMEOUT_SECONDS = 180


def fail(code: int, message: str) -> NoReturn:
    print(f"cross_model_score: {message}", file=sys.stderr)
    sys.exit(code)


class UsageErrorParser(argparse.ArgumentParser):
    """Remap argparse's default exit code 2 for usage mistakes to this
    script's documented code 5, so callers can distinguish a bad flag
    from a missing API key (which owns code 2)."""

    def error(self, message: str) -> NoReturn:
        fail(5, f"usage error: {message}")


def main() -> None:
    parser = UsageErrorParser(add_help=True)
    parser.add_argument("packet_file")
    parser.add_argument("--model", default=os.environ.get("ST_CROSS_MODEL", ""))
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    args = parser.parse_args()

    if not args.model:
        fail(5, "no model named: pass --model or set ST_CROSS_MODEL")

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        fail(2, "OPENAI_API_KEY not set")

    try:
        with open(args.packet_file, "r", encoding="utf-8") as f:
            packet = f.read()
    except OSError as e:
        fail(5, f"cannot read packet file: {e}")

    if not packet.strip():
        fail(5, "packet file is empty")

    body = json.dumps(
        {
            "model": args.model,
            "messages": [{"role": "user", "content": packet}],
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as e:
        # Read the error body for diagnostics but never echo request headers.
        # Assumes the API never reflects the Authorization header back in
        # error bodies (true for OpenAI today); the 500-char cap limits any
        # future surprise.
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")[:500]
        except OSError:
            pass
        fail(3, f"HTTP {e.code} from API: {detail}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        fail(3, f"network error: {e}")
    except json.JSONDecodeError as e:
        fail(4, f"response is not JSON: {e}")

    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        fail(4, f"unexpected response shape: keys={sorted(payload)[:10]}")

    if not isinstance(content, str) or not content.strip():
        fail(4, "empty completion")

    sys.stdout.write(content)


if __name__ == "__main__":
    main()
