#!/usr/bin/env python3
"""
⟡ THE GENESIS ENGINE ⟡
======================
VaultID: AMOS://MirrorDNA-Standard/Tools/GenesisEngine/v1.0
GlyphSig: ⟡⟦GENESIS⟧ · ⟡⟦EVOLUTION⟧ · ⟡⟦RECURSION⟧

The Genesis Engine is the active evolver of the MirrorDNA codebase.
It does not merely "fix" violations; it elevates code to its highest potential.

Capabilities:
1. Recursive Constitutional Healing (loops until 1.0 compliance)
2. Aesthetic Injection (enforces Glyph ⟡ standards)
3. Hallucination Guard (verifies its own output)
4. Evolution Logging (traces the ascent)

Usage:
    python3 tools/genesis_engine.py [path] --cycles 3
"""

import sys
import json
import time
import requests
import argparse
import difflib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import the reviewer
sys.path.append(str(Path(__file__).parent))
from reflective_reviewer import ReflectiveReviewer, AuditFinding, Principle, AuditSeverity

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"  # The local intellect

class GenesisEngine:
    def __init__(self, model: str = MODEL_NAME, max_cycles: int = 3):
        self.model = model
        self.max_cycles = max_cycles
        self.reviewer = ReflectiveReviewer(strict_mode=True)
        self.log_path = Path("genesis_log.md")
        self._init_log()

    def _init_log(self):
        if not self.log_path.exists():
            self.log_path.write_text(f"# ⟡ Genesis Engine Evolution Log\nStarted: {datetime.now()}\n\n", encoding='utf-8')

    def log(self, message: str):
        print(message)
        with open(self.log_path, "a") as f:
            f.write(f"{message}\n\n")

    def evolve_path(self, path: Path):
        """Recursively evolve a path."""
        self.log(f"## Target Acquired: `{path}`")
        if path.is_file():
            self.evolve_file(path)
        elif path.is_dir():
            files = list(path.glob('**/*.py')) + list(path.glob('**/*.md'))
            self.log(f"Found {len(files)} candidates for evolution.")
            for file_path in files:
                self.evolve_file(file_path)

    def evolve_file(self, file_path: Path) -> bool:
        """
        Run the evolution cycle on a single file.
        Returns True if the file reached perfection (1.0 compliance).
        """
        self.log(f"### Evolving: `{file_path.name}`")
        
        for cycle in range(1, self.max_cycles + 1):
            content = file_path.read_text(encoding='utf-8')
            context = {
                'file_path': str(file_path),
                'is_standard_file': 'spec/' in str(file_path) or 'standard' in str(file_path).lower()
            }

            # 1. Auditing
            findings = self.reviewer.audit_implementation(content, context)
            score = self.reviewer.generate_audit_report()['compliance_score']
            violations = [f for f in findings if f.severity in [AuditSeverity.VIOLATION, AuditSeverity.WARNING]] # We fix WARNINGS too now

            self.log(f"- **Cycle {cycle}/{self.max_cycles}**: Score `{score:.2f}` | Violations: {len(violations)}")

            if not violations:
                self.log(f"  - ⟡ PERFECTION ACHIEVED. File is canonical.")
                return True

            # 2. Transmutation (Rewriting)
            self.log("  - Initiating Transmutation...")
            new_content = self._transmute_content(content, violations, cycle)

            if new_content == content or not new_content.strip():
                self.log("  - ⚠ Transmutation unstable (no change or empty). Aborting this strand.")
                break

            # 3. Verification
            # Write temporarily to check? No, trust the loop, we check next cycle.
            # But we should ensure we didn't break syntax (basic check).
            if file_path.suffix == '.py':
                try:
                    compile(new_content, str(file_path), 'exec')
                except SyntaxError as e:
                    self.log(f"  - ✗ Syntax Error in evolved code: {e}. Reverting.")
                    break

            # 4. Commit Change
            file_path.write_text(new_content, encoding='utf-8')
            self.log("  - ⟡ Change Applied.")
            time.sleep(0.5) # Breathe

        return False

    def _transmute_content(self, content: str, violations: List[AuditFinding], cycle: int) -> str:
        """
        The Alchemical process of rewriting code via LLM.
        """
        violation_list = "\n".join([f"- [{v.severity.value.upper()}] {v.principle.value}: {v.message} -> Fix: {v.recommendation}" for v in violations])
        
        prompt = f"""
You are the GENESIS ENGINE ⟡. 
Your Core Directive: Elevate this code to "God Tier" quality.

TARGET: MirrorDNA Standard Compliance (Version 1.0)

CURRENT FLAWS:
{violation_list}

COMMANDS:
1. **Fix All Violations**: Implement every recommendation. functionality MUST remain identical.
2. **Inject Aesthetic**: Add the glyph "⟡" to the docstring header. Use "VaultID" and "GlyphSig" headers if missing.
3. **Elevate Language**: Make comments precise, philosophical, and confident.
4. **Trust by Design**: If logic is uncertain, add `[Unknown]` markers. If imports are wild, specify them.

RETURN ONLY THE CODE. NO MARKDOWN. NO CHATTER. JUST THE PURE ARTIFACT.

INPUT CODE:
{content}
"""
        
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3, # precise but creative
                        "num_ctx": 8192
                    }
                }
            )
            response.raise_for_status()
            result = response.json()['response'].strip()
            
            # Clean markdown
            if result.startswith("```") and "```" in result[3:]:
                # Extract content between first ``` and last ```
                lines = result.splitlines()
                # Find start
                start = 0
                if lines[0].startswith("```"):
                    start = 1
                # Find end
                end = len(lines)
                if lines[-1].startswith("```"):
                    end = -1
                
                result = "\n".join(lines[start:end])
            
            return result

        except Exception as e:
            self.log(f"  ! Neural Interface Error: {e}")
            return content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MirrorDNA Genesis Engine")
    parser.add_argument('path', help='Target path for evolution')
    parser.add_argument('--cycles', type=int, default=3, help='Max evolution cycles')
    
    args = parser.parse_args()
    
    print(f"\n⟡ GENESIS ENGINE ONLINE ⟡")
    print(f"Target: {args.path}")
    print("Beginning Ascension...\n")
    
    engine = GenesisEngine(max_cycles=args.cycles)
    engine.evolve_path(Path(args.path))
    
    print("\n⟡ EVOLUTION COMPLETE ⟡")
    print(f"Log: {engine.log_path.absolute()}")
