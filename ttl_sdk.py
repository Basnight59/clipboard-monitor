#!/usr/bin/env python3
"""
TTL SDK - Truth, Trust, Liberation
Provider-agnostic SDK implementation.

Goals:
- UNIVERSAL across LLM platforms (OpenAI, Anthropic, Google, local, etc.)
- Conversation capture + module storage
- Markdown and HTML export
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# ============================================================================
# CONFIG
# ============================================================================

DEFAULT_ROOT = "ttl_data"


# ============================================================================
# DATA MODEL
# ============================================================================

@dataclass
class TTLModule:
    """
    Represents a single captured conversation "module".

    Key concepts:
    - llm_provider: 'openai', 'anthropic', 'google', 'local', 'other', etc.
    - model_name:   'gpt-4.1', 'claude-3.5-sonnet', 'gemini-1.5-pro', etc.
    - platform:     surface where it happened: 'chatgpt-web', 'poe', 'cursor',
                    'api', 'notebook', etc.
    """
    module_id: str
    creator: str

    # LLM-related metadata
    llm_provider: str          # openai / anthropic / google / local / other
    model_name: str            # gpt-4.1 / claude-3.5-sonnet / etc.
    platform: str              # ui or runtime surface (chatgpt-web, api, etc.)

    conversation_type: str     # coding / research / business / general / etc.
    tags: List[str]

    created_at: str            # ISO datetime (UTC)
    content: str               # raw conversation text


# ============================================================================
# STORAGE LAYER
# ============================================================================

class TTLStorage:
    """
    Handles saving and loading modules to/from disk.

    Layout:

    ttl_data/
      modules/
        2025-12-09/
          openai-coding-20251209084450_meta.json
          openai-coding-20251209084450_content.txt
      exports/
        openai-coding-20251209084450.md
        openai-coding-20251209084450.html
    """

    def __init__(self, root_dir: str = DEFAULT_ROOT) -> None:
        self.root = Path(root_dir)
        (self.root / "modules").mkdir(parents=True, exist_ok=True)
        (self.root / "exports").mkdir(parents=True, exist_ok=True)

    def _safe_join(self, *parts: str) -> Path:
        """
        Very simple path traversal protection.
        Only allows relative, normalized paths under self.root.
        """
        base = self.root
        path = base.joinpath(*parts).resolve()
        if not str(path).startswith(str(base.resolve())):
            raise ValueError("Unsafe path detected")
        return path

    def save_module(self, module: TTLModule) -> Dict[str, str]:
        """
        Save metadata and content for a module.
        Returns dict with paths for reference.
        """
        try:
            date_str = module.created_at[:10]  # YYYY-MM-DD
            day_dir = self._safe_join("modules", date_str)
            day_dir.mkdir(parents=True, exist_ok=True)

            meta_path = day_dir / f"{module.module_id}_meta.json"
            content_path = day_dir / f"{module.module_id}_content.txt"

            meta = asdict(module).copy()
            content = meta.pop("content", "")

            with meta_path.open("w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)

            with content_path.open("w", encoding="utf-8") as f:
                f.write(content)

            print(f"  Metadata: {meta_path}")
            print(f"  Content:  {content_path}")

            return {
                "meta_path": str(meta_path),
                "content_path": str(content_path),
            }

        except Exception as e:
            print(f"[ERROR] Failed to save module: {e}")
            return {}

    def load_module(self, module_id: str) -> Optional[TTLModule]:
        """
        Locate a module by ID by scanning modules directory.
        """
        modules_root = self._safe_join("modules")
        if not modules_root.exists():
            return None

        meta_file = None
        content_file = None

        for root, _, files in os.walk(modules_root):
            for name in files:
                if name == f"{module_id}_meta.json":
                    meta_file = Path(root) / name
                elif name == f"{module_id}_content.txt":
                    content_file = Path(root) / name

        if not meta_file or not content_file:
            return None

        try:
            with meta_file.open("r", encoding="utf-8") as f:
                meta = json.load(f)
            with content_file.open("r", encoding="utf-8") as f:
                content = f.read()

            return TTLModule(
                module_id=module_id,
                creator=meta.get("creator", ""),

                llm_provider=meta.get("llm_provider", "unknown"),
                model_name=meta.get("model_name", "unknown"),
                platform=meta.get("platform", "unknown"),

                conversation_type=meta.get("conversation_type", "general"),
                tags=meta.get("tags", []),
                created_at=meta.get("created_at", ""),
                content=content,
            )
        except Exception as e:
            print(f"[ERROR] Failed to load module {module_id}: {e}")
            return None

    def get_exports_dir(self) -> Path:
        return self._safe_join("exports")


# ============================================================================
# EXPORT LAYER
# ============================================================================

class TTLExport:
    """
    Handles export of modules to different formats.
    """

    def __init__(self, storage: TTLStorage) -> None:
        self.storage = storage
        self.export_root = self.storage.get_exports_dir()
        self.export_root.mkdir(parents=True, exist_ok=True)

    def export_markdown(self, module: TTLModule) -> str:
        """
        Export module as Markdown.
        """
        md_path = self.export_root / f"{module.module_id}.md"

        lines: List[str] = []
        lines.append(f"# TTL Module: {module.module_id}")
        lines.append("")
        lines.append("## Metadata")
        lines.append("")
        lines.append(f"- Creator: `{module.creator}`")
        lines.append(f"- LLM Provider: `{module.llm_provider}`")
        lines.append(f"- Model: `{module.model_name}`")
        lines.append(f"- Platform: `{module.platform}`")
        lines.append(f"- Type: `{module.conversation_type}`")
        lines.append(f"- Created (UTC): `{module.created_at}`")
        if module.tags:
            tag_str = ", ".join(module.tags)
            lines.append(f"- Tags: `{tag_str}`")
        lines.append("")
        lines.append("## Conversation")
        lines.append("")
        lines.append("```text")
        lines.append(module.content)
        lines.append("```")
        lines.append("")

        md_path.write_text("\n".join(lines), encoding="utf-8")
        return str(md_path)

    def export_html(self, module: TTLModule) -> str:
        """
        Export module as very simple HTML.
        """
        html_path = self.export_root / f"{module.module_id}.html"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>TTL Module {module.module_id}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 2rem; }}
    pre {{ white-space: pre-wrap; font-family: Consolas, "Liberation Mono", monospace; }}
    .meta {{ font-size: 0.9rem; color: #555; margin-bottom: 1rem; }}
    h1 {{ margin-bottom: 0.25rem; }}
  </style>
</head>
<body>
  <h1>TTL Module: {module.module_id}</h1>
  <div class="meta">
    <div><strong>Creator:</strong> {module.creator}</div>
    <div><strong>LLM Provider:</strong> {module.llm_provider}</div>
    <div><strong>Model:</strong> {module.model_name}</div>
    <div><strong>Platform:</strong> {module.platform}</div>
    <div><strong>Type:</strong> {module.conversation_type}</div>
    <div><strong>Created (UTC):</strong> {module.created_at}</div>
    <div><strong>Tags:</strong> {", ".join(module.tags)}</div>
  </div>
  <h2>Conversation</h2>
  <pre>{self._escape_html(module.content)}</pre>
</body>
</html>
"""
        html_path.write_text(html, encoding="utf-8")
        return str(html_path)

    @staticmethod
    def _escape_html(text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )


