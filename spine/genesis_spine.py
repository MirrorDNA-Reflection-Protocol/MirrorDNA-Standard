#!/usr/bin/env python3
"""
⟡ GENESIS SPINE ⟡
=================
VaultID: AMOS://MirrorDNA-Standard/Spine/GenesisSpine/v1.0
GlyphSig: ⟡⟦SPINE⟧ · ⟡⟦EVOLUTION⟧ · ⟡⟦CORE⟧

The Genesis Spine is the shared intelligence layer for all MirrorDNA evolution engines.
It centralizes neural interface logic, persistent logging, and aesthetic standards.
"""

import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

class SemanticCache:
    def __init__(self, cache_path: Path):
        self.cache_path = Path(cache_path)
        self.cache = self._load()

    def _load(self) -> Dict[str, str]:
        if self.cache_path.exists():
            try:
                return json.loads(self.cache_path.read_text())
            except:
                return {}
        return {}

    def get(self, key: str) -> Optional[str]:
        # Simple exact match for now; semantic matching could be added later
        return self.cache.get(key)

    def set(self, key: str, value: str):
        self.cache[key] = value
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(self.cache, indent=2))

class NeuralInterface:
    def __init__(self, model="qwen3-8b-turbo", base_url="http://localhost:5002/v1/chat/completions"):
        self.model = model
        self.base_url = base_url
        self.cache = SemanticCache(Path("/Users/mirror-admin/Documents/MirrorDNA-Vault/ActiveMirrorOS/Logs/neural_cache.json"))

    def generate(self, prompt: str, temperature=0.3) -> str:
        """Calls the MirrorBrain V1 API and returns cleaned content, with caching."""
        import hashlib
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        
        cached = self.cache.get(prompt_hash)
        if cached:
            return cached

        try:
            # PROJECT OMEGA: Use V1 Chat Completion format
            response = requests.post(
                self.base_url,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "max_tokens": 1024
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract content from AXIOM response
            result = data["choices"][0]["message"]["content"]
            
            # Remove reflection markers for raw tool consumption
            if "◈ Pattern:" in result:
                result = result.split("◈ Pattern:")[0].strip()
            
            cleaned = self._clean_markdown(result)
            
            if cleaned:
                self.cache.set(prompt_hash, cleaned)
                
            return cleaned
        except Exception as e:
            print(f"  ! Neural Interface (V1) Error: {e}")
            return ""

    def _clean_markdown(self, text: str) -> str:
        """Removes markdown code fences if present."""
        if text.startswith("```"):
            lines = text.splitlines()
            start = 1
            # Check for language identifier
            if len(lines[0]) > 3:
                pass 
            
            # Find the last ```
            end = len(lines)
            for i in range(len(lines) - 1, 0, -1):
                if lines[i].strip() == "```":
                    end = i
                    break
            return "\n".join(lines[start:end])
        return text

class EvolutionLogger:
    def __init__(self, log_path: Path):
        self.log_path = Path(log_path)
        if not self.log_path.exists():
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            self.log_path.write_text(f"# ⟡ Genesis Evolution Log\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n", encoding='utf-8')

    def log(self, message: str):
        """Prints and appends to the evolution log."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted = f"[{timestamp}] {message}"
        print(formatted)
        with open(self.log_path, "a", encoding='utf-8') as f:
            f.write(f"{message}\n\n")

class GenesisAesthetics:
    @staticmethod
    def ensure_glyphs(content: str, vault_id: str, glyph_sig: str) -> str:
        """Ensures the content has the canonical MirrorDNA header."""
        if "⟡" in content[:500]:
            return content
        
        header = f'"""\n⟡ {vault_id.split("/")[-1].upper()} ⟡\n'
        header += "=" * (len(header) - 5) + "\n"
        header += f"VaultID: {vault_id}\n"
        header += f"GlyphSig: {glyph_sig}\n"
        header += '"""\n\n'
        return header + content
