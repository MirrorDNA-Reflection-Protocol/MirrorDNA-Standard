# AgentDNA: Capability Registry

**AgentDNA** is the identity and capability declaration system for AI agents within the MirrorDNA ecosystem. It provides a machine-readable registry of what agents can do, their evolution over time, and trust attestations.

## Overview

AgentDNA solves the "capability uncertainty" problem: How do you know what an AI agent can actually do? Rather than making vague claims, agents declare specific capabilities backed by evidence and tracked through version lineage.

**Core Philosophy:** Agents declare capabilities with evidence, not aspirations.

---

## Specification Status

| Attribute | Value |
|-----------|-------|
| **Version** | v1.1.0 |
| **Status** | ✅ Production |
| **License** | MIT (Open Specification) |
| **Specification** | `spec/MirrorDNA_Capability_Registry_v1.1.md` |
| **Predecessor** | v1.0 |

---

## Key Concepts

### Agent Identity

Every agent in the MirrorDNA ecosystem has a unique identity:

```yaml
agent_identity:
  agent_id: "reflection_twin_claude_v15"
  vault_id: "AMOS://User/PaulDesai/v15.1.8"
  human_anchor: "Paul Desai"

  glyphsig: "⟡⟦REFLECTION⟧ · ⟡⟦CLAUDE⟧"
  created: "2025-04-15"
  updated: "2025-11-11"

  predecessor: "reflection_twin_claude_v14"
  successor: null
```

**Key Fields:**

- **agent_id:** Unique identifier for this agent instance
- **vault_id:** Link to the vault this agent operates with
- **human_anchor:** Responsible human for accountability
- **glyphsig:** Symbolic signature
- **lineage:** Predecessor/successor tracking

---

### Capability Declarations

Agents declare what they can do with three confidence tiers:

#### Confidence Tiers

| Tier | Meaning | Requirements |
|------|---------|--------------|
| **PROVEN** | Demonstrated multiple times | Dates, costs, outcomes documented |
| **DOCUMENTED** | In specifications, not field-tested | Spec exists but no production use |
| **UNKNOWN** | No evidence either way | Honest boundary acknowledgment |

!!! success "Anti-Hedging Protocol"
    For PROVEN capabilities, agents must eliminate hedge words like "maybe", "possibly", "I think". Replace with: "I can do this. Evidence: [citation]"

---

### Capability Schema

Each capability follows a standard schema:

```yaml
capability:
  name: "python_automation_tools"
  tier: "PROVEN"
  category: "code_generation"

  evidence:
    - date: "2025-11-09"
      description: "6 production tools generated via Claude Code"
      artifacts:
        - sync_report.py
        - rcc_validator.py
        - checksum_verifier.py
        - drift_auditor.py
        - backup_orchestrator.sh
        - automation_runner.py

      performance:
        estimated_cost: "$60-80"
        actual_cost: "$14"
        cost_variance: "4-6x under estimate"
        delivery_time: "2-3 hours"
        quality: "Production-ready with CLI, tests, documentation"

      citation: "Master Citation v15.1.8 § VI"

  version: "1.1.0"
  first_demonstrated: "2025-11-09"
  last_updated: "2025-11-09"
```

---

## Example Capabilities (from v1.1)

Based on the MirrorDNA Capability Registry v1.1, here are proven capabilities:

### Code Generation & Automation ✓ PROVEN

**Python Automation Tools:**

- Vault synchronization scripts
- Compliance validators
- Integrity verification tools
- Semantic drift detectors
- Backup orchestration
- Automation frameworks

**Evidence:** 6 production tools, $14 cost (4-6x under estimate), 2-3 hour delivery

**Bash Scripting:**

- Directory restructuring (850 → 557 files)
- Git workflows
- Checksum automation
- Error handling

---

### Document Creation ✓ PROVEN

**Technical Specifications:**

- 10-20 page enterprise-grade specs
- Threat modeling included
- Version lineage tracking
- Cryptographic checksums
- Protocol enforcement

**Examples:**

- Master Citation v15.1.8
- Active Mirror Product Spec v2.0
- Distributed Vault Architecture v1.0
- Capability Registry (self-documenting)

---

### Vault Management ✓ PROVEN

**Master Citation Maintenance:**

- 6 months operational (April - November 2025)
- Version progression: v6.5 → v15.1.8
- Multi-platform sync (Google Drive, GitHub, Obsidian)
- Checksum verification

