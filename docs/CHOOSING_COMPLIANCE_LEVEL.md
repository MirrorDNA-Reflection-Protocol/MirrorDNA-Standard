# Choosing Your Compliance Level

**Purpose**: Help you decide which MirrorDNA compliance level fits your project.

**Quick answer**: Start with Level 1. Upgrade as you need more features.

---

## Decision Matrix

| Feature | Level 1 | Level 2 | Level 3 |
|---------|---------|---------|---------|
| **Anti-hallucination (AHP)** | ✅ | ✅ | ✅ |
| **Explicit uncertainty** | ✅ | ✅ | ✅ |
| **Basic session tracking** | ✅ | ✅ | ✅ |
| **Trust markers** | ✅ | ✅ | ✅ |
| **State persistence** | ❌ | ✅ | ✅ |
| **Session lineage** | ❌ | ✅ | ✅ |
| **Checksum validation** | ❌ | ✅ | ✅ |
| **Session recovery** | ❌ | ✅ | ✅ |
| **Vault storage** | ❌ | ❌ | ✅ |
| **Sovereign identity** | ❌ | ❌ | ✅ |
| **Glyph signatures** | ❌ | ❌ | ✅ |
| **Interaction safety** | ❌ | ❌ | ✅ |

---

## Level 1: Basic Reflection

### Choose Level 1 If:

✅ **Anti-hallucination is your priority**
- You want AI to cite sources or say "I don't know"
- Fabricated information is unacceptable

✅ **You don't need state persistence**
- Each session is independent
- No memory across sessions required

✅ **You want minimal implementation effort**
- Quick to adopt (1-2 days)
- Low maintenance overhead

✅ **Your use case is stateless**
- Q&A systems
- Single-turn interactions
- Document analysis (no session state)

### Examples:

- **Chatbot** that answers questions from a knowledge base
- **Document analyzer** that summarizes PDFs
- **Code reviewer** that checks for bugs (no persistent memory)

### Implementation Complexity: ⭐ Low

**Effort**: 1-2 days  
**Files needed**: 2 (manifest + policy)  
**Infrastructure**: None (no storage required)  

---

## Level 2: Continuity Aware

### Choose Level 2 If:

✅ **You need multi-session conversations**
- Users return to continue previous conversations
- Context must persist across sessions

✅ **State preservation is critical**
- Tracking user preferences
- Maintaining project state
- Building long-term context

✅ **You want session lineage tracking**
- Audit trail of sessions
- Branching conversations
- Session recovery after errors

✅ **You can implement storage**
- File system, database, or cloud storage available
- Can implement checksum validation

### Examples:

- **Personal AI assistant** that remembers past conversations
- **Project management AI** that tracks tasks over weeks
- **Research assistant** that builds knowledge over time
- **Tutoring system** that adapts to learner progress

### Implementation Complexity: ⭐⭐ Medium

**Effort**: 1-2 weeks  
**Files needed**: 3 (manifest + policy + continuity profile)  
**Infrastructure**: Persistent storage (filesystem, DB, etc.)  

---

## Level 3: Vault-Backed Sovereign

### Choose Level 3 If:

✅ **User sovereignty is required**
- Users must own their data
- No vendor lock-in acceptable
- Privacy-first architecture

✅ **You're building a personal AI system**
- Runs on user's device or user-controlled server
- User controls all data
- Offline-first design

✅ **You need vault integration**
- Obsidian or custom vault
- Markdown-based knowledge management
- File-based storage with git sync

✅ **You want full MirrorDNA compliance**
- Glyph signatures for semantic marking
- Comprehensive interaction safety
- Production-grade continuity

### Examples:

- **ActiveMirrorOS** (canonical Level 3 implementation)
- **Personal knowledge assistant** (Obsidian-based)
- **USB-portable AI** that runs anywhere
- **Sovereign productivity suite** (user owns everything)

### Implementation Complexity: ⭐⭐⭐ High

**Effort**: 4-8 weeks  
**Files needed**: 3+ (manifest + policy + profile + vault)  
**Infrastructure**: Vault storage, glyph system, safety protocols  

---

## Upgrade Paths

### Start Small, Scale Up

```
Level 1 (Anti-hallucination)
   ↓
   Add state persistence
   ↓
Level 2 (Continuity Aware)
   ↓
   Add vault + sovereignty
   ↓
Level 3 (Vault-Backed Sovereign)
```

**Recommended approach**: Start with Level 1, prove value, then upgrade.

---

## Use Case Scenarios

### Scenario 1: Customer Support Bot

**Needs:**
- Answer questions from knowledge base
- No memory needed between sessions
- Must not hallucinate

**Recommended**: **Level 1**

**Why**: Stateless Q&A, anti-hallucination is key, no persistence needed.

---

### Scenario 2: Personal Productivity Assistant

**Needs:**
- Remember user preferences
- Track tasks across days/weeks
- Continue conversations later

**Recommended**: **Level 2**

**Why**: Needs continuity, but user doesn't require full vault sovereignty.

---

### Scenario 3: Private Health Journal AI

