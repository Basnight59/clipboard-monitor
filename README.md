# TTL Clipboard Monitor

**TTL** = Truth, Trust, Liberation

A universal, provider-agnostic system for capturing, organizing, and exporting AI conversations from any LLM platform (Claude, ChatGPT, Gemini, etc.).

## Overview

The TTL Clipboard Monitor automatically captures conversations you copy from AI chat platforms and stores them with rich metadata, making them searchable, exportable, and easy to organize.

### Key Features

- **Universal Capture**: Works with conversations from OpenAI, Anthropic, Google, Perplexity, and any LLM platform
- **Automatic Detection**: Identifies the platform and content type of conversations
- **Rich Metadata**: Tracks creator, LLM provider, model name, conversation type, tags, and timestamps
- **Smart Storage**: Organizes modules by date in a structured file system
- **Multiple Exports**: Export conversations as Markdown or HTML
- **Flexible Tagging**: Add custom tags to organize conversations by topic
- **Background Monitoring**: Optional daemon mode to capture conversations as you work

## Project Structure

```
clipboard-monitor/
├── clipboard.py                 # Main universal capture script
├── ttl_clipboard_monitor.py    # Background monitoring daemon
├── ttl_sdk.py                  # Core SDK (storage, export, metadata)
├── session_to_markdown.py      # Convert sessions to markdown
├── simple_installer.py         # Installation helper
├── ttl_care_integrated.py      # Care decision integration
├── ttl_reparatory_score.py     # Reparatory scoring system
├── ttl_sdk_demo.py             # SDK demonstration
├── ttl_sdk_v1.py               # SDK version 1 reference
├── requirements.txt            # Python dependencies
├── examples/                   # Sample care decision outputs
├── ttl_data/                   # Storage directory (local only, git-ignored)
│   ├── modules/                # Captured conversations (sorted by date)
│   │   ├── 2025-12-09/
│   │   ├── 2025-12-10/
│   │   └── ...
│   └── exports/                # Exported markdown and HTML files
└── ttl_modules/                # Alternative module storage (local only, git-ignored)
```

## Installation

### Requirements

- **Python 3.7+**
- **pyperclip**: For clipboard access
- **Operating System**: Windows, macOS, or Linux

### Setup Steps

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure "Add Python to PATH" is checked during installation

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python clipboard.py
   ```

### Optional: Automated Installation

Run the installer generator to create a Windows batch installer:
```bash
python simple_installer.py
```

This creates a `profai-windows-installer/` folder with an `install.bat` script.

## Quick Start

### Manual Capture Mode (Interactive)

1. Copy a conversation from Claude, ChatGPT, or any LLM platform
2. Run the clipboard monitor:
   ```bash
   python clipboard.py
   ```
3. When new text is detected in your clipboard, the script will prompt you:
   - Enter your name (creator)
   - Specify the LLM provider (openai, anthropic, google, etc.)
   - Enter the model name (e.g., gpt-4, claude-3.5-sonnet)
   - Select the platform (chatgpt-web, cursor, api, etc.)
   - Add conversation tags (optional)

4. The conversation is saved automatically with metadata and timestamp

### Automatic Capture Mode (Daemon)

For continuous background monitoring without prompts:
```bash
python ttl_clipboard_monitor.py
```

The daemon automatically:
- Detects AI conversations in your clipboard
- Identifies platforms and content types
- Captures them with minimal user interaction
- Runs indefinitely until you press Ctrl+C

## Understanding the Data Structure

### Module Storage

Conversations are stored in `ttl_data/modules/` organized by date:

```
ttl_data/modules/2025-12-09/
├── anthropic-coding-20251209084450_meta.json
├── anthropic-coding-20251209084450_content.txt
├── openai-research-20251209175616_meta.json
└── openai-research-20251209175616_content.txt
```

**Naming Convention**: `{provider}-{type}-{timestamp}_{file_type}`

### Metadata File Example

```json
{
  "module_id": "anthropic-coding-20251209084450",
  "creator": "john_doe",
  "llm_provider": "anthropic",
  "model_name": "claude-3.5-sonnet",
  "platform": "cursor",
  "conversation_type": "coding",
  "tags": ["python", "debugging", "refactoring"],
  "created_at": "2025-12-09T08:44:50Z",
  "license_type": "personal"
}
```

## Features in Detail

### Conversation Type Detection

The system automatically categorizes conversations as:
- **coding**: Python, JavaScript, code review, functions, classes
- **research**: Studies, analysis, findings, evidence, data
- **business**: Market strategy, customer insights, revenue
- **creative**: Stories, poems, narrative, characters
- **general**: Default for mixed or unclassified content

### Platform Detection

Automatically identifies when conversations are from:
- Claude (Anthropic)
- ChatGPT (OpenAI)
- Gemini / Bard (Google)
- Perplexity
- Custom/unknown platforms

### Export Formats

#### Convert to Markdown
Use `session_to_markdown.py` to convert captured sessions:
```python
module_id = "your-module-name"
# Modify the script with your module ID and run
python session_to_markdown.py
```

#### Exports Location
All exports are saved in `ttl_data/exports/`:
- `.md` files for Markdown format
- `.html` files for HTML format

## Advanced Usage

### Care Decision Integration

Use care decision workflows for sensitive conversations:
```bash
python ttl_care_integrated.py
```

This writes `care_decision_approved.json`, `care_decision_rejected.json`, and `care_decision_review.json` to the project root. Sample outputs are in `examples/`.

### Reparatory Scoring

Score conversations for their reparatory value:
```bash
python ttl_reparatory_score.py
```

### SDK Demo

See the SDK in action:
```bash
python ttl_sdk_demo.py
```

### Using the TTL SDK Directly

```python
from ttl_sdk import TTLSDK