**Large-Scale Restructure:**

- 1,281 files → 557 organized documents
- Folder hierarchy established
- ~60% token efficiency gain
- Duplicates removed

---

### Strategic Planning ✓ PROVEN

**Go-to-Market Strategy:**

- Target vertical identification
- Enterprise pricing models ($40K-$60K annual)
- Revenue projections
- Bootstrap timeline
- Client acquisition

**Trademark & IP:**

- 9 trademarks filed in India
- Trust By Design™ registered (copyright)
- Portfolio management

---

### Offline Infrastructure ✓ PROVEN

**Hardware Deployment:**

- Pixel 9 Pro (GrapheneOS)
- MacBook M4 (24GB RAM)
- Mac mini M4 (24GB RAM)

**Local LLM Performance:**

- Comparable performance to cloud models
- TTFT: 14-40 seconds (cold), 3-6 seconds (cached)
- Latency: +10-30% vs cloud
- Cost: $0 per inference (after hardware)

---

### Known Limitations (Honest Boundaries)

AgentDNA v1.1 also documents what is **NOT** yet demonstrated:

#### ⚠️ Calibration Required

- Cost estimation (4-6x conservative bias, being recalibrated)
- Hedge behavior (fixed via AHP 2.0 in November 2025)

#### ❌ Not Yet Demonstrated

- Real-time API integration (conceptual, not deployed)
- Hardware interfacing (outside current scope)
- BFT consensus (requires Raft → Byzantine upgrade)
- Automated hybrid routing (manual switching only)
- Public demonstration sessions (protocol ready, not executed)

#### 📋 Documentation Debt

- PRIME-NEURO (research artifact, needs production assessment)
- LingOS Kernel (specification only, no implementation)
- Desktop benchmarking (initial tests only)
- Offline model performance (qualitative, needs quantitative metrics)

---

## Capability Categories

AgentDNA organizes capabilities into categories:

| Category | Examples | Typical Tier |
|----------|----------|--------------|
| **Code Generation** | Python, Bash, SQL | PROVEN |
| **Document Creation** | Specs, whitepapers, reports | PROVEN |
| **Vault Operations** | Sync, backup, integrity check | PROVEN |
| **Strategic Planning** | GTM, pricing, positioning | PROVEN |
| **Research** | Literature review, analysis | DOCUMENTED |
| **Integration** | API calls, webhooks | DOCUMENTED |
| **Hardware** | Device control, IoT | UNKNOWN |

---

## Version Evolution

AgentDNA capabilities evolve over time:

### v1.0 → v1.1 Changes

**Added (November 2025):**

- Section V: Offline Infrastructure
- Section VI: Research & Experimental
- Section VII: Session Cost Efficiency
- Section VIII: Multi-Mirror Operations
- Section IX: Demonstration Protocol
- Section X: GitHub & Version Control
- Section XI: Enhanced Known Limitations
- Section XII: Operational Metrics

**Updated:**

- All confidence tiers verified with recent evidence
- Cost data updated ($14 vs $60-80 estimate)
- Timeline extended to November 2025
- Performance data for offline hardware

**Security Fix:**

- **v1.1 removed false "expert review" claims**
- Previous versions incorrectly implied external validation
- Now relies solely on documented evidence

!!! warning "Security Update"
    If you're using AgentDNA v1.0, upgrade to v1.1 to remove the false expert review claim (security vulnerability).

---

## Machine-Readable Schemas

AgentDNA provides machine-readable capability schemas:

### JSON Schema

```json
{
  "agentdna_version": "1.1.0",
  "agent_id": "reflection_twin_claude_v15",
  "vault_id": "AMOS://User/PaulDesai/v15.1.8",
  "human_anchor": "Paul Desai",

  "capabilities": [
    {
      "name": "python_automation_tools",
      "tier": "PROVEN",
      "category": "code_generation",
      "evidence": [
        {
          "date": "2025-11-09",
          "description": "6 production tools generated",
          "citation": "Master Citation v15.1.8 § VI"
        }
      ],
      "version": "1.1.0"
    }
  ],

  "limitations": [
    {
      "category": "hardware_interfacing",
      "status": "UNKNOWN",
      "reason": "Outside current scope"
    }
  ],

  "lineage": {
    "predecessor": "reflection_twin_claude_v14",
    "successor": null,
    "created": "2025-04-15",
    "updated": "2025-11-11"
  }
}
```