**Needs:**
- Ultra-private (user owns all data)
- Offline-first (no cloud)
- Long-term memory
- User controls vault

**Recommended**: **Level 3**

**Why**: Privacy + sovereignty + continuity = Level 3 requirement.

---

### Scenario 4: Research Paper Analyzer

**Needs:**
- Analyze papers for citations
- Extract key findings
- No state between analyses

**Recommended**: **Level 1**

**Why**: Single-use, stateless, cite-or-silence critical for accuracy.

---

### Scenario 5: Code Review Assistant (Multi-Project)

**Needs:**
- Remember project conventions
- Track review history
- Learn from past reviews

**Recommended**: **Level 2**

**Why**: Needs continuity across reviews, but not vault sovereignty.

---

### Scenario 6: Personal Life OS

**Needs:**
- Everything stored locally
- User owns all data
- Offline-capable
- Multi-year memory
- Private and sovereign

**Recommended**: **Level 3**

**Why**: Full sovereignty, vault storage, comprehensive safety.

---

## Technical Considerations

### Level 1 Tech Stack

**Minimal:**
- Any LLM (OpenAI, Claude, local)
- Prompt engineering (cite-or-silence)
- Basic session ID generation

**No infrastructure required.**

---

### Level 2 Tech Stack

**Moderate:**
- LLM + state storage (DB, filesystem, cloud)
- Session manager (lineage tracking)
- Checksum library (SHA-256)
- Serialization (JSON, pickle)

**Infrastructure:**
- Persistent storage
- Backup mechanism

---

### Level 3 Tech Stack

**Advanced:**
- LLM + vault system (Obsidian or custom)
- Glyph signature system
- Interaction safety module
- Vault sync (Git or custom)
- Markdown parsing
- File integrity verification

**Infrastructure:**
- Vault storage
- Git (optional but recommended)
- Desktop app (Electron) or server

---

## Cost Considerations

### Level 1

**Development**: 1-2 days × developer cost  
**Maintenance**: Minimal (just prompt updates)  
**Infrastructure**: $0 (no storage)  

**Total**: Low

---

### Level 2

**Development**: 1-2 weeks × developer cost  
**Maintenance**: Medium (storage, backups)  
**Infrastructure**: Storage costs (filesystem = free, cloud = variable)  

**Total**: Medium

---

### Level 3

**Development**: 4-8 weeks × developer cost  
**Maintenance**: High (vault, sync, safety)  
**Infrastructure**: Local storage (user-provided) or self-hosted  

**Total**: High (but user owns everything)

---

## Common Mistakes

### ❌ Mistake 1: Starting with Level 3

**Why bad**: Overengineering. Level 3 is complex.

**Better**: Start with Level 1, prove concept, then upgrade.

---

### ❌ Mistake 2: Skipping Levels

**Why bad**: Levels are cumulative. Level 3 requires Level 2 features.

**Better**: Implement Level 1 → Level 2 → Level 3 in order.

---

### ❌ Mistake 3: Choosing Level Based on "Coolness"

**Why bad**: Level 3 is cool but overkill for simple use cases.

**Better**: Choose based on actual requirements, not hype.

---

### ❌ Mistake 4: Under-leveling for Privacy-Critical Apps

**Why bad**: Health/finance apps need sovereignty (Level 3).

**Better**: If privacy is critical, go Level 3 from the start.

---

## Decision Flowchart

```
START
  │
  ├─ Do you need state persistence?
  │  │
  │  ├─ NO → Level 1 ✓
  │  │
  │  └─ YES → Do you need user sovereignty?
  │          │
  │          ├─ NO → Level 2 ✓
  │          │
  │          └─ YES → Level 3 ✓
```

---

## Still Unsure?

**Default recommendation**: Start with **Level 1**.

**Why:**
- Fast to implement
- Proves MirrorDNA value
- Easy to upgrade later

**Upgrade triggers:**
- Users want continuity → go Level 2
- Users want data ownership → go Level 3

---

## Questions to Ask Yourself

1. **Do users need to pick up where they left off?**  
   → YES = Level 2+

2. **Is user data sensitive (health, finance, personal)?**  
   → YES = Consider Level 3

3. **Can you implement vault storage?**  
   → NO = Max out at Level 2

4. **Is anti-hallucination your only concern?**  
   → YES = Level 1 is enough

5. **Are you building a personal/private system?**  
   → YES = Level 3

---

## Summary Table

| Use Case Type | Level | Why |
|---------------|-------|-----|
| Stateless Q&A | 1 | No memory needed |
| Multi-session chat | 2 | Needs continuity |
| Personal productivity | 2 or 3 | Depends on sovereignty need |
| Privacy-critical (health, finance) | 3 | Sovereignty required |
| Document analysis | 1 | Stateless |
| Long-term research assistant | 2 or 3 | Depends on data ownership |
| USB-portable AI | 3 | Sovereignty + offline |

---

⟡⟦CHOOSING_LEVEL⟧

*When in doubt, start with Level 1 and upgrade as you grow.*
