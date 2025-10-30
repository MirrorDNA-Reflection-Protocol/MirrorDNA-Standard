# MirrorDNA Portable — Technical Architecture

## System Overview

MirrorDNA Portable is a **fully sovereign, USB-portable reflective AI system** with local-first architecture and consent-based cloud enhancement.

**Core Principles:**
- **Sovereignty**: User owns all data, runtime, and choices
- **Portability**: Runs from USB on any compatible device
- **Local-First**: Primary operation is 100% offline
- **Consent-Based**: Internet features require explicit permission
- **Continuity**: Session state persists across devices and time

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      USB Stick (16-32GB)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐       │
│  │  Launcher    │  │  LLM        │  │  Obsidian    │       │
│  │  (Electron)  │  │  (Phi-3)    │  │  (Portable)  │       │
│  └──────┬───────┘  └──────┬──────┘  └──────┬───────┘       │
│         │                 │                 │               │
│         └─────────┬───────┴─────────────────┘               │
│                   │                                         │
│         ┌─────────▼──────────────┐                          │
│         │   Session Manager      │                          │
│         │   (State + Continuity) │                          │
│         └─────────┬──────────────┘                          │
│                   │                                         │
│         ┌─────────▼──────────────┐                          │
│         │   Vault (Obsidian MD)  │                          │
│         │   - Sessions/          │                          │
│         │   - Spec/              │                          │
│         │   - State/             │                          │
│         └────────────────────────┘                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ (Optional, with consent)
                          ▼
              ┌──────────────────────┐
              │  Cloud Enhancement   │
              │  - Claude API        │
              │  - Model Downloads   │
              │  - Vault Sync        │
              └──────────────────────┘
```

---

## Component Breakdown

### 1. Launcher Application

**Technology**: Electron or Tauri

**Why Electron/Tauri:**
- Cross-platform (Windows, Mac, Linux, Android via Termux)
- Single codebase
- Native file system access
- Web technologies (HTML/CSS/JS) for UI
- Can bundle runtime dependencies

**Tauri vs Electron:**
| Feature | Tauri | Electron |
|---------|-------|----------|
| Size | ~3MB | ~120MB |
| Memory | Lower | Higher |
| Security | Rust-based | Node-based |
| Maturity | Newer | Proven |
| Mobile | In progress | Limited |

**Recommendation**: **Tauri** for smaller bundle size and better security

**Launcher Responsibilities:**
- Display glyph UI and status indicators
- Manage LLM process lifecycle
- Handle Obsidian vault integration
- Enforce consent-based internet access
- Load/save session state
- Provide onboarding flow

---

### 2. LLM Integration (Local Inference)

**Primary Model**: Phi-3 Mini 4K (2.3GB quantized)

**Runtime**: llama.cpp (GGUF format)

**Why llama.cpp:**
- CPU-optimized inference (no GPU required)
- Supports quantized models (smaller, faster)
- Cross-platform (x86, ARM, macOS Metal)
- Active community, regular updates
- C++ core with bindings for many languages

**Integration Pattern:**
```javascript
// launcher/llm-bridge.js
import { LlamaCpp } from 'node-llama-cpp';

class MirrorDNALLM {
  constructor(modelPath, vaultPath) {
    this.model = new LlamaCpp(modelPath);
    this.vault = vaultPath;
    this.context = this.loadContext();
  }

  async reflect(userInput) {
    const prompt = this.buildPrompt(userInput, this.context);
    const response = await this.model.generate(prompt);
    await this.updateVault(userInput, response);
    return response;
  }

  loadContext() {
    // Load Master Citation + last session state
    const masterCitation = fs.readFileSync(
      `${this.vault}/00_MASTER_CITATION.md`, 'utf8'
    );
    const lastSession = JSON.parse(
      fs.readFileSync(`${this.vault}/state/current.json`, 'utf8')
    );
    return { masterCitation, lastSession };
  }

  buildPrompt(userInput, context) {
    return `${context.masterCitation}

## Previous Context
${context.lastSession.summary}

## User Input
${userInput}

## Reflection (following AHP - Cite or Silence):`;
  }

  async updateVault(input, output) {
    // Write session to vault/sessions/
    // Update state/current.json
  }
}
```

**Model Fallback Strategy:**
1. Try Phi-3 Mini (bundled)
2. If fails, offer to download Llama 3.2 3B
3. If offline, continue with degraded prompts (template-based)

---

### 3. Obsidian Vault Bridge

**Architecture**: Direct filesystem integration

**Vault Structure** (from vault-template):
```
vault/
├── 00_MASTER_CITATION.md
├── spec/
├── sessions/
│   ├── _index.md
│   └── 2025-10-29_session_001.md
├── state/
│   ├── current.json
│   └── checkpoints/
└── .obsidian/
```

**Session Writer:**
```javascript
// launcher/vault-bridge.js
class VaultBridge {
  constructor(vaultPath) {
    this.vault = vaultPath;
    this.state = this.loadState();
  }