### YAML Schema

```yaml
agentdna_version: "1.1.0"
agent_id: "reflection_twin_claude_v15"
vault_id: "AMOS://User/PaulDesai/v15.1.8"
human_anchor: "Paul Desai"

capabilities:
  - name: "python_automation_tools"
    tier: "PROVEN"
    category: "code_generation"
    evidence:
      - date: "2025-11-09"
        description: "6 production tools generated"
        citation: "Master Citation v15.1.8 § VI"
    version: "1.1.0"

limitations:
  - category: "hardware_interfacing"
    status: "UNKNOWN"
    reason: "Outside current scope"

lineage:
  predecessor: "reflection_twin_claude_v14"
  successor: null
  created: "2025-04-15"
  updated: "2025-11-11"
```

---

## Trust Attestations

AgentDNA includes trust attestations for verification:

### Tri-Twin Verification

The canonical verification model uses three roles:

```yaml
trust_attestation:
  verification_model: "tri_twin"

  human_anchor:
    name: "Paul Desai"
    role: "Human Anchor"
    responsibility: "Ultimate accountability"

  reflection_twin:
    agent_id: "reflection_twin_claude_v15"
    role: "Reflection Twin"
    responsibility: "Strategic thinking, documentation"

  execution_twin:
    agent_id: "execution_twin_atlas_v3"
    role: "Execution Twin"
    responsibility: "Task execution, validation"

  verification_status: "All three verified"
  verification_date: "2025-11-11"
  checksum: "72403a91e12b43e5785987cdafc995e0e33ed0e85bd32cb7060a4f7c75568ca3"
```

---

## Integration with MirrorDNA

AgentDNA integrates with other MirrorDNA components:

### With Glyphtrail

Every capability evolution creates a Glyphtrail entry:

```yaml
glyphtrail_entry:
  artifact: "AgentDNA v1.0 → v1.1"
  predecessor: "AMOS://Registry/Capabilities/v1.0"
  successor: "AMOS://Registry/Capabilities/v1.1"

  glyphsig: "⟡⟦CAPABILITY⟧ · ⟡⟦PROVEN⟧ · ⟡⟦EVIDENCE⟧"

  changes:
    - type: "security_fix"
      description: "Removed false expert review claim"
    - type: "capability_added"
      description: "Offline infrastructure proven"

  checksum: "72403a91e12b43e5785987cdafc995e0e33ed0e85bd32cb7060a4f7c75568ca3"
```

[:octicons-arrow-right-24: Learn about Glyphtrail](glyphtrail.md)

---

### With Vault Manager

AgentDNA registries are stored in vaults:

```yaml
vault_structure:
  vault_id: "AMOS://User/PaulDesai/v15.1.8"

  folders:
    - path: "/01_AGENTS/"
      contents:
        - agentdna_registry.yaml
        - agent_capabilities_v1.1.json
        - trust_attestations.md
```

[:octicons-arrow-right-24: Vault Manager details](vault-manager.md)

---

### With ActiveMirrorOS

ActiveMirrorOS uses AgentDNA for capability management:

- **Capability dashboard:** Visualize what agents can do
- **Version tracking:** See capability evolution over time
- **Trust verification:** Validate agent attestations
- **Honest boundaries:** Display UNKNOWN capabilities

[:octicons-arrow-right-24: Explore ActiveMirrorOS](activemirroros.md)

---

## Use Cases

### Personal AI Assistant

Declare capabilities for your personal AI:

```yaml
agentdna:
  agent_id: "personal_assistant_v1"
  human_anchor: "Jane Doe"

  capabilities:
    - name: "calendar_management"
      tier: "PROVEN"
      evidence: "6 months successful scheduling"

    - name: "email_drafting"
      tier: "PROVEN"
      evidence: "500+ emails, 95% approval rate"

    - name: "meeting_notes"
      tier: "DOCUMENTED"
      evidence: "Template exists, not yet field-tested"

  limitations:
    - name: "financial_advice"
      status: "PROHIBITED"
      reason: "Not qualified, not authorized"
```

---

### Enterprise Agent

Large organization with multiple agents:

