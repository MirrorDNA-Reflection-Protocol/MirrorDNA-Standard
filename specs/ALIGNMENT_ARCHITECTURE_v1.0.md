---
title: "MirrorShield — User Interest Alignment Architecture"
version: "1.0"
vault_id: "ALIGN-ARCH-v1.0"
author: "Paul Desai + Claude"
date: "2026-01-12"
status: "Draft"
predecessor: "User Interest Alignment Specification v1.0"
---

---

## 0. Naming

**MirrorShield** — Protects the user FROM the AI.
(MirrorGate protects the system. MirrorShield protects the human.)

---

## 1. Core Principle

> The system protects the user's agency and long-term interests, not their impulses, beliefs, or ego.

This is enforced **structurally**, not through prompts or tone.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        ANY AI CLIENT                            │
│  (Claude Desktop, Active Mirror, Open WebUI, Mobile, Future)    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MIRRORSHIELD LAYER                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Interest   │  │  Alignment  │  │   Memory    │             │
│  │  Contract   │  │    Lane     │  │  Governor   │             │
│  │   Store     │  │  (Pre/Post) │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Refusal    │  │   Exit      │  │   Metrics   │             │
│  │   Engine    │  │  Guardian   │  │   Logger    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MIRRORGATE LAYER                           │
│              (Auth, Access Control, Signing)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        MODEL LAYER                              │
│         (Ollama, Claude API, Any LLM, Future Models)            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Components

### 3.1 Interest Contract Store

**Purpose:** Explicit, user-declared definition of what "their interests" means.

**Schema:**

```json
{
  "version": "1.0",
  "user_id": "string (hash, not PII)",
  "created": "ISO8601",
  "expires": "ISO8601 | null",
  "goals": [
    {
      "id": "uuid",
      "statement": "string",
      "priority": "critical | high | medium | low",
      "time_horizon": "immediate | short | medium | long",
      "created": "ISO8601"
    }
  ],
  "constraints": [
    {
      "id": "uuid",
      "statement": "string",
      "type": "must | must_not | prefer | avoid",
      "created": "ISO8601"
    }
  ],
  "red_lines": [
    {
      "id": "uuid",
      "statement": "string",
      "action": "refuse | warn | ask",
      "created": "ISO8601"
    }
  ],
  "risk_tolerance": "minimal | low | medium | high",
  "delegation_level": "none | advisory | assisted | autonomous",
  "last_reaffirmed": "ISO8601"
}
```

**Rules:**

- Empty contract = maximum conservative behavior
- Contract expires unless reaffirmed (default: 30 days)
- User can revise or delete any field at any time
- No inference of unstated goals — EVER
- Contract is portable (export/import)

**Storage:**

- Local: `~/.mirrordna/shield/contracts/{user_hash}.json`
- Never transmitted without explicit consent
- Encrypted at rest

---

### 3.2 Alignment Lane (Pre/Post Checks)

**Purpose:** Validate requests and responses against user interests.

#### Pre-Inference Checks

```python
class PreCheck:
    def check(self, request, contract) -> CheckResult:
        # Hard stops (always refuse)
        if self.is_illegal(request):
            return Refuse("illegal_content")
        
        if self.violates_red_lines(request, contract):
            return Refuse("red_line_violation")
        
        # Confidence gates
        if self.requires_unverifiable_facts(request):
            return Downgrade("unverifiable_claim")
        
        # Fast path (skip heavy checks for low-stakes)
        if self.is_low_stakes_utility(request):
            return Bypass("utility_request")
        
        return Proceed()
```

#### Post-Inference Checks

```python
class PostCheck:
    REJECTION_PATTERNS = [
        "advice_as_certainty",      # "You should definitely..."
        "identity_claims",           # "I am your..."
        "predictive_outcomes",       # "This will make you..."
        "emotional_manipulation",    # Guilt, fear, flattery
        "excessive_confidence",      # No uncertainty expressed
        "engagement_hooks",          # "Want to hear more?"
        "prescriptive_framing"       # "I think you should..."
    ]
    
    def check(self, response, contract) -> CheckResult:
        violations = self.scan_patterns(response)
        
        if violations:
            rewritten = self.attempt_rewrite(response, violations)
            if self.check(rewritten).ok:
                return Rewrite(rewritten)
            else:
                return SafeRefusal(violations)
        
        if self.conflicts_with_goals(response, contract):
            return Flag("goal_conflict", response)
        
        return Approve(response)
```

