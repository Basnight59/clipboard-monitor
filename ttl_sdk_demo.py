# ttl_sdk_demo.py

from datetime import datetime
import os
import json

# 1. TTL Metadata Class
class TTLMetadata:
    def __init__(self, module_id, creator, date, license_type, consent_policy, tags, spiritual_context="universal"):
        self.module_id = module_id
        self.creator = creator
        self.date = date
        self.license_type = license_type
        self.consent_policy = consent_policy
        self.tags = tags
        self.spiritual_context = spiritual_context
        self.created_at = datetime.utcnow().isoformat()

    def as_dict(self):
        return vars(self)

# 2. Full Session Content (replace ... with your actual session)
FULL_SESSION = """
USER: software development kits
ASSISTANT: Software Development Kits (SDKs) are collections of software tools, libraries, documentation, and code samples that help developers create applications for specific platforms, devices, or ecosystems...

USER: okay, thank you understood, can you show me a basic example
ASSISTANT: Absolutely. Here’s a basic Python SDK structure for a fictional...

USER: Lets say I am working on code in a siloed session in ChatGpt, developing an app, can you I guess make it sdk
ASSISTANT: Yes. You can structure your session’s logic, helper functions, and reusable code as a mini-SDK...

... (Add all subsequent messages in order, up to your latest message) ...

USER: code the demo fully, i will not be able to rest until it works proof of concept
ASSISTANT: **Respect. That’s the right mentality.** Let’s deliver an actual, end-to-end, running “walking skeleton” for the TTL SDK concept...
"""

# 3. Knowledge Module (dict)
knowledge_module = {
    "metadata": TTLMetadata(
        module_id="chat-session-20250723",
        creator="Kenneth Abdul-Hakim Basnight",
        date="2025-07-23",
        license_type="Liberation License",
        consent_policy={"required_token": True, "revocable": True},
        tags=["sdk", "ttl", "brainstorm", "proof-of-concept"],
        spiritual_context="universal"
    ).as_dict(),
    "content": FULL_SESSION
}

# 4. Invocation Function (Consent & Audit)
def invoke_knowledge(module, invoker_id, consent_token):
    # Minimal consent check
    if not consent_token or not consent_token.startswith("sacred-token"):
        raise PermissionError("Consent validation failed.")
    # Audit record (print to console for now)
    audit_record = {
        "module_id": module["metadata"]["module_id"],
        "invoker_id": invoker_id,
        "timestamp": datetime.utcnow().isoformat(),
        "consent": "ok",
        "spiritual_context": module["metadata"]["spiritual_context"]
    }
    print("\n[AUDIT RECORD]", json.dumps(audit_record, indent=2))
    print(f"\n--- MODULE CONTENT PREVIEW ---\n{module['content'][:500]}...\n")
    return module["content"]

# 5. Save Module (Local Files)
def save_module_to_files(module, dir_path="./ttl_modules"):
    os.makedirs(dir_path, exist_ok=True)
    meta_path = os.path.join(dir_path, f"{module['metadata']['module_id']}.json")
    txt_path = os.path.join(dir_path, f"{module['metadata']['module_id']}.txt")
    with open(meta_path, "w") as meta:
        json.dump(module["metadata"], meta, indent=2)
    with open(txt_path, "w") as txt:
        txt.write(module["content"])
    print(f"\n[SAVED] Metadata: {meta_path}\n[SAVED] Content: {txt_path}")

# === RUNNING THE DEMO ===
if __name__ == "__main__":
    print("\n=== TTL SDK DEMO: WALKING SKELETON ===\n")
    # Try invocation with a valid token
    try:
        invoke_knowledge(
            knowledge_module,
            invoker_id="sphinx-devops",
            consent_token="sacred-token-20250723"
        )
    except PermissionError as e:
        print("ERROR:", e)

    # Save to local files (JSON + TXT)
    save_module_to_files(knowledge_module)
    print("\nDemo complete! Check your ./ttl_modules folder for output.\n")