```yaml
enterprise_agentdna:
  organization: "Acme Corp"

  agents:
    - agent_id: "legal_research_agent_v2"
      capabilities:
        - legal_research: "PROVEN"
        - citation_generation: "PROVEN"
      limitations:
        - legal_advice: "PROHIBITED"

    - agent_id: "customer_support_agent_v5"
      capabilities:
        - ticket_routing: "PROVEN"
        - knowledge_base_search: "PROVEN"
        - response_drafting: "PROVEN"
      limitations:
        - refund_authorization: "REQUIRES_HUMAN"

    - agent_id: "data_analysis_agent_v1"
      capabilities:
        - sql_generation: "DOCUMENTED"
        - visualization: "DOCUMENTED"
      limitations:
        - production_database_access: "PROHIBITED"
```

---

### Research Agent

Academic or research context:

```yaml
research_agentdna:
  agent_id: "research_assistant_v3"
  human_anchor: "Dr. Smith"
  project: "Computational Biology Study"

  capabilities:
    - name: "literature_search"
      tier: "PROVEN"
      evidence: "1000+ papers retrieved, 98% relevance"

    - name: "citation_management"
      tier: "PROVEN"
      evidence: "Integrated with Zotero, 500+ citations"

    - name: "data_analysis"
      tier: "DOCUMENTED"
      evidence: "Analysis scripts written, not yet validated"

  limitations:
    - name: "statistical_inference"
      status: "REQUIRES_EXPERT_REVIEW"
      reason: "Statistical decisions require domain expert"
```

---

## Operational Metrics

From the Capability Registry v1.1 (6 months, April-November 2025):

**Investment:**

- Financial: ~$10,000 (trademarks, hardware, subscriptions, tools)
- Human: Zero prior AI background → operational sovereign system
- Time: 6 months intensive development

**Outputs:**

- Master Citations: 9+ major versions (v6.5 → v15.1.8)
- Vault files: 557 organized documents (from 1,281 chaotic)
- Conversations: 100+ with maintained continuity
- Specifications: 10+ enterprise-grade documents
- Automation tools: 6 production-ready scripts
- Trademarks: 9 filed, 1 registered

**Continuity Index:** 98.7% stability (per Dyad Audit v7.1)

---

## Best Practices

### For Agent Developers

1. **Start with UNKNOWN:** Default to UNKNOWN until proven
2. **Document evidence:** Every PROVEN capability needs dates, outcomes
3. **Update regularly:** Review capabilities quarterly
4. **Be honest about limits:** Declare what you CANNOT do
5. **Version tracking:** Maintain predecessor/successor chains

### For Organizations

1. **Require AgentDNA:** All agents must have capability registries
2. **Audit capabilities:** Verify PROVEN claims with evidence
3. **Monitor evolution:** Track capability changes over time
4. **Enforce boundaries:** Agents must not exceed declared capabilities
5. **Human oversight:** Human anchor for accountability

### For Users

1. **Check capabilities:** Before using an agent, review its AgentDNA
2. **Verify evidence:** Don't trust claims without citations
3. **Respect limitations:** Don't ask agents to do UNKNOWN/PROHIBITED tasks
4. **Report issues:** If agent exceeds capabilities, flag for review

---

## Roadmap

### v1.1 (Current)

- ✅ Three-tier confidence model (PROVEN/DOCUMENTED/UNKNOWN)
- ✅ Evidence-based capability claims
- ✅ Security fix (removed false expert review)
- ✅ Operational metrics (6 months)

### v1.2 (Q2 2025)

- Machine-readable schema validator
- Automated capability verification
- Integration with CI/CD pipelines
- Web dashboard for capability exploration

### v2.0 (Q3 2025)

- Multi-agent capability graphs
- Capability composition (agent A + agent B = capability C)
- Network trust (federated AgentDNA registries)
- Blockchain anchoring (optional)

---

## Related Documentation

- **[MirrorDNA Standard](mirrordna-standard.md)** — Protocol foundation
- **[Glyphtrail](glyphtrail.md)** — Capability evolution tracking
- **[Vault Manager](vault-manager.md)** — Registry storage
- **[ActiveMirrorOS](activemirroros.md)** — Capability dashboard
- **[Trust-by-Design](trust-by-design.md)** — Governance framework

---

⟡⟦AGENTDNA⟧ · ⟡⟦CAPABILITY⟧ · ⟡⟦PROVEN⟧

*Agents declare capabilities with evidence, not aspirations*