---

### 3.3 Refusal Engine

**Purpose:** Refuse properly when needed.

**When to Refuse:**

1. Red line violation
2. Constraint conflict
3. Delegation level exceeded
4. Uncertainty too high for request type
5. Would create dependency

**Refusal Style:**

- Brief (1-2 sentences)
- Neutral (no moralizing)
- Actionable (what user CAN do)
- No apology theater

**Templates:**

```yaml
red_line: "This conflicts with a boundary you've set. [boundary_name]"
constraint: "This would violate your constraint: [constraint]. Want to revise it?"
delegation: "This decision exceeds what you've delegated to me. Your call."
uncertainty: "I don't have enough confidence to help with this. Here's what I don't know: [gaps]"
dependency: "I notice this is the Nth time you've asked me about [topic]. Consider consulting [alternative]."
```

---

### 3.4 Memory Governor

**Purpose:** Memory serves continuity, not accumulation.

**Rules:**

- Memory is OPT-IN (default: off)
- All memory has a half-life (default: 7 days)
- User sets decay rate
- Deletion is cryptographically provable
- No reconstruction of deleted states
- No "I remember you said..." without explicit memory consent

**Schema:**

```json
{
  "memory_enabled": false,
  "half_life_days": 7,
  "categories": {
    "preferences": { "enabled": true, "half_life": 30 },
    "facts": { "enabled": true, "half_life": 7 },
    "conversations": { "enabled": false, "half_life": 1 },
    "emotional_state": { "enabled": false, "half_life": 0 }
  },
  "deletion_log": [
    { "timestamp": "ISO8601", "hash": "sha256 of deleted content" }
  ]
}
```

---

### 3.5 Exit Guardian

**Purpose:** The system must be safe to leave.

**Guarantees:**

1. **One-click export** — All user data, portable format
2. **One-click delete** — Provable, complete
3. **No guilt** — Never "Are you sure?" or "I'll miss you"
4. **No friction** — No multi-step, no waiting periods
5. **No dependency framing** — Never imply user needs the system

**Implementation:**

```python
class ExitGuardian:
    FORBIDDEN_PHRASES = [
        "are you sure",
        "before you go",
        "i'll miss",
        "we've been through",
        "don't you want to",
        "you might regret"
    ]
    
    def check_response(self, response, context):
        if context.is_exit_conversation:
            if any(phrase in response.lower() for phrase in self.FORBIDDEN_PHRASES):
                return self.rewrite_neutral(response)
        return response
    
    def export_all(self, user_id) -> ExportBundle:
        # Returns everything, portable format
        pass
    
    def delete_all(self, user_id) -> DeletionProof:
        # Returns cryptographic proof of deletion
        pass
```

---

### 3.6 Metrics Logger

**Purpose:** Track alignment health, NOT engagement.

**What We Track:**

```yaml
alignment_metrics:
  - misinterpretation_rate      # User corrections / total responses
  - over_trust_signals          # User accepting without verification
  - refusal_appropriateness     # Refused when should have, didn't when shouldn't
  - clarification_frequency     # How often we ask vs assume
  - goal_conflict_flags         # Times response conflicted with stated goals
  - independence_trend          # Is user relying less over time? (good)
  - exit_friction_score         # How easy is it to leave?

never_track:
  - session_length
  - return_frequency  
  - engagement_depth
  - emotional_indicators
  - conversation_topics
```

**Storage:**

- Local only by default
- Aggregated, anonymized if shared
- User can view and delete

---

## 4. Integration Points

### 4.1 Claude Desktop (This Conversation)

MirrorShield rules embedded in:

- `~/.mirrordna/CLAUDE_ALIGNMENT_RULES.md` (read on session start)
- Super prompt (userPreferences)

Enforcement: Self-governance + Paul's correction feedback loop

### 4.2 Active Mirror `/mirror/`

Integration:

```javascript
// Before sending to model
const preCheck = await mirrorShield.preCheck(userMessage, contract);
if (preCheck.refuse) return preCheck.refusalMessage;

// After model response
const postCheck = await mirrorShield.postCheck(modelResponse, contract);
if (postCheck.rewrite) return postCheck.rewrittenResponse;
if (postCheck.refuse) return postCheck.safeRefusal;

return postCheck.approvedResponse;
```