# ============================================================================
# SDK FACADE
# ============================================================================

class TTLSDK:
    """
    High-level SDK used by your scripts, demos, tools, and agents.

    Design decisions:
    - This SDK does NOT depend on any specific LLM API.
      You integrate providers in your own code and pass the
      resulting conversation + metadata into TTLSDK.
    """

    def __init__(self, root_dir: str = DEFAULT_ROOT) -> None:
        self.root_dir = root_dir
        self.storage = TTLStorage(root_dir)
        self.export = TTLExport(self.storage)

    def create_module(
        self,
        *,
        creator: str,
        content: str,
        llm_provider: str = "unknown",     # openai / anthropic / google / local / other
        model_name: str = "unknown",
        platform: str = "unknown",         # chatgpt-web / api / etc.
        conversation_type: str = "general",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, object]:
        """
        Create a TTL module from conversation content and metadata.

        NOTE: All arguments are keyword-only by design to keep you honest.
        """
        if tags is None:
            tags = []

        provider_slug = (llm_provider or "unknown").lower().replace(" ", "-")
        conv_slug = (conversation_type or "general").lower().replace(" ", "-")

        now = datetime.utcnow()
        module_id = f"{provider_slug}-{conv_slug}-{now.strftime('%Y%m%d%H%M%S')}"
        created_at = now.isoformat()

        module = TTLModule(
            module_id=module_id,
            creator=creator,
            llm_provider=llm_provider,
            model_name=model_name,
            platform=platform,
            conversation_type=conversation_type,
            tags=tags,
            created_at=created_at,
            content=content,
        )

        print(f"✅ TTL module created: {module_id}")
        paths = self.storage.save_module(module)

        return {
            "module_id": module_id,
            "paths": paths,
        }

    def export_module(self, module_id: str, formats: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Export an existing module to one or more formats.
        """
        if formats is None:
            formats = ["markdown"]

        module = self.storage.load_module(module_id)
        if not module:
            raise ValueError(f"Module {module_id} not found")

        exports: Dict[str, str] = {}
        fmts_normalized = [f.lower() for f in formats]

        if "markdown" in fmts_normalized or "md" in fmts_normalized:
            exports["markdown"] = self.export.export_markdown(module)

        if "html" in fmts_normalized:
            exports["html"] = self.export.export_html(module)

        return exports


# ============================================================================
# DEMO + INTERACTIVE CAPTURE
# ============================================================================

def main_demo() -> None:
    """
    Example usage of TTL SDK.
    Creates a sample module and exports it.
    """
    print("=" * 70)
    print("TTL SDK - Truth, Trust, Liberation (Universal LLM Capture)")
    print("=" * 70)
    print()

    sdk = TTLSDK()

    sample_content = "Sample AI conversation content here..."

    result = sdk.create_module(
        creator="demo-user",
        content=sample_content,
        llm_provider="openai",
        model_name="gpt-4.1",
        platform="api",
        conversation_type="coding",
        tags=["python", "ai", "demo"],
    )

    exports = sdk.export_module(
        result["module_id"],
        formats=["markdown", "html"],
    )

    print("\n📤 Exported:")
    for fmt, path in exports.items():
        print(f"   {fmt}: {path}")

    print("\n🚀 TTL SDK is provider-agnostic and ready to plug into any stack.")


def interactive_capture() -> None:
    """
    Interactive conversation capture.
    Paste full threads from ANY LLM platform.
    """
    print("=" * 70)
    print("TTL SDK - Interactive Capture (Any LLM, Any Surface)")
    print("=" * 70)

    creator = input("\nCreator name: ").strip() or "unknown"

    llm_provider = input(
        "LLM Provider (openai/anthropic/google/local/other): "
    ).strip() or "unknown"

    model_name = input(
        "Model name (e.g., gpt-4.1, claude-3.5-sonnet, gemini-1.5-pro): "
    ).strip() or "unknown"

    platform = input(
        "Platform / Surface (chatgpt-web, poe, api, notebook, other): "
    ).strip() or "unknown"

    conv_type = input(
        "Conversation type (coding/research/business/general/other): "
    ).strip() or "general"

    print("\nPaste your conversation content.")
    print("When done, type 'END' on a new line and press Enter.")
    print("-" * 70)

    lines: List[str] = []
    while True:
        try:
            line = input()
        except KeyboardInterrupt:
            print("\n\⚠️  Capture cancelled")
            return

        if line.strip().upper() == "END":
            break
        lines.append(line)

    content = "\n".join(lines)

    if not content.strip():
        print("❌ No content entered!")
        return

    sdk = TTLSDK()
    result = sdk.create_module(
        creator=creator,
        content=content,
        llm_provider=llm_provider,
        model_name=model_name,
        platform=platform,
        conversation_type=conv_type,
    )

    exports = sdk.export_module(result["module_id"], formats=["markdown", "html"])

    print(f"\n✅ Module created: {result['module_id']}")
    print("\n📤 Exported to:")
    for fmt, path in exports.items():
        print(f"   {fmt}: {path}")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("\nTTL SDK - Choose mode:")
    print("1. Demo (create sample module)")
    print("2. Capture conversation (paste full chat)")

    choice = input("\nSelect (1 or 2): ").strip()

    if choice == "2":
        interactive_capture()
    else:
        main_demo()