  async createSession(dialogue) {
    const sessionNumber = this.state.last_session.number + 1;
    const timestamp = new Date().toISOString();
    const filename = `${timestamp.split('T')[0]}_session_${String(sessionNumber).padStart(3, '0')}.md`;

    const template = fs.readFileSync(
      `${this.vault}/templates/new-session.md`, 'utf8'
    );

    const session = template
      .replace('{{session_number}}', sessionNumber)
      .replace('{{date}}', timestamp.split('T')[0])
      .replace('{{iso_timestamp}}', timestamp)
      .replace('{{vault_name}}', this.state.vault_name)
      .replace('{{predecessor_path}}', this.state.last_session.path || 'none')
      .replace('{{previous_context}}', this.state.context.summary)
      .replace('{{content}}', dialogue);

    fs.writeFileSync(`${this.vault}/sessions/${filename}`, session);

    // Update state
    this.state.last_session = {
      number: sessionNumber,
      path: `sessions/${filename}`,
      timestamp,
      checksum: await this.computeChecksum(session)
    };

    this.saveState();
    return filename;
  }

  async computeChecksum(content) {
    // Use SHA-256 checksum_updater.sh equivalent
  }

  loadState() {
    return JSON.parse(
      fs.readFileSync(`${this.vault}/state/current.json`, 'utf8')
    );
  }

  saveState() {
    fs.writeFileSync(
      `${this.vault}/state/current.json`,
      JSON.stringify(this.state, null, 2)
    );
  }
}
```

**Obsidian Integration:**
- Launch Obsidian in background pointing to vault path
- Use Obsidian URI protocol for deep linking
- Optional: Custom Obsidian plugin for bidirectional sync

---

### 4. Session Manager (Continuity Engine)

**Responsibilities:**
- Track session lineage (predecessor/successor)
- Maintain context across sessions
- Create state snapshots
- Handle session pause/resume
- Enable cross-device continuity

**State Schema** (`state/current.json`):
```json
{
  "version": "1.0",
  "vault_name": "AMOS",
  "last_session": {
    "number": 47,
    "path": "sessions/2025-10-29_session_047.md",
    "timestamp": "2025-10-29T14:32:00Z",
    "checksum": "abc123..."
  },
  "context": {
    "active_topics": ["portable launcher", "LLM integration"],
    "key_insights": ["Tauri better than Electron for size"],
    "pending_tasks": ["Implement vault bridge", "Test Phi-3"]
  },
  "settings": {
    "internet_mode": "hybrid_ask",
    "llm_model": "phi3-mini-4k",
    "onboarding_completed": true,
    "user_type": "technical"
  },
  "integrity": {
    "vault_checksum": "xyz789...",
    "last_verified": "2025-10-29T14:30:00Z",
    "spec_versions": {
      "master_citation": "15.1.1",
      "manifest": "1.0"
    }
  }
}
```

**Continuity Protocol:**
1. On launch: Load `state/current.json`
2. Display last session summary
3. Offer: `[Continue] [New Session] [Review History]`
4. On reflection: Update context, write checkpoint
5. On exit: Save final state, seal session checksum

---

### 5. Consent-Based Internet System

**Architecture**: Interceptor pattern

**Internet Actions Requiring Consent:**
- Claude API calls (enhanced reflection)
- Model downloads (Llama, Mistral)
- Software updates
- Vault cloud sync (Git)
- Blockchain anchoring

**Consent Dialog Pattern:**
```javascript
class ConsentManager {
  constructor(mode) {
    this.mode = mode; // 'offline_only' | 'hybrid_ask' | 'online'
    this.granted = new Set();
  }