# Initialize the SDK
sdk = TTLSDK()

# Capture a conversation with metadata
sdk.capture(
    creator="john_doe",
    llm_provider="anthropic",
    model_name="claude-3.5-sonnet",
    platform="cursor",
    conversation_type="coding",
    tags=["python", "fastapi"],
    content="[conversation text here]"
)

# Export as markdown
sdk.export_markdown(module_id)

# Export as HTML
sdk.export_html(module_id)

# List all modules
modules = sdk.list_modules()
print(modules)
```

## Keyboard Shortcuts & Controls

- **Ctrl+C**: Stop the clipboard monitor (graceful shutdown)
- **Enter**: Confirm prompts and save conversations
- **Tab**: Auto-complete suggestions (platform and provider names)

## Troubleshooting

### Issue: "No module named 'pyperclip'"
**Solution**: Install pyperclip
```bash
pip install pyperclip
```

### Issue: "Permission denied" when creating directories
**Solution**: Ensure you have write permissions in the project directory. On Windows, run as Administrator if needed.

### Issue: Clipboard monitor not detecting AI conversations
**Solution**: 
- Ensure the text is at least 50 characters long
- Check that the conversation contains AI patterns (User:, Assistant:, Claude:, etc.)
- Try capturing manually with `clipboard.py`

### Issue: Nothing appears when I copy text
**Solution**:
- The monitor has a 1-5 second polling interval - wait a moment after copying
- Verify the text meets the minimum size requirement (200 chars for interactive mode, 50 for daemon)
- Check that your clipboard manager isn't interfering

## Configuration

### Adjust Polling Interval (clipboard.py)
```python
POLL_INTERVAL = 1.0  # seconds between checks
```

### Adjust Minimum Capture Size (clipboard.py)
```python
MIN_CHARS_FOR_CAPTURE = 200  # minimum characters
```

### Adjust Daemon Cooldown (ttl_clipboard_monitor.py)
```python
self.capture_cooldown = 5  # seconds between captures
```

## License & Ethics

- Conversations are stored securely in your local `ttl_data/` directory
- No data is sent to external servers by default
- You retain full ownership of your captured conversations
- Use the care decision integration for sensitive content

## Support & Contribution

For issues, questions, or feature requests, refer to:
- Check the **Users Guide** for detailed usage examples
- Review SDK documentation in `ttl_sdk.py` docstrings
- Run `ttl_sdk_demo.py` to see examples

## Version History

- **v1.0**: Universal clipboard capture with provider detection
- **v2.0**: Daemon mode and automatic detection added
- **v3.0**: Care decision integration and advanced exports

---

**Last Updated**: February 2026
**Maintained By**: TTL Team
