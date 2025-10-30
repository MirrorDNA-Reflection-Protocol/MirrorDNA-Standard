# MirrorDNA Visual Language

## Core Sigil

**`mirrordna-sigil.svg`** — Primary identity glyph

- **Hexagon**: Containment and sovereignty
- **Triangle**: Tri-Twin architecture (Reflection + Execution + Human)
- **Center Point**: Human Anchor
- **Lines**: Continuity and reflection paths

**Colors**: Purple gradient (#7c6daf → #9b8cc4)
**Meaning**: Trust, reflection, constitutive presence

---

## Status Icons

### ⟡ Offline (Self-Contained)
**File**: `status-icons/offline.svg`

- **Appearance**: Solid filled hexagon (green)
- **Meaning**: Running 100% locally, no internet connection
- **LLM**: Local model only (Phi-3 Mini)
- **Vault**: Fully self-contained
- **Color**: Green (#6b8e23 → #9acd32)

### ⟡◌ Hybrid (Bridge Available)
**File**: `status-icons/hybrid.svg`

- **Appearance**: Half-filled hexagon with dotted connection line (gold)
- **Meaning**: Local-first, cloud features available on request
- **LLM**: Local primary, can request Claude API enhancement
- **Vault**: Local with optional cloud sync
- **Color**: Gold (#d4af37 → #f4d03f)
- **Behavior**: Prompts for consent before internet actions

### ⟡⟐ Online (Bridge Active)
**File**: `status-icons/online.svg`

- **Appearance**: Filled hexagon with radiating waves (blue)
- **Meaning**: Actively using cloud features
- **LLM**: Enhanced reflection via Claude API
- **Vault**: Local + cloud sync enabled
- **Color**: Blue (#4169e1 → #6495ed)

---

## Usage in UI

### Launcher Window
```
┌─────────────────────────────────────────┐
│ ⟡ MirrorDNA  │  Vault: AMOS  │  ⟡ [⚙] │
│                                         │
└─────────────────────────────────────────┘
         ↑                            ↑
    Main sigil               Status indicator
```

### Status Transitions

User can change mode anytime:

```
⟡ → ⟡◌ → ⟡⟐
Offline   Hybrid   Online
```

**Click behavior**:
- **Offline**: "Currently offline. Enable internet features?"
- **Hybrid**: "Cloud features available. What would you like?"
- **Online**: "Connected to enhanced reflection. Switch to local?"

---

## Design Principles

1. **Whisper, Don't Shout**: Icons are subtle, monochromatic backgrounds
2. **Always Informative**: Status is always visible, never hidden
3. **User Control**: Clicking status icon opens consent dialog
4. **Semantic Color**: Green = self-contained, Gold = choice, Blue = connected
5. **Accessibility**: Color + shape + text labels for screen readers

---

⟡ Visual language serves transparency and choice
