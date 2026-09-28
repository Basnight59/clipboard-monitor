#!/usr/bin/env python3
"""
TTL Clipboard Monitor
Automatically captures AI conversations when you copy them

Usage: python ttl_clipboard_monitor.py
Keep it running in the background while you use Claude/ChatGPT
"""

import pyperclip
import time
import re
from datetime import datetime
from ttl_sdk import TTLSDK

class TTLClipboardMonitor:
    """Monitor clipboard for AI conversations and auto-capture."""
    
    def __init__(self):
        self.sdk = TTLSDK()
        self.last_clipboard = ""
        self.last_capture_time = None
        self.capture_cooldown = 5  # seconds between captures
        
        # Patterns to detect AI conversations
        self.ai_patterns = [
            r'\*\*Human\*\*:',
            r'\*\*Claude\*\*:',
            r'\*\*Assistant\*\*:',
            r'ChatGPT:',
            r'User:.*\n.*Assistant:',
            r'Q:.*\n.*A:',
        ]
        
        print("🎯 TTL Clipboard Monitor Started")
        print("=" * 60)
        print("Watching clipboard for AI conversations...")
        print("Copy any Claude/ChatGPT conversation to auto-capture")
        print("Press Ctrl+C to stop")
        print("=" * 60)
    
    def is_ai_conversation(self, text: str) -> bool:
        """Check if text looks like an AI conversation."""
        if len(text) < 50:  # Too short to be a conversation
            return False
        
        # Check for AI conversation patterns
        for pattern in self.ai_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def detect_platform(self, text: str) -> str:
        """Detect which AI platform from content."""
        text_lower = text.lower()
        
        if 'claude' in text_lower or '**claude**:' in text_lower:
            return 'claude'
        elif 'chatgpt' in text_lower or 'openai' in text_lower:
            return 'chatgpt'
        elif 'gemini' in text_lower or 'bard' in text_lower:
            return 'gemini'
        elif 'perplexity' in text_lower:
            return 'perplexity'
        
        return 'unknown'
    
    def detect_type(self, text: str) -> str:
        """Detect conversation type from content."""
        text_lower = text.lower()
        
        # Count keywords
        coding_keywords = ['python', 'javascript', 'code', 'function', 'def ', 'class ', 'import ', 'const ', 'let ']
        research_keywords = ['research', 'study', 'analysis', 'findings', 'evidence', 'data']
        business_keywords = ['business', 'market', 'strategy', 'revenue', 'customer', 'sales']
        creative_keywords = ['story', 'poem', 'creative', 'narrative', 'character', 'plot']
        
        counts = {
            'coding': sum(1 for kw in coding_keywords if kw in text_lower),
            'research': sum(1 for kw in research_keywords if kw in text_lower),
            'business': sum(1 for kw in business_keywords if kw in text_lower),
            'creative': sum(1 for kw in creative_keywords if kw in text_lower)
        }
        
        if max(counts.values()) > 0:
            return max(counts, key=counts.get)
        
        return 'general'
    
    def capture_conversation(self, content: str):
        """Capture conversation to TTL SDK."""
        try:
            platform = self.detect_platform(content)
            conv_type = self.detect_type(content)
            
            # Auto-generate creator name from system
            import getpass
            creator = getpass.getuser()
            
            result = self.sdk.create_module(
                creator=creator,
                content=content,
                platform=platform,
                conversation_type=conv_type,
                tags=['auto-captured', 'clipboard']
            )
            
            # Auto-export
            exports = self.sdk.export_module(
                result['module_id'],
                formats=['markdown', 'html']
            )
            
            print(f"\n✅ AUTO-CAPTURED: {result['module_id']}")
            print(f"   Platform: {platform}")
            print(f"   Type: {conv_type}")
            print(f"   Size: {len(content)} chars")
            print(f"   📂 HTML: {exports['html']}")
            print(f"   📂 MD: {exports['markdown']}")
            print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Capture error: {e}")
    
    def run(self):
        """Main monitoring loop."""
        try:
            while True:
                current = pyperclip.paste()
                
                # Check if clipboard changed
                if current != self.last_clipboard and current.strip():
                    
                    # Check cooldown period
                    if self.last_capture_time:
                        time_since_last = (datetime.now() - self.last_capture_time).total_seconds()
                        if time_since_last < self.capture_cooldown:
                            self.last_clipboard = current
                            time.sleep(1)
                            continue
                    
                    # Check if it's an AI conversation
                    if self.is_ai_conversation(current):
                        print(f"\n🎯 AI conversation detected! ({len(current)} chars)")
                        self.capture_conversation(current)
                        self.last_capture_time = datetime.now()
                    
                    self.last_clipboard = current
                
                time.sleep(1)  # Check every second
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Clipboard monitor stopped")
            print(f"Total monitoring time: Running until stopped")


def main():
    """Start the clipboard monitor."""
    # Check if pyperclip is installed
    try:
        import pyperclip
    except ImportError:
        print("❌ pyperclip not installed!")
        print("Install with: pip install pyperclip")
        return
    
    monitor = TTLClipboardMonitor()
    monitor.run()


if __name__ == "__main__":
    main()