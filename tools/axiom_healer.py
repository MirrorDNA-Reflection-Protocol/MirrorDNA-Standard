#!/usr/bin/env python3
"""
MirrorDNA Axiom Healer
======================
Autonomic self-correction tool that:
1. Audits codebase using ReflectiveReviewer
2. Identifies constitutional violations
3. Uses local LLM (Ollama) to rewrite content for compliance
4. Verifies the fix

Usage:
    python3 tools/axiom_healer.py [path]
"""

import sys
import json
import requests
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Import the reviewer (assuming it's in the same directory or adjust path)
sys.path.append(str(Path(__file__).parent))
from reflective_reviewer import ReflectiveReviewer, AuditFinding, Principle, AuditSeverity

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"  # Fast, capable model

class AxiomHealer:
    def __init__(self, model: str = MODEL_NAME):
        self.model = model
        self.reviewer = ReflectiveReviewer(strict_mode=True)

    def heal_file(self, file_path: Path) -> bool:
        """
        Audit and heal a single file.
        Returns True if changes were made.
        """
        print(f"⟡ Auditing {file_path}...")
        
        # Initial Audit
        content = file_path.read_text(encoding='utf-8')
        context = {
            'file_path': str(file_path),
            'is_standard_file': 'spec/' in str(file_path) or 'standard' in str(file_path).lower()
        }
        
        findings = self.reviewer.audit_implementation(content, context)
        violations = [f for f in findings if f.severity in [AuditSeverity.VIOLATION, AuditSeverity.CRITICAL]]
        
        if not violations:
            print("  ✓ Compliant")
            return False
            
        print(f"  ⚠ Found {len(violations)} violations. Healing...")
        
        # Heal iteratively (one pass for now to avoid loops, but ideally recursive)
        new_content = self._rewrite_content(content, violations)
        
        if new_content == content:
            print("  ✗ Healing failed (LLM returned identical content or error)")
            return False
            
        # Verify fix
        verification_findings = self.reviewer.audit_implementation(new_content, context)
        remaining_violations = [f for f in verification_findings if f.severity in [AuditSeverity.VIOLATION, AuditSeverity.CRITICAL]]
        
        if len(remaining_violations) < len(violations):
            print(f"  ✓ Healing successful! Reduced violations from {len(violations)} to {len(remaining_violations)}")
            file_path.write_text(new_content, encoding='utf-8')
            return True
        else:
            print(f"  ✗ Healing ineffective. Violations remain: {len(remaining_violations)}")
            return False

    def _rewrite_content(self, content: str, violations: list[AuditFinding]) -> str:
        """
        Send content and violations to LLM for rewriting.
        """
        violation_desc = "\n".join([f"- {v.principle.value}: {v.message} ({v.recommendation})" for v in violations])
        
        prompt = f"""
You are the MirrorDNA Axiom Healer. Your task is to rewrite the following file content to fix Constitutional Violations.
Strictly adhere to the MirrorDNA Principles.

VIOLATIONS TO FIX:
{violation_desc}

INSTRUCTIONS:
1. Rewrite the minimal necessary parts of the content to satisfy the principles.
2. Do not change the logic or functionality, only the compliance aspects (e.g., adding citations, checksums, uncertainty markers).
3. Return ONLY the full valid rewritten file content. Do not include markdown code blocks (```) or explanation text. Just the raw content.

FILE CONTENT:
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
                        "temperature": 0.2,  # Low temp for precision
                        "num_ctx": 8192     # Large context for files
                    }
                }
            )
            response.raise_for_status()
            result = response.json()['response'].strip()
            
            # Remove markdown code blocks if the LLM ignored instruction
            if result.startswith("```") and result.endswith("```"):
                result = "\n".join(result.splitlines()[1:-1])
            elif result.startswith("```"):
                 result = "\n".join(result.splitlines()[1:])
            
            return result
            
        except Exception as e:
            print(f"  ! LLM Error: {e}")
            return content

    def heal_path(self, path: Path):
        """Recursively heal path."""
        if path.is_file():
            self.heal_file(path)
        elif path.is_dir():
            for file_path in path.glob('**/*.py'):
                self.heal_file(file_path)
            for file_path in path.glob('**/*.md'):
                self.heal_file(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MirrorDNA Axiom Healer")
    parser.add_argument('path', help='Path to heal')
    parser.add_argument('--model', default=MODEL_NAME, help='Ollama model to use')
    
    args = parser.parse_args()
    
    healer = AxiomHealer(model=args.model)
    healer.heal_path(Path(args.path))
