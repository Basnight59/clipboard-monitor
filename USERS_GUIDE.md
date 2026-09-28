# TTL Clipboard Monitor - Users Guide

Complete guide to capturing, managing, and exporting AI conversations using the TTL Clipboard Monitor system.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Running the Monitor](#running-the-monitor)
3. [Capturing Conversations](#capturing-conversations)
4. [Managing Captured Conversations](#managing-captured-conversations)
5. [Exporting Conversations](#exporting-conversations)
6. [Advanced Features](#advanced-features)
7. [Tips & Best Practices](#tips--best-practices)
8. [FAQ](#faq)

---

## Getting Started

### Prerequisites

Before you start, ensure you have:
- **Python 3.7+** installed
- **pyperclip** library installed (`pip install pyperclip`)
- Write access to the project directory
- The ability to copy text from your clipboard

### First-Time Setup

1. **Open Command Prompt / PowerShell**
   - On Windows: Press `Win + R`, type `cmd`, press Enter
   - On macOS: Open Terminal
   - On Linux: Open your terminal application

2. **Navigate to the project folder**
   ```bash
   cd "C:\Users\[YourUsername]\Clipboard Monitor"
   ```
   Replace `[YourUsername]` with your actual Windows username.

3. **Verify Python Installation**
   ```bash
   python --version
   ```
   Should show Python 3.7 or higher.

4. **Install Dependencies**
   ```bash
   pip install pyperclip
   ```

5. **Test the Setup**
   ```bash
   python clipboard.py
   ```
   You should see the prompt asking for metadata.

---

## Running the Monitor

### Option 1: Interactive Mode (Manual Capture)

Best for: When you want to review and annotate conversations before saving.

```bash
python clipboard.py
```

**What Happens:**
1. The script waits for new content in your clipboard
2. When you copy text (200+ characters), it detects it
3. It prompts you for metadata:
   - Creator name (your name/handle)
   - LLM provider (openai, anthropic, google, etc.)
   - Model name (gpt-4, claude-3.5-sonnet, etc.)
   - Platform (chatgpt-web, cursor, api, etc.)
   - Conversation type (coding, research, business, creative, general)
   - Tags (comma-separated, optional)
4. The conversation is saved with metadata and timestamp

**Example Session:**
```
🎯 TTL Clipboard Monitor

Watching clipboard for AI conversations...
Copy any Claude/ChatGPT conversation to auto-capture
Press Ctrl+C to stop

=== TTL Metadata ===
Creator (your name / handle) [default: unknown]: alice_engineer
LLM Provider (openai/anthropic/google/local/other) [default: unknown]: anthropic
Model name (e.g., gpt-4.1, claude-3.5-sonnet, gemini-1.5-pro) [default: unknown]: claude-3.5-sonnet
Platform / Surface (chatgpt-web, poe, cursor, api, notebook, other) [default: unknown]: cursor
Conversation Type (coding/research/business/creative/general) [default: general]: coding
Tags (comma-separated, optional) [default: none]: python,debugging,optimization

✓ Saved to ttl_data/modules/...
```

### Option 2: Daemon Mode (Automatic Capture)

Best for: Hands-off operation while you work. Captures automatically with minimal prompts.

```bash
python ttl_clipboard_monitor.py
```

**What Happens:**
1. Runs in the background continuously
2. Watches your clipboard for AI conversation patterns
3. Automatically detects:
   - Platform (Claude, ChatGPT, Gemini, etc.)
   - Conversation type (coding, research, etc.)
   - Uses your Windows username as creator
4. Captures conversations without interrupting your work
5. Runs until you press `Ctrl+C`

**Benefits:**
- No interruptions
- Fast capture
- Automatic platform & type detection
- Better for continuous use

**Example Setup (Windows):**
1. Open Command Prompt
2. Navigate to your project folder
3. Run `python ttl_clipboard_monitor.py`
4. Leave it running in the background
5. Copy conversations as usual - they'll be captured automatically

---

## Capturing Conversations

### Step-by-Step Capture Process

#### Step 1: Copy a Conversation

From any LLM platform (ChatGPT, Claude, Gemini, etc.):
1. Select the conversation text you want to save
2. Copy it to clipboard (Ctrl+C or Cmd+C)
3. The conversation should be at least 200 characters (roughly 3-4 exchange turns)

**What to Copy:**
- Full Q&A exchanges
- Code snippets with explanations
- Research discussions
- Creative writing
- Anything you want to preserve

**What NOT to Copy:**
- Single words or very short responses
- Private tokens or API keys (use care decisions for sensitive content)
- System prompts you don't want saved

#### Step 2: Provide Metadata

When using interactive mode (`clipboard.py`), you'll be prompted:

**Creator Name** (Your name/handle)
```
Creator (your name / handle) [default: unknown]: alice_engineer
```
Use something recognizable. This helps when reviewing captures later.

**LLM Provider** (Which AI service)
```
LLM Provider (openai/anthropic/google/local/other) [default: unknown]: anthropic
```
Options:
- `openai` - ChatGPT, GPT-4
- `anthropic` - Claude
- `google` - Gemini, Bard
- `local` - Local LLM running on your machine
- `other` - Unknown or mixed sources

**Model Name** (Specific AI model)
```
Model name (e.g., gpt-4.1, claude-3.5-sonnet, gemini-1.5-pro) [default: unknown]: claude-3.5-sonnet
```
Be as specific as possible. Visit the AI platform to find the exact model name.

**Platform** (Where you accessed it)
```
Platform / Surface (chatgpt-web, poe, cursor, api, notebook, other) [default: unknown]: cursor
```
Options:
- `chatgpt-web` - OpenAI web interface
- `cursor` - Cursor IDE
- `poe` - Poe platform
- `api` - Programmatic API call
- `notebook` - Jupyter or similar
- `other` - Custom integration

**Conversation Type** (What kind of content)
```
Conversation Type (coding/research/business/creative/general) [default: general]: coding
```
- `coding` - Programming, debugging, code review
- `research` - Data analysis, academic discussion
- `business` - Strategy, planning, market analysis
- `creative` - Writing, storytelling, brainstorming
- `general` - Mixed or unclear

**Tags** (Optional keywords for organization)
```
Tags (comma-separated, optional) [default: none]: python,debugging,async
```
Add searchable keywords:
- Technology used: `python`, `javascript`, `rust`
- Topic: `debugging`, `optimization`, `refactoring`
- Domain: `web`, `mobile`, `data-science`
- Custom: Any relevant term

#### Step 3: Confirmation

The script confirms the save:
```
✓ Saved to: ttl_data/modules/2025-12-09/anthropic-coding-20251209084450_meta.json
✓ Content saved to: ttl_data/modules/2025-12-09/anthropic-coding-20251209084450_content.txt
```

The timestamp (like `20251209084450`) ensures all captures are unique.

### Capture Tips

**For Maximum Utility:**
1. Include the full context (both question and answer)
2. Use specific, searchable tags
3. Capture before the window closes
4. Note any special context in tags

**For Finding Later:**
- Use consistent creator names
- Be specific with platform (cursor vs api vs web)
- Add 3-5 descriptive tags
- Include technology/language names in tags

---

## Managing Captured Conversations

### Where Conversations Are Stored

```
ttl_data/
├── modules/
│   ├── 2025-12-09/          ← Date organized
│   │   ├── anthropic-coding-20251209084450_meta.json
│   │   ├── anthropic-coding-20251209084450_content.txt
│   │   ├── openai-research-20251209175616_meta.json
│   │   └── openai-research-20251209175616_content.txt
│   ├── 2025-12-10/
│   └── ... (more dates)
└── exports/
    ├── anthropic-coding-20251209084450.md
    └── anthropic-coding-20251209084450.html
```

### File Naming

Each captured conversation creates two files:

1. **Metadata File** (`_meta.json`)
   - Contains all tags, creator, model, platform info
   - Lightweight, human-readable JSON
   - Example: `anthropic-coding-20251209084450_meta.json`

2. **Content File** (`_content.txt`)
   - The full conversation text
   - Plain text format, preserves formatting
   - Example: `anthropic-coding-20251209084450_content.txt`

### Viewing Captured Conversations

#### View as Text File
1. Navigate to `ttl_data/modules/[DATE]/`
2. Open `_content.txt` file with any text editor
3. View the full conversation

#### View Metadata
1. Open `_meta.json` file with text editor or VS Code
2. See all tags, creator, model, platform information
3. Check the exact timestamp

#### List All Captures
Open file explorer/Finder:
```
Windows: C:\Users\[YourName]\Clipboard Monitor\ttl_data\modules\
Mac: ~/Clipboard Monitor/ttl_data/modules/
Linux: ~/Clipboard Monitor/ttl_data/modules/
```

Browse by date folder to find conversations from specific dates.

### Organizing Conversations

#### Using Tags for Organization
Tags are the best way to organize. When capturing, use consistent tag conventions:

**Project-based:**
`myproject, feature-auth, sprint-2`

**Technology-based:**
`python, fastapi, async, database`

**Purpose-based:**
`debug, optimize, refactor, learning`

#### Finding Conversations
Since files are named with provider, type, and timestamp:
- Look in date folders for conversations from specific dates
- Check metadata files (.json) to find specific tags
- Search for model names: `claude`, `gpt-4`, `gemini`

#### Batch Operations on Named Files
Using command line (advanced):
```bash
# Find all coding conversations from Anthropic
dir ttl_data\modules\* /S | find "anthropic-coding"

# Find all conversations with specific tag in metadata
# (Open the .json files to view tags)
```

---

## Exporting Conversations

### Convert to Markdown

Markdown is ideal for sharing, documentation, and readability.

#### Method 1: Using the Conversion Script

Edit `session_to_markdown.py`:
```python
module_id = "anthropic-coding-20251209084450"  # Change this to your module ID
```

Then run:
```bash
python session_to_markdown.py
```

The markdown file will be saved to `ttl_data/exports/` and `ttl_modules/`

#### Method 2: Manual Conversion

1. Open the `_content.txt` file
2. Copy the content
3. Paste into a `.md` file with headers:
   ```markdown
   # Conversation: [Topic]
   
   **Creator:** Your Name
   **Date:** 2025-12-09
   **Model:** claude-3.5-sonnet
   **Provider:** Anthropic
   
   ---
   
   [Paste conversation content here]
   ```
4. Save as `.md` file

### Convert to HTML

For web sharing and formatting:

#### Using the SDK
```python
from ttl_sdk import TTLSDK

sdk = TTLSDK()
sdk.export_html("anthropic-coding-20251209084450")
```

#### Manual HTML Creation

Save as `.html` file:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Conversation Export</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; }
        .meta { background: #f0f0f0; padding: 10px; border-radius: 5px; }
        .content { white-space: pre-wrap; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="meta">
        <h2>Conversation Export</h2>
        <p><strong>Creator:</strong> Your Name</p>
        <p><strong>Date:</strong> 2025-12-09</p>
        <p><strong>Model:</strong> claude-3.5-sonnet</p>
    </div>
    <div class="content">
        [Paste conversation content here]
    </div>
</body>
</html>
```

### Viewing Exports

Exports are saved in:
- **Markdown**: `ttl_data/exports/[module_id].md`
- **HTML**: `ttl_data/exports/[module_id].html`

Open with:
- **Markdown**: Any text editor or Markdown viewer
- **HTML**: Any web browser

---

## Advanced Features

### Care Decision Integration

For sensitive conversations (private content, special handling required):

```bash
python ttl_care_integrated.py
```

**Files involved:**
- `care_decision_approved.json` - Conversations approved for storage
- `care_decision_rejected.json` - Conversations to exclude
- `care_decision_review.json` - Conversations pending review

**Use Cases:**
- Medical or personal information
- Proprietary business secrets
- Sensitive research
- Private communications

### Reparatory Scoring

Score conversations for their educational or reparatory value:

```bash
python ttl_reparatory_score.py
```

Assigns scores based on:
- Learning value
- Technical depth
- Innovation
- Reusability

### Using the SDK Directly

For custom workflows, use the TTL SDK:

```python
from ttl_sdk import TTLSDK

# Initialize
sdk = TTLSDK()

# Capture conversation
sdk.capture(
    creator="alice_engineer",
    llm_provider="anthropic",
    model_name="claude-3.5-sonnet",
    platform="cursor",
    conversation_type="coding",
    tags=["python", "fastapi", "optimization"],
    content="[Full conversation text]"
)

# Export to markdown
sdk.export_markdown("anthropic-coding-[timestamp]")

# List all modules
all_modules = sdk.list_modules()
for module in all_modules:
    print(f"{module.module_id}: {module.tags}")

# Load specific module
module = sdk.load_module("anthropic-coding-[timestamp]")
print(f"By {module.creator}: {module.tags}")
```

### SDK Demo

See working examples:
```bash
python ttl_sdk_demo.py
```

This demonstrates:
- Capturing conversations
- Loading modules
- Exporting formats
- Working with metadata

---

## Tips & Best Practices

### Capturing Best Practices

**🎯 Be Specific with Metadata**
- Use your real name or consistent handle
- Choose the most specific platform option (not "other")
- List 3-5 relevant tags
- Be accurate with model names (check the AI platform for exact version)

**📌 Tag Conventions**
- Keep tags lowercase and hyphenated: `web-dev` not `Web Development`
- Use technology names: `python`, `javascript`, `rust`
- Add topic tags: `debugging`, `optimization`, `architecture`
- Include domain: `backend`, `frontend`, `devops`

**💾 Regular Capture**
- Capture conversations regularly - don't wait until you forget
- Use daemon mode if you chat with AI daily
- Review captures periodically to add missing tags

**🔍 For Easy Finding Later**
- Creator name is consistent (same name each time)
- Tags are searchable (open .json files to find by tag)
- Dates are organized in folders (look by date when you remember roughly when)
- Model names in filenames (grep for "gpt" vs "claude")

### Managing Your Library

**Monthly Maintenance:**
1. Review captures from the previous month
2. Add any missing tags by editing .json metadata files
3. Archive especially valuable conversations by exporting to Markdown
4. Clean up any test captures

**Organization Strategy:**
- Use date folders naturally (auto-created)
- Rely on tags for quick finding
- Export Markdown for important conversations to a separate "archives" folder
- Keep .json files readable for manual searching

**Backup:**
1. Regular backups of `ttl_data/` directory
2. Export valuable conversations to version control (Git)
3. Consider cloud storage for exports

### Performance Tips

**Polling Interval:**
The daemon checks your clipboard every 1-5 seconds. This is a good default.
- Slower polling (5s) = less CPU usage
- Faster polling (1s) = quicker capture

Edit in `ttl_clipboard_monitor.py` if needed:
```python
self.capture_cooldown = 5  # seconds between captures
```

**Minimum Size:**
Conversations must be at least 50 characters (daemon) or 200 characters (interactive) to capture.
This prevents accidental captures of small text.

---

## FAQ

### Q: Can I edit a captured conversation after saving?

**A:** Yes. The content is in `_content.txt` files which are plain text:
1. Navigate to `ttl_data/modules/[DATE]/[module]_content.txt`
2. Edit with any text editor
3. Save
4. If you update metadata, edit the corresponding `_meta.json` file

### Q: How do I search my captured conversations?

**A:** Multiple ways:
1. **By Date**: Look in `ttl_data/modules/YYYY-MM-DD/`
2. **By Tags**: Open `.json` files and search for tag keywords
3. **By Platform**: Filenames start with provider (`anthropic`, `openai`, `google`)
4. **By Type**: Filenames include type (`coding`, `research`, `business`)
5. **Full text search**: Use your OS file search or command line `grep`

### Q: Can I delete a captured conversation?

**A:** Yes. Both files must be deleted:
1. Delete `_meta.json` file
2. Delete `_content.txt` file

**Warning**: Deletion is permanent. Export to Markdown first if you want to keep it.

### Q: How much disk space do captures use?

**A:** Very little. A typical conversation:
- Content file: 5-50 KB
- Metadata file: <1 KB
- Total: ~50 KB per conversation

1000 conversations ≈ 50 MB (very manageable)

### Q: Can I share captured conversations?

**A:** Yes:
1. Export to Markdown for sharing
2. Share `.md` files freely
3. For `.json` files, remember they contain all metadata (tags, creator, etc.)
4. Use care decisions for sensitive content before sharing

### Q: What if the monitor misses a conversation?

**A:** Try these fixes:
1. **Ensure minimum size**: At least 50 chars (daemon) or 200 chars (interactive)
2. **Check clipboard**: Paste to verify it's there
3. **Wait between copies**: Don't copy multiple things rapidly
4. **Use interactive mode**: `python clipboard.py` for more control
5. **Check patterns**: Daemon looks for AI conversation keywords (User:, Assistant:, Claude:, etc.)

### Q: Can I use both interactive and daemon mode?

**A:** Not simultaneously on the same machine (they both monitor clipboard). Use:
- **Interactive** when you want to review and annotate
- **Daemon** when you want background capture
- Switch between them as needed

### Q: How do I change the polling interval?

**A:** Edit `clipboard.py`:
```python
POLL_INTERVAL = 1.0  # Change to 0.5, 2.0, 5.0, etc.
```

Lower = faster detection but more CPU usage
Higher = slower detection but less CPU usage

### Q: Can I use this with local LLMs?

**A:** Yes:
- Set `llm_provider` to `local`
- Set `model_name` to your model name (e.g., `llama-2-7b`)
- Set `platform` to how you access it (e.g., `ollama`, `llamacpp`, `api`)
- Capture as normal

### Q: Is my data secure?

**A:** Yes:
- All conversations stored locally in `ttl_data/`
- No data sent to external servers by default
- You control all files completely
- Use `.gitignore` to exclude from version control if needed

Add to `.gitignore` if using Git:
```
ttl_data/
```

### Q: How do I backup my conversations?

**A:** Simple folder copy:
1. Copy entire `ttl_data/` folder to external drive
2. Or compress it: `zip -r ttl_data.zip ttl_data/`
3. Or use your OS backup tools

For version control (Git):
```bash
# First, keep ttl_data out of version control with .gitignore
echo "ttl_data/" >> .gitignore

# Then version control exports separately:
git add ttl_data/exports/  # Optional: track exports
git commit -m "Add conversation exports"
```

### Q: Can I import conversations from other systems?

**A:** Yes, manually:
1. Place conversation text in `_content.txt` file
2. Create corresponding `_meta.json` with metadata
3. Place both in `ttl_data/modules/[DATE]/[filename]`
4. Follow naming convention: `{provider}-{type}-{timestamp}_{filetype}`

### Q: What Python version do I need?

**A:** Python 3.7 or higher:
```bash
python --version
```

If you have Python 2, install Python 3:
- Download from python.org
- Run installer
- Check "Add Python to PATH"

### Q: How do I enable daemon mode to start automatically on boot?

**A:** 

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. New Basic Task → Name it "TTL Clipboard Monitor"
3. Trigger: At log on
4. Action: Start program: `python`
5. Arguments: Full path to `ttl_clipboard_monitor.py`

**macOS (LaunchAgent):**
Create `~/Library/LaunchAgents/com.ttl.monitor.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ttl.monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/ttl_clipboard_monitor.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Then load it:
```bash
launchctl load ~/Library/LaunchAgents/com.ttl.monitor.plist
```

**Linux (crontab):**
```bash
crontab -e
```

Add:
```
@reboot /usr/bin/python3 /path/to/ttl_clipboard_monitor.py &
```

---

## Quick Reference

### Common Commands

```bash
# Interactive clipboard monitor
python clipboard.py

# Daemon (automatic) monitor
python ttl_clipboard_monitor.py

# Convert session to markdown
python session_to_markdown.py

# View SDK examples
python ttl_sdk_demo.py

# Run installer generator
python simple_installer.py
```

### File Locations

```
Captured conversations:  ttl_data/modules/[DATE]/
Exports:                 ttl_data/exports/
Metadata (JSON):         [module-name]_meta.json
Content (Text):          [module-name]_content.txt
Exports (Markdown):      [module-name].md
Exports (HTML):          [module-name].html
```

### Metadata Fields

- `creator`: Your name/handle
- `llm_provider`: openai / anthropic / google / local / other
- `model_name`: Specific model (e.g., claude-3.5-sonnet)
- `platform`: How you accessed it (chatgpt-web, cursor, api, etc.)
- `conversation_type`: coding / research / business / creative / general
- `tags`: Comma-separated keywords

---

**Version:** 1.0  
**Last Updated:** February 2026  
**For Issues:** Review README.md or run `ttl_sdk_demo.py` for examples