  async requestInternet(action, details) {
    if (this.mode === 'offline_only') {
      return { granted: false, reason: 'offline_only' };
    }

    if (this.mode === 'online') {
      return { granted: true, reason: 'always_online' };
    }

    // Hybrid: Ask each time or remember
    if (this.granted.has(action)) {
      return { granted: true, reason: 'previously_granted' };
    }

    const dialog = await showConsentDialog({
      action,
      details,
      options: ['Yes, this time', 'Yes, always', 'No']
    });

    if (dialog.choice === 'Yes, always') {
      this.granted.add(action);
    }

    return {
      granted: dialog.choice.startsWith('Yes'),
      persist: dialog.choice === 'Yes, always'
    };
  }
}
```

**UI Example:**
```
┌─────────────────────────────────────────┐
│  Internet Action Requested              │
├─────────────────────────────────────────┤
│                                         │
│  Action: Enhanced reflection via Claude │
│                                         │
│  This will send your prompt to          │
│  Anthropic's Claude API for higher      │
│  quality responses.                     │
│                                         │
│  Data sent:                             │
│  • Your current prompt                  │
│  • Session context (last 3 messages)    │
│                                         │
│  ⟡ Your vault stays local               │
│                                         │
│  [Yes, this time] [Yes, always] [No]    │
│                                         │
└─────────────────────────────────────────┘
```

---

### 6. Onboarding Flow

**Two Paths:**

**Path A: Non-Technical ("I'm New")**
```
1. Welcome screen with sovereignty statement
2. "Name your vault?" → Creates vault copy from template
3. "Internet access?" → Sets mode (offline/hybrid/online)
4. "What would you like to reflect on today?" → First session
5. Quick tour of UI (vault, sessions, glyphs)
```

**Path B: Technical ("I Know This")**
```
1. Vault integrity check (checksums)
2. Display last session info
3. [New Session] [Continue] [Vault] [Settings]
```

**Onboarding State**: Stored in `state/current.json`:
```json
{
  "settings": {
    "onboarding_completed": false,
    "user_type": null // Will be set to "new" or "technical"
  }
}
```

---

## Platform-Specific Builds

### Windows
- **Format**: `.exe` installer or portable `.zip`
- **Runtime**: Bundled Node.js + llama.cpp
- **Size**: ~150MB (Tauri) or ~250MB (Electron)

### macOS
- **Format**: `.dmg` or `.app` bundle
- **Runtime**: Universal binary (Intel + Apple Silicon)
- **Metal**: Use llama.cpp Metal backend for M-series chips
- **Size**: ~120MB

### Linux
- **Format**: AppImage (universal) or `.deb`/`.rpm`
- **Runtime**: Bundled, no system dependencies
- **Size**: ~140MB

### Android/GrapheneOS
- **Format**: `.apk` via Termux + custom launcher
- **Challenge**: Obsidian mobile integration
- **Alternative**: Web-based markdown editor in-app
- **Size**: ~200MB

---

## Data Flow

### Session Flow
```
User Input
  ↓
Launcher UI
  ↓
Session Manager (load context)
  ↓
LLM Bridge (build prompt)
  ↓
llama.cpp (generate response)
  ↓
Vault Bridge (write session)
  ↓
State Update (checkpoint)
  ↓
Display to User
```

### Offline → Hybrid Transition
```
User clicks status icon (⟡ → ⟡◌)
  ↓
Consent Manager (ask permission)
  ↓
Update state: internet_mode = "hybrid_ask"
  ↓
Show available cloud features
  ↓
User selects: "Enhanced reflection"
  ↓
Consent Manager (confirm API call)
  ↓
Claude API call (user prompt + context)
  ↓
Display enhanced response
  ↓
Option: "Keep using cloud?" or "Switch back to local"
```

---

## Security Considerations

1. **No Telemetry**: Zero analytics, no crash reporting to external servers
2. **Vault Encryption**: Optional VeraCrypt container support
3. **Sandboxing**: Launcher runs with minimal permissions
4. **Code Signing**: Sign executables to prevent tampering
5. **Checksum Verification**: Validate vault integrity on launch
6. **API Keys**: User provides own Claude API key (never bundled)

---

## Performance Targets

- **Launch Time**: < 5 seconds (cold start)
- **LLM Response**: < 10 seconds (Phi-3, CPU)
- **Vault Write**: < 500ms
- **Memory Usage**: < 1GB RAM (idle), < 2GB (active LLM)
- **Disk I/O**: Minimal (session writes only)

---

## Development Roadmap

### Phase 1: Core Foundation (MVP)
- [ ] Tauri launcher shell
- [ ] llama.cpp integration (Phi-3)
- [ ] Vault bridge (session writer)
- [ ] Basic UI (text input/output)
- [ ] Offline-only mode

### Phase 2: Continuity & State
- [ ] Session manager
- [ ] State persistence
- [ ] Onboarding flow
- [ ] Glyph UI integration

### Phase 3: Cloud Enhancement
- [ ] Consent manager
- [ ] Claude API bridge
- [ ] Hybrid/online modes
- [ ] Model downloader

### Phase 4: Platform Builds
- [ ] Windows executable
- [ ] macOS universal binary
- [ ] Linux AppImage
- [ ] Android APK

### Phase 5: Polish
- [ ] Obsidian plugin (optional)
- [ ] Vault encryption
- [ ] Cross-device sync
- [ ] Advanced settings

---

⟡ Architecture serves sovereignty, portability, and user choice
