#!/usr/bin/env python3
"""
TTL SDK - Complete Python Implementation
Truth, Trust, Liberation - AI Conversation Management System

Author: Kenneth Abdul-Hakim Basnight
Date: December 2025
License: Liberation License

Production-ready code for AI conversation management
"""

import os
import json
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field

# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

@dataclass
class TTLMetadata:
    """Core metadata structure for TTL knowledge modules."""
    module_id: str
    creator: str
    date: str
    license_type: str = "Liberation License"
    consent_policy: Dict[str, Any] = field(default_factory=lambda: {
        "required_token": True,
        "revocable": True
    })
    tags: List[str] = field(default_factory=list)
    spiritual_context: str = "universal"
    platform: str = "unknown"
    conversation_type: str = "general"
    
    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditRecord:
    """Audit trail record for consent and access tracking."""
    module_id: str
    invoker_id: str
    timestamp: str
    action: str
    consent_status: str
    spiritual_context: str
    
    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# SECURITY VALIDATION
# ============================================================================

class TTLSecurityValidator:
    """Enterprise-grade security validation."""
    
    MAX_CONTENT_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_FILENAME_LENGTH = 200
    RESERVED_NAMES = ['CON', 'PRN', 'AUX', 'NUL']
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for cross-platform security."""
        if not filename or not filename.strip():
            return f"unnamed_{hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:8]}"
        
        safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.")
        filename = ''.join(c if c in safe_chars else '_' for c in filename)
        
        if filename.split('.')[0].upper() in TTLSecurityValidator.RESERVED_NAMES:
            filename = f"ttl_{filename}"
        
        if len(filename) > TTLSecurityValidator.MAX_FILENAME_LENGTH:
            name, ext = os.path.splitext(filename)
            filename = name[:TTLSecurityValidator.MAX_FILENAME_LENGTH - len(ext)] + ext
        
        return filename
    
    @staticmethod
    def validate_path(path: str, base_path: str) -> bool:
        """Validate path doesn't escape base directory."""
        try:
            abs_path = os.path.abspath(os.path.join(base_path, path))
            abs_base = os.path.abspath(base_path)
            return abs_path.startswith(abs_base)
        except Exception:
            return False
    
    @staticmethod
    def validate_content_size(content: str) -> bool:
        """Validate content size within limits."""
        return len(content.encode('utf-8')) <= TTLSecurityValidator.MAX_CONTENT_SIZE


# ============================================================================
# STORAGE MANAGEMENT
# ============================================================================

