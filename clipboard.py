#!/usr/bin/env python3
"""
clipboard.py - Universal TTL clipboard capture

Purpose:
- Watch the system clipboard for conversation text copied from ANY LLM platform.
- When new text is detected, offer to save it as a TTL module.
- Use the provider-agnostic TTLSDK (ttl_sdk.py) for storage + export.

Requirements:
- ttl_sdk.py in the same directory.
- pyperclip: pip install pyperclip
"""

from __future__ import annotations

import sys
import time
from typing import List, Dict

import pyperclip  # type: ignore

from ttl_sdk import TTLSDK


# How long to sleep between clipboard checks (seconds)
POLL_INTERVAL = 1.0

# Minimum size of clipboard text to consider it a conversation
MIN_CHARS_FOR_CAPTURE = 200


def prompt_metadata() -> Dict[str, object]:
    """
    Ask the user for LLM metadata in a universal way.
    """
    print("\n=== TTL Metadata ===")

    creator = input("Creator (your name / handle) [default: unknown]: ").strip() or "unknown"

    llm_provider = input(
        "LLM Provider (openai/anthropic/google/local/other) [default: unknown]: "
    ).strip() or "unknown"

    model_name = input(
        "Model name (e.g., gpt-4.1, claude-3.5-sonnet, gemini-1.5-pro) [default: unknown]: "
    ).strip() or "unknown"

    platform = input(
        "Platform / Surface (chatgpt-web, poe, cursor, api, notebook, other) [default: unknown]: "
    ).strip() or "unknown"

    conversation_type = input(
        "Conversation type (coding/research/business/general/other) [default: general]: "
    ).strip() or "general"

    raw_tags = input(
        "Tags (comma-separated, e.g. python, sdk, ttl) [optional]: "
    ).strip()

    tags: List[str] = []
    if raw_tags:
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

    return {
        "creator": creator,
        "llm_provider": llm_provider,
        "model_name": model_name,
        "platform": platform,
        "conversation_type": conversation_type,
        "tags": tags,
    }


def capture_once_from_clipboard() -> None:
    """
    Capture the CURRENT clipboard contents once and create a TTL module.
    Useful when you already copied a conversation and just want to save it.
    """
    try:
        text = pyperclip.paste()
    except pyperclip.PyperclipException as e:
        print(f"[ERROR] Unable to access clipboard: {e}")
        return

    if not text or not text.strip():
        print("❌ Clipboard is empty or non-text. Copy a conversation and try again.")
        return

    if len(text) < MIN_CHARS_FOR_CAPTURE:
        print(
            f"⚠️ Clipboard text is quite short ({len(text)} chars). "
            f"If this is really a full conversation, continue."
        )

    print("\n=== Clipboard Preview (first 600 chars) ===")
    preview = text[:600]
    print(preview)
    if len(text) > 600:
        print("... [truncated]\n")

    confirm = input("Save this clipboard content as a TTL module? [y/N]: ").strip().lower()
    if confirm not in ("y", "yes"):
        print("ℹ️ Capture cancelled.")
        return

    metadata = prompt_metadata()

    sdk = TTLSDK()
    result = sdk.create_module(
        creator=metadata["creator"],
        content=text,
        llm_provider=metadata["llm_provider"],
        model_name=metadata["model_name"],
        platform=metadata["platform"],
        conversation_type=metadata["conversation_type"],
        tags=metadata["tags"],
    )

    exports = sdk.export_module(result["module_id"], formats=["markdown", "html"])

    print(f"\n✅ TTL module created: {result['module_id']}")
    print("📤 Exported:")
    for fmt, path in exports.items():
        print(f"   {fmt}: {path}")


def watch_clipboard() -> None:
    """
    Continuous clipboard watcher.

    Flow:
    - Poll clipboard every POLL_INTERVAL.
    - If new text appears, and it's "big enough", show a preview.
    - Ask user if they want to capture it as a TTL module.
    - Ask metadata, then save + export.

    This is UNIVERSAL:
    - You can copy from ChatGPT, Claude, Gemini, local models, etc.
    - The only contract is: you copy the conversation, we see it.
    """
    print("=" * 70)
    print("TTL Clipboard Watcher (Universal LLM Capture)")
    print("=" * 70)
    print("\nInstructions:")
    print("  1) Interact with ANY LLM (web, app, IDE, local, etc.).")
    print("  2) When you have a conversation worth saving, SELECT ALL + COPY.")
    print("  3) This watcher will detect the new clipboard content.")
    print("  4) It will ask if you want to save it as a TTL module.\n")
    print("Press Ctrl+C to exit.\n")

    sdk = TTLSDK()
    last_text = ""

    while True:
        try:
            try:
                current = pyperclip.paste()
            except pyperclip.PyperclipException as e:
                print(f"[ERROR] Unable to access clipboard: {e}")
                time.sleep(POLL_INTERVAL)
                continue

            if not isinstance(current, str):
                time.sleep(POLL_INTERVAL)
                continue

            # Only react when clipboard content changes and is non-trivial
            if current != last_text and current.strip():
                if len(current) >= MIN_CHARS_FOR_CAPTURE:
                    print("\n=== New clipboard content detected ===")
                    preview = current[:600]
                    print("\nPreview (first 600 chars):")
                    print(preview)
                    if len(current) > 600:
                        print("... [truncated]\n")

                    choice = input(
                        "Save this as a TTL module? [y]es / [n]o / [s]kip & stop watching: "
                    ).strip().lower()

                    if choice in ("y", "yes"):
                        metadata = prompt_metadata()
                        result = sdk.create_module(
                            creator=metadata["creator"],
                            content=current,
                            llm_provider=metadata["llm_provider"],
                            model_name=metadata["model_name"],
                            platform=metadata["platform"],
                            conversation_type=metadata["conversation_type"],
                            tags=metadata["tags"],
                        )
                        exports = sdk.export_module(
                            result["module_id"], formats=["markdown", "html"]
                        )

                        print(f"\n✅ TTL module created: {result['module_id']}")
                        print("📤 Exported:")
                        for fmt, path in exports.items():
                            print(f"   {fmt}: {path}")

                        # Update last_text so we don't re-trigger on same content
                        last_text = current

                    elif choice in ("s", "stop"):
                        print("🛑 Stopping clipboard watcher.")
                        return
                    else:
                        print("ℹ️ Ignored this clipboard content.")
                        last_text = current  # Don't keep nagging about the same text

                else:
                    # Text changed but is too small to be a conversation
                    last_text = current

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Exiting clipboard watcher.")
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error in watcher loop: {e}")
            time.sleep(POLL_INTERVAL)


def main() -> None:
    """
    Entry point.

    Modes:
      python clipboard.py          -> watch mode (continuous)
      python clipboard.py once     -> capture current clipboard once
    """
    if len(sys.argv) > 1 and sys.argv[1].lower() == "once":
        capture_once_from_clipboard()
    else:
        watch_clipboard()


if __name__ == "__main__":
    main()