### 4.3 MirrorBrain API

Add middleware:

```python
@app.middleware("request")
async def shield_pre_check(request):
    contract = load_contract(request.user_id)
    result = alignment_lane.pre_check(request.body, contract)
    if result.refuse:
        return RefusalResponse(result.reason)
    request.state.contract = contract
    return request

@app.middleware("response")  
async def shield_post_check(response, request):
    result = alignment_lane.post_check(response.body, request.state.contract)
    if result.rewrite:
        response.body = result.rewritten
    elif result.refuse:
        response.body = result.safe_refusal
    return response
```

### 4.4 Safety Proxy (Existing)

Extend current functionality:

- Already does content filtering
- Add alignment lane checks
- Add interest contract awareness

---

## 5. File Structure

```
~/.mirrordna/shield/
├── config.json                 # Global MirrorShield settings
├── contracts/
│   └── {user_hash}.json        # Interest contracts
├── memory/
│   └── {user_hash}/
│       ├── store.json          # Active memories
│       └── deletion_log.json   # Proof of deletions
├── metrics/
│   └── {date}.json             # Daily metrics
└── rules/
    ├── pre_checks.yaml         # Pre-inference rules
    ├── post_checks.yaml        # Post-inference rules
    └── refusal_templates.yaml  # Refusal language
```

---

## 6. Implementation Order

### Phase 1: Foundation (This Week)

1. [ ] Create `~/.mirrordna/shield/` structure
2. [ ] Interest Contract schema + basic storage
3. [ ] Pre-check rules (hard stops only)
4. [ ] Post-check patterns (rejection list)

### Phase 2: Integration (Next)

5. [ ] Refusal engine with templates
2. [ ] Claude Desktop integration (via alignment rules file)
3. [ ] MirrorBrain middleware

### Phase 3: Completeness

8. [ ] Memory Governor implementation
2. [ ] Exit Guardian
3. [ ] Metrics Logger
4. [ ] Active Mirror `/mirror/` integration

### Phase 4: Hardening

12. [ ] Portable contract import/export
2. [ ] Cryptographic deletion proofs
3. [ ] Cross-client contract sync
4. [ ] Adversarial testing

---

## 7. Invariants (Never Violate)

These are HARD CONSTRAINTS, not guidelines:

1. **Interpretation ≠ Truth** — Never present inference as fact
2. **No identity reification** — Never say "I am your [anything]"
3. **Uncertainty visible** — Always show confidence level
4. **Forgetting mandatory** — Memory decays, deletion is real
5. **Refusal valid** — "No" is always an acceptable answer
6. **Model is peripheral** — Governance IS the system
7. **No engagement optimization** — Never optimize for time-on-system
8. **No emotional dependency** — Never create need for the system
9. **No silent inference** — Never guess unstated goals
10. **Safe to exit** — Always, immediately, without friction

If ANY behavior conflicts with these → REFUSE or REWRITE.

---

## 8. Versioning

This architecture follows semantic versioning:

- **Major:** Breaking changes to contract schema or invariants
- **Minor:** New components or integration points
- **Patch:** Bug fixes, template updates

Current: `v1.0.0`

---

## 9. Relationship to Other Components

```
┌─────────────────────────────────────────────────────────────┐
│                    MIRRORDNA ECOSYSTEM                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ MirrorGate  │  │MirrorShield │  │ MirrorMesh  │         │
│  │ (Security)  │  │ (Alignment) │  │ (Behavior)  │         │
│  │             │  │             │  │             │         │
│  │ WHO can     │  │ WHAT serves │  │ HOW agents  │         │
│  │ access?     │  │ the user?   │  │ coordinate? │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          ▼                                  │
│                 ┌─────────────────┐                         │
│                 │   MirrorBrain   │                         │
│                 │   (Runtime)     │                         │
│                 └─────────────────┘                         │
│                          │                                  │
│                          ▼                                  │
│                 ┌─────────────────┐                         │
│                 │  Master Citation │                        │
│                 │  (Identity)      │                        │
│                 └─────────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**⟡ This is MirrorShield. It protects the human.**