class TTLStorageManager:
    """Secure file storage with organization."""
    
    def __init__(self, base_path: str = "./ttl_modules"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.dirs = {
            'by_date': self.base_path / 'by-date',
            'by_creator': self.base_path / 'by-creator',
            'by_type': self.base_path / 'by-type',
            'by_platform': self.base_path / 'by-platform'
        }
        
        for dir_path in self.dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def save_module(self, module: Dict[str, Any]) -> Dict[str, str]:
        """Save module with security validation."""
        metadata = module['metadata']
        content = module['content']
        
        if not TTLSecurityValidator.validate_content_size(content):
            raise ValueError("Content exceeds maximum size")
        
        module_id = TTLSecurityValidator.sanitize_filename(metadata['module_id'])
        
        date_obj = datetime.datetime.strptime(metadata['date'], '%Y-%m-%d')
        date_dir = self.dirs['by_date'] / f"{date_obj.year}" / f"{date_obj.month:02d}"
        date_dir.mkdir(parents=True, exist_ok=True)
        
        meta_path = date_dir / f"{module_id}.json"
        content_path = date_dir / f"{module_id}.txt"
        
        with open(meta_path, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        with open(content_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(content)
        
        return {
            'primary': str(meta_path),
            'content': str(content_path)
        }
    
    def load_module(self, module_id: str) -> Optional[Dict[str, Any]]:
        """Load module by ID from storage."""
        for year_dir in self.dirs['by_date'].iterdir():
            if year_dir.is_dir():
                for month_dir in year_dir.iterdir():
                    if month_dir.is_dir():
                        meta_path = month_dir / f"{module_id}.json"
                        content_path = month_dir / f"{module_id}.txt"
                        
                        if meta_path.exists() and content_path.exists():
                            with open(meta_path, 'r', encoding='utf-8', errors='replace') as f:
                                metadata = json.load(f)
                            with open(content_path, 'r', encoding='utf-8', errors='replace') as f:
                                content = f.read()
                            return {'metadata': metadata, 'content': content}
        return None


# ============================================================================
# EXPORT SYSTEM
# ============================================================================

class TTLExportManager:
    """Multi-format export system."""
    
    def __init__(self, output_dir: str = "./ttl_exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_markdown(self, module: Dict[str, Any]) -> str:
        """Export to Markdown format."""
        metadata = module['metadata']
        content = module['content']
        
        markdown = f"""# TTL Module: {metadata['module_id']}

## Metadata
- **Creator:** {metadata['creator']}
- **Date:** {metadata['date']}
- **Platform:** {metadata.get('platform', 'unknown')}
- **Type:** {metadata.get('conversation_type', 'general')}
- **Tags:** {', '.join(metadata.get('tags', []))}

## Conversation

{content}

---
*TTL SDK | Liberation License*
"""
        
        filename = TTLSecurityValidator.sanitize_filename(f"{metadata['module_id']}.md")
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8', errors='replace') as f:
            f.write(markdown)
        
        return str(filepath)
    
    def export_html(self, module: Dict[str, Any]) -> str:
        """Export to HTML format."""
        metadata = module['metadata']
        content = module['content'].replace('\n\n', '</p><p>')
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TTL: {metadata['module_id']}</title>
    <style>
        body {{ font-family: Arial; max-width: 900px; margin: 40px auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; border-radius: 10px; }}
        .metadata {{ background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; }}
        .content {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TTL Module: {metadata['module_id']}</h1>
        <p>Liberation License</p>
    </div>
    <div class="metadata">
        <p><strong>Creator:</strong> {metadata['creator']}</p>
        <p><strong>Date:</strong> {metadata['date']}</p>
        <p><strong>Platform:</strong> {metadata.get('platform', 'unknown')}</p>
    </div>
    <div class="content">
        <h2>Conversation</h2>
        <p>{content}</p>
    </div>
</body>
</html>"""
        
        filename = TTLSecurityValidator.sanitize_filename(f"{metadata['module_id']}.html")
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8', errors='replace') as f:
            f.write(html)
        
        return str(filepath)


# ============================================================================
# MAIN TTL SDK CLASS
# ============================================================================

class TTLSDK:
    """Main TTL SDK interface."""
    
    def __init__(self, base_path: str = "./ttl_data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.storage = TTLStorageManager(str(self.base_path / "modules"))
        self.export = TTLExportManager(str(self.base_path / "exports"))
        
        print(f"✅ TTL SDK initialized: {self.base_path}")
    
    def create_module(self, creator: str, content: str, 
                     platform: str = "unknown",
                     conversation_type: str = "general",
                     tags: List[str] = None) -> Dict[str, Any]:
        """Create new conversation module."""
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        module_id = f"{platform}-{conversation_type}-{timestamp}"
        
        metadata = TTLMetadata(
            module_id=module_id,
            creator=creator,
            date=datetime.datetime.now().strftime('%Y-%m-%d'),
            platform=platform,
            conversation_type=conversation_type,
            tags=tags or []
        )
        
        module = {
            'metadata': metadata.as_dict(),
            'content': content
        }
        
        paths = self.storage.save_module(module)
        
        return {
            'module_id': module_id,
            'paths': paths
        }
    
    def export_module(self, module_id: str, formats: List[str] = None) -> Dict[str, str]:
        """Export module to specified formats."""
        if formats is None:
            formats = ['markdown']
        
        module = self.storage.load_module(module_id)
        if not module:
            raise ValueError(f"Module {module_id} not found")
        
        exports = {}
        
        if 'markdown' in formats or 'md' in formats:
            exports['markdown'] = self.export.export_markdown(module)
        
        if 'html' in formats:
            exports['html'] = self.export.export_html(module)
        
        return exports


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def main():
    """Example usage of TTL SDK."""
    print("=" * 70)
    print("TTL SDK - Truth, Trust, Liberation")
    print("=" * 70)
    print()
    
    sdk = TTLSDK()
    
    result = sdk.create_module(
        creator="kenneth-basnight",
        content="Sample AI conversation content here...",
        platform="claude",
        conversation_type="coding",
        tags=["python", "ai", "conversation"]
    )
    
    print(f"✅ Module created: {result['module_id']}")
    
    exports = sdk.export_module(
        result['module_id'],
        formats=['markdown', 'html']
    )
    
    print("\n📤 Exported:")
    for fmt, path in exports.items():
        print(f"   {fmt}: {path}")
    
    print("\n🚀 TTL SDK Ready for Production!")


def interactive_capture():
    """Interactive conversation capture."""
    print("=" * 70)
    print("TTL SDK - Interactive Capture")
    print("=" * 70)
    
    creator = input("\nCreator name: ")
    platform = input("Platform (claude/chatgpt/gemini): ") or "claude"
    conv_type = input("Type (coding/business/research): ") or "general"
    
    print("\nPaste your conversation content.")
    print("When done, type 'END' on a new line:")
    print("-" * 70)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        except KeyboardInterrupt:
            print("\n\n⚠️  Capture cancelled")
            return
    
    content = '\n'.join(lines)
    
    if not content.strip():
        print("❌ No content entered!")
        return
    
    sdk = TTLSDK()
    result = sdk.create_module(
        creator=creator,
        content=content,
        platform=platform,
        conversation_type=conv_type
    )
    
    print(f"\n✅ Module created: {result['module_id']}")
    
    exports = sdk.export_module(result['module_id'], formats=['markdown', 'html'])
    
    print("\n📤 Exported to:")
    for fmt, path in exports.items():
        print(f"   {fmt}: {path}")


if __name__ == "__main__":
    print("\nTTL SDK - Choose mode:")
    print("1. Demo")
    print("2. Capture conversation")
    
    choice = input("\nSelect (1 or 2): ")
    
    if choice == "2":
        interactive_capture()
    else:
        main()