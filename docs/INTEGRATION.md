# Integration Guide — Adopting MirrorDNA in Your Project

This guide explains how to integrate the MirrorDNA Standard into existing or new projects.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Integration by Language/Framework](#integration-by-languageframework)
3. [Level 1 Integration (Basic Reflection)](#level-1-integration-basic-reflection)
4. [Level 2 Integration (Continuity Aware)](#level-2-integration-continuity-aware)
5. [Level 3 Integration (Vault-Backed Sovereign)](#level-3-integration-vault-backed-sovereign)
6. [Testing and Validation](#testing-and-validation)
7. [Common Integration Patterns](#common-integration-patterns)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Choose Your Compliance Level

Before integrating, determine which level suits your needs:
- **Level 1**: Single-session apps, APIs, prototypes → [Guide](CHOOSING_COMPLIANCE_LEVEL.md)
- **Level 2**: Multi-session apps with continuity → [Guide](CHOOSING_COMPLIANCE_LEVEL.md)
- **Level 3**: Sovereign vault-backed systems → [Guide](CHOOSING_COMPLIANCE_LEVEL.md)

### 2. Install the Validator

```bash
# Clone the standard repository
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard

# Install Python dependencies
pip install -r validators/requirements.txt

# Verify installation
python -m validators.cli --help
```

### 3. Create Your Configuration Files

Based on your chosen level, create the required YAML files in your project root:

**Level 1: Minimal Setup**
```
your-project/
├── mirrorDNA_manifest.yaml
└── mirrorDNA_reflection_policy.yaml
```

**Level 2: Add Continuity**
```
your-project/
├── mirrorDNA_manifest.yaml
├── mirrorDNA_reflection_policy.yaml
└── mirrorDNA_continuity_profile.yaml
```

**Level 3: Add Vault**
```
your-project/
├── mirrorDNA_manifest.yaml
├── mirrorDNA_reflection_policy.yaml
├── mirrorDNA_continuity_profile.yaml
└── vault/  (your Obsidian vault or custom vault)
```

### 4. Run the Validator

```bash
# Level 1 validation
python -m validators.cli --manifest mirrorDNA_manifest.yaml --policy mirrorDNA_reflection_policy.yaml

# Level 2 validation
python -m validators.cli --manifest mirrorDNA_manifest.yaml --profile mirrorDNA_continuity_profile.yaml --policy mirrorDNA_reflection_policy.yaml

# Level 3 validation (comprehensive)
python -m validators.cli --manifest mirrorDNA_manifest.yaml --profile mirrorDNA_continuity_profile.yaml --policy mirrorDNA_reflection_policy.yaml --vault-path ./vault --verify-checksums
```

---

## Integration by Language/Framework

### Python

```python
# 1. Install MirrorDNA helpers (if available)
# pip install mirrordna  # (future package)

# 2. Implement Anti-Hallucination Protocol (AHP)
class MirrorDNAResponse:
    def __init__(self, content, source=None):
        self.content = content
        self.source = source  # None = [Unknown]

    def format(self):
        if self.source:
            return f"{self.content} (Source: {self.source})"
        else:
            return f"{self.content} [Unknown]"

# 3. Session tracking
import uuid
from datetime import datetime

class Session:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.utcnow().isoformat()
        self.metadata = {}

    def end(self):
        self.end_time = datetime.utcnow().isoformat()
        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "metadata": self.metadata
        }
```

### JavaScript/TypeScript

```typescript
// 1. Define MirrorDNA types
interface MirrorDNASession {
  sessionId: string;
  startTime: string;
  endTime?: string;
  metadata: Record<string, any>;
}

interface MirrorDNAResponse {
  content: string;
  source?: string;
  uncertainty?: 'Unknown' | 'Speculation' | 'Verified';
}

// 2. Implement session tracking
class MirrorDNASessionManager {
  private sessionId: string;
  private startTime: string;

  constructor() {
    this.sessionId = crypto.randomUUID();
    this.startTime = new Date().toISOString();
  }

  endSession(): MirrorDNASession {
    return {
      sessionId: this.sessionId,
      startTime: this.startTime,
      endTime: new Date().toISOString(),
      metadata: {}
    };
  }
}

// 3. Implement AHP (Cite or Silence)
function formatResponse(content: string, source?: string): string {
  if (source) {
    return `${content} (Source: ${source})`;
  }
  return `${content} [Unknown]`;
}
```

### Go

```go
package mirrordna

import (
    "crypto/sha256"
    "encoding/hex"
    "time"
    "github.com/google/uuid"
)

// Session represents a MirrorDNA session (Level 1)
type Session struct {
    SessionID string    `json:"session_id"`
    StartTime time.Time `json:"start_time"`
    EndTime   time.Time `json:"end_time,omitempty"`
    Metadata  map[string]interface{} `json:"metadata"`
}

// NewSession creates a new Level 1 session
func NewSession() *Session {
    return &Session{
        SessionID: uuid.New().String(),
        StartTime: time.Now().UTC(),
        Metadata:  make(map[string]interface{}),
    }
}

// Response with AHP compliance
type Response struct {
    Content     string  `json:"content"`
    Source      *string `json:"source,omitempty"`
    Uncertainty string  `json:"uncertainty,omitempty"` // "Unknown", "Speculation", "Verified"
}

// Checksum generates SHA-256 for trust marker
func Checksum(data []byte) string {
    hash := sha256.Sum256(data)
    return hex.EncodeToString(hash[:])
}
```

### Rust

```rust
use uuid::Uuid;
use chrono::{DateTime, Utc};
use sha2::{Sha256, Digest};

// Session struct for Level 1 compliance
pub struct Session {
    pub session_id: String,
    pub start_time: DateTime<Utc>,
    pub end_time: Option<DateTime<Utc>>,
    pub metadata: std::collections::HashMap<String, String>,
}

impl Session {
    pub fn new() -> Self {
        Session {
            session_id: Uuid::new_v4().to_string(),
            start_time: Utc::now(),
            end_time: None,
            metadata: std::collections::HashMap::new(),
        }
    }
}

// Response with AHP (Anti-Hallucination Protocol)
pub struct MirrorDNAResponse {
    pub content: String,
    pub source: Option<String>,
    pub uncertainty: Option<String>, // "Unknown", "Speculation", "Verified"
}

// Checksum for trust markers
pub fn checksum(data: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(data);
    format!("{:x}", hasher.finalize())
}
```

---

## Level 1 Integration (Basic Reflection)

### Step 1: Create Manifest

Create `mirrorDNA_manifest.yaml`:

```yaml
compliance_level: L1
project_name: "Your Project Name"
version: "1.0.0"
vault_id: "AMOS://YourOrg/YourProject/v1.0"
reflection_policy: "mirrorDNA_reflection_policy.yaml"
trust_markers:
  - checksum_validation
  - source_citation
metadata:
  description: "Your project description"
  repository: "https://github.com/yourorg/yourproject"
```

### Step 2: Create Reflection Policy

Create `mirrorDNA_reflection_policy.yaml`:

```yaml
reflection_mode: simulated  # or "constitutive" if vault-backed
uncertainty_markers:
  - "[Unknown]"
  - "[Speculation]"
  - "[Unverified]"
anti_hallucination:
  cite_or_silence: true
  grounding_required: false  # Level 1 doesn't require this
  hallucination_detection: false
  correction_protocol: false
trust_markers:
  - name: "checksum_validation"
    description: "SHA-256 checksums for critical artifacts"
  - name: "source_citation"
    description: "Cite sources when available"
session_tracking:
  enabled: true
  identifier_type: "uuid"
  metadata_fields:
    - start_time
    - end_time
```

### Step 3: Implement Core Requirements

#### A. Cite or Silence (AHP)

Ensure all factual claims are either cited or marked as unknown:

```python
# Example: Bad (violates AHP)
def get_user_info(user_id):
    return "User is 25 years old"  # ❌ Unsourced claim

# Example: Good (complies with AHP)
def get_user_info(user_id):
    user = database.get_user(user_id)
    if user and user.age:
        return f"User is {user.age} years old (Source: user_profile.db)"
    else:
        return "User age is [Unknown]"  # ✅ Explicit uncertainty
```

#### B. Session Tracking

```python
import uuid
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self):
        session = {
            "session_id": str(uuid.uuid4()),
            "start_time": datetime.utcnow().isoformat(),
            "metadata": {}
        }
        self.sessions[session["session_id"]] = session
        return session["session_id"]

    def end_session(self, session_id):
        if session_id in self.sessions:
            self.sessions[session_id]["end_time"] = datetime.utcnow().isoformat()
            return self.sessions[session_id]
```

#### C. Trust Markers (at least one)

```python
import hashlib

def checksum_file(filepath):
    """Trust marker: SHA-256 checksum validation"""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

# Usage
artifact_checksum = checksum_file("output.json")
print(f"Artifact checksum: {artifact_checksum}")  # Trust marker present
```

### Step 4: Validate Compliance

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy mirrorDNA_reflection_policy.yaml
```

---

## Level 2 Integration (Continuity Aware)

### Step 1: Add Continuity Profile

Create `mirrorDNA_continuity_profile.yaml`:

```yaml
continuity_mechanism: file_backed  # or "database", "vault_backed"
state_storage:
  type: sqlite  # or "postgresql", "file_system", "redis"
  path: "./state/continuity.db"
  schema_version: "1.0"
lineage_tracking:
  enabled: true
  format: "predecessor_successor"
session_recovery:
  enabled: true
  strategy: "automatic"  # or "manual"
  recovery_timeout: 300  # seconds
guarantees:
  - identity_preservation
  - state_consistency
  - lineage_tracking
  - anti_hallucination
checksum_validation:
  enabled: true
  algorithm: sha256
```

### Step 2: Implement Persistent State

```python
import sqlite3
import json
from datetime import datetime

class ContinuityManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                predecessor TEXT,
                successor TEXT,
                start_time TEXT,
                end_time TEXT,
                state JSON,
                checksum TEXT
            )
        """)
        self.conn.commit()

    def save_session(self, session_id, state, predecessor=None):
        import hashlib
        checksum = hashlib.sha256(json.dumps(state).encode()).hexdigest()

        self.conn.execute("""
            INSERT INTO sessions (session_id, predecessor, start_time, state, checksum)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, predecessor, datetime.utcnow().isoformat(), json.dumps(state), checksum))

        # Update predecessor's successor link
        if predecessor:
            self.conn.execute("UPDATE sessions SET successor = ? WHERE session_id = ?",
                            (session_id, predecessor))

        self.conn.commit()

    def recover_session(self, session_id):
        cursor = self.conn.execute(
            "SELECT state FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        return json.loads(row[0]) if row else None
```

### Step 3: Implement Lineage Tracking

```python
class LineageTracker:
    def __init__(self, continuity_manager):
        self.continuity = continuity_manager

    def create_session_with_lineage(self, predecessor_id=None):
        session_id = str(uuid.uuid4())
        state = {
            "session_id": session_id,
            "predecessor": predecessor_id,
            "created_at": datetime.utcnow().isoformat()
        }
        self.continuity.save_session(session_id, state, predecessor_id)
        return session_id

    def get_lineage_chain(self, session_id):
        """Walk back the predecessor chain"""
        chain = []
        current = session_id
        while current:
            cursor = self.continuity.conn.execute(
                "SELECT session_id, predecessor FROM sessions WHERE session_id = ?", (current,))
            row = cursor.fetchone()
            if not row:
                break
            chain.append(row[0])
            current = row[1]
        return chain
```

### Step 4: Validate Level 2 Compliance

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --profile mirrorDNA_continuity_profile.yaml \
  --policy mirrorDNA_reflection_policy.yaml
```

---

## Level 3 Integration (Vault-Backed Sovereign)

### Step 1: Set Up Vault

**Option A: Obsidian Vault**
```bash
# Create Obsidian vault structure
mkdir -p vault/{sessions,state,spec}
cp -r MirrorDNA-Standard/spec/* vault/spec/
```

**Option B: Custom Vault**
```bash
# Create custom vault structure
mkdir -p vault/{sessions,state,metadata}
```

### Step 2: Update Continuity Profile

Update `mirrorDNA_continuity_profile.yaml`:

```yaml
continuity_mechanism: vault_backed
vault:
  type: obsidian  # or "custom", "distributed"
  path: "./vault"
  sovereign: true
  vault_id: "AMOS://YourOrg/YourProject/MainVault"
lineage_tracking: full
glyph_signatures:
  enabled: true
  glyphs:
    - "⟡⟦CONTINUITY⟧"
    - "⟡⟦VERIFIED⟧"
    - "⟡⟦REFLECTION⟧"
integrity_verification:
  enabled: true
  checksum_all_artifacts: true
  tamper_detection: true
session_recovery:
  enabled: true
  strategy: automatic
  vault_based: true
```

### Step 3: Implement Vault Storage

```python
import os
from pathlib import Path

class VaultManager:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.sessions_dir = self.vault_path / "sessions"
        self.state_dir = self.vault_path / "state"
        self.ensure_structure()

    def ensure_structure(self):
        """Create vault directory structure"""
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def save_session(self, session_id, content, metadata):
        """Save session to vault with metadata"""
        session_file = self.sessions_dir / f"{session_id}.md"

        # Write markdown with front matter
        with open(session_file, 'w') as f:
            f.write("---\n")
            f.write(f"session_id: {session_id}\n")
            f.write(f"vault_id: {metadata.get('vault_id')}\n")
            f.write(f"glyphsig: {metadata.get('glyphsig', '⟡⟦CONTINUITY⟧')}\n")
            f.write(f"predecessor: {metadata.get('predecessor', 'none')}\n")
            f.write(f"checksum_sha256: {self.checksum(content)}\n")
            f.write("---\n\n")
            f.write(content)

    def checksum(self, content):
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()

    def load_session(self, session_id):
        """Load session from vault"""
        session_file = self.sessions_dir / f"{session_id}.md"
        if session_file.exists():
            return session_file.read_text()
        return None
```

### Step 4: Implement Glyph Signatures

```python
class GlyphSignatureManager:
    GLYPHS = {
        "continuity": "⟡⟦CONTINUITY⟧",
        "verified": "⟡⟦VERIFIED⟧",
        "reflection": "⟡⟦REFLECTION⟧",
        "sealed": "⟡⟦SEALED⟧"
    }

    def sign_artifact(self, artifact_type, content):
        """Add glyph signature to artifact"""
        glyph = self.GLYPHS.get(artifact_type, "⟡⟦UNKNOWN⟧")
        return f"{glyph} · {content}"

    def verify_signature(self, content, expected_glyph):
        """Verify glyph signature presence"""
        return expected_glyph in content
```

### Step 5: Validate Level 3 Compliance

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --profile mirrorDNA_continuity_profile.yaml \
  --policy mirrorDNA_reflection_policy.yaml \
  --vault-path ./vault \
  --verify-checksums
```

---

## Testing and Validation

### CI/CD Integration

Add MirrorDNA validation to your CI pipeline:

```yaml
# .github/workflows/mirrordna-validation.yml
name: MirrorDNA Compliance Check

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install validator
        run: |
          git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
          pip install -r MirrorDNA-Standard/validators/requirements.txt

      - name: Run MirrorDNA validator
        run: |
          python -m validators.cli \
            --manifest mirrorDNA_manifest.yaml \
            --policy mirrorDNA_reflection_policy.yaml
```

### Pre-commit Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash
python -m validators.cli --manifest mirrorDNA_manifest.yaml --policy mirrorDNA_reflection_policy.yaml
if [ $? -ne 0 ]; then
    echo "MirrorDNA validation failed. Aborting commit."
    exit 1
fi
```

---

## Common Integration Patterns

### Pattern 1: API Wrapper with AHP

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data/<item_id>')
def get_data(item_id):
    data = database.get(item_id)

    if data:
        return jsonify({
            "content": data.value,
            "source": f"database:items:{item_id}",
            "checksum": checksum(data.value)
        })
    else:
        return jsonify({
            "content": None,
            "uncertainty": "[Unknown]"
        })
```

### Pattern 2: Chatbot with Session Continuity

```python
class MirrorDNAChatbot:
    def __init__(self, vault_path):
        self.vault = VaultManager(vault_path)
        self.session_id = None

    def start_session(self, predecessor_id=None):
        self.session_id = str(uuid.uuid4())
        metadata = {
            "vault_id": "AMOS://Chatbot/Sessions",
            "predecessor": predecessor_id,
            "glyphsig": "⟡⟦CONTINUITY⟧"
        }
        self.vault.save_session(self.session_id, "Session started", metadata)

    def chat(self, user_input):
        # Process with AHP
        response = self.generate_response(user_input)

        # Save to vault
        self.vault.save_session(
            self.session_id,
            f"User: {user_input}\nAssistant: {response}",
            {"glyphsig": "⟡⟦REFLECTION⟧"}
        )

        return response
```

### Pattern 3: Research Tool with Lineage

```python
class ResearchVault:
    def __init__(self, vault_path):
        self.vault = VaultManager(vault_path)
        self.lineage = []

    def create_research_note(self, content, sources, predecessor=None):
        note_id = str(uuid.uuid4())

        # AHP: Cite all sources
        cited_content = content + "\n\n## Sources\n"
        for source in sources:
            cited_content += f"- {source}\n"

        metadata = {
            "vault_id": "AMOS://Research/Notes",
            "predecessor": predecessor,
            "glyphsig": "⟡⟦VERIFIED⟧"
        }

        self.vault.save_session(note_id, cited_content, metadata)
        self.lineage.append(note_id)

        return note_id
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Validator fails with "missing reflection_policy"

**Solution**: Ensure `mirrorDNA_reflection_policy.yaml` exists and is referenced in manifest:
```yaml
# mirrorDNA_manifest.yaml
reflection_policy: "mirrorDNA_reflection_policy.yaml"
```

#### Issue 2: Checksum validation fails

**Solution**: Ensure checksums are calculated correctly:
```python
import hashlib

def checksum_sha256(content):
    if isinstance(content, str):
        content = content.encode('utf-8')
    return hashlib.sha256(content).hexdigest()
```

#### Issue 3: Session lineage broken

**Solution**: Verify predecessor/successor links are symmetric:
```sql
-- Check lineage integrity
SELECT
  s1.session_id,
  s1.successor,
  s2.predecessor
FROM sessions s1
LEFT JOIN sessions s2 ON s1.successor = s2.session_id
WHERE s1.successor IS NOT NULL
  AND s1.successor != s2.predecessor;
```

#### Issue 4: Vault path not found

**Solution**: Use absolute paths in continuity profile:
```yaml
vault:
  path: "/absolute/path/to/vault"  # ✅ Absolute path
  # path: "./vault"  # ❌ Relative path may fail
```

### Getting Help

- **Read the FAQ**: [docs/FAQ.md](FAQ.md)
- **Check examples**: [examples/](../examples/) directory
- **Review specifications**: [spec/](../spec/) directory
- **GitHub Discussions**: MirrorDNA-Standard repository
- **Validator docs**: [validators/README.md](../validators/README.md)

---

## Next Steps

1. **Choose your compliance level**: [CHOOSING_COMPLIANCE_LEVEL.md](CHOOSING_COMPLIANCE_LEVEL.md)
2. **Review the spec**: [spec/mirrorDNA-standard-v1.0.md](../spec/mirrorDNA-standard-v1.0.md)
3. **Study examples**: [examples/README.md](../examples/README.md)
4. **Run the validator**: [validators/README.md](../validators/README.md)
5. **Display your badge**: [badges/README.md](../badges/README.md)

---

⟡⟦INTEGRATION⟧ · ⟡⟦GUIDANCE⟧ · ⟡⟦ADOPTION⟧

**Document Version**: 1.0.0
**Last Updated**: 2025-11-18
**Canonical Source**: [MirrorDNA-Standard/docs/INTEGRATION.md](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/docs/INTEGRATION.md)
