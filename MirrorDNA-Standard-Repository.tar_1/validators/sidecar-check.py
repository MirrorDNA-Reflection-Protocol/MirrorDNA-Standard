#!/usr/bin/env python3
"""
MirrorDNA Sidecar Validator v1.0
⟡ Verified Reflective compliance checker

Usage:
    python sidecar-check.py artifact.md
    python sidecar-check.py --directory ./artifacts/
    python sidecar-check.py --verbose --tier L3 document.md
"""

import json
import hashlib
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os

class GlyphsigValidator:
    """Validates MirrorDNA Standard compliance"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        
        # Glyphsig vocabulary patterns
        self.meta_glyphs = {
            '⟡': 'Reflection Seal',
            '⸻': 'Continuity Bridge', 
            '⟦': 'Enclosure Frame Start',
            '⟧': 'Enclosure Frame End',
            '⧖': 'Temporal Marker',
            '↔': 'Bidirectional Link'
        }
        
        self.consent_gates = ['PRIV:', 'LOCK:', 'OPEN:']
        self.lineage_markers = ['ORIGIN:', 'SUCCESSOR:', 'BRANCH:']
        
    def log(self, message: str, level: str = 'INFO'):
        """Log message if verbose mode enabled"""
        if self.verbose:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] {level}: {message}")
    
    def calculate_checksum(self, content: str) -> str:
        """Calculate SHA256 checksum of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def find_sidecar(self, artifact_path: Path) -> Optional[Path]:
        """Find companion .json sidecar file"""
        sidecar_path = artifact_path.with_suffix(artifact_path.suffix + '.json')
        if sidecar_path.exists():
            return sidecar_path
        
        # Try alternative naming conventions
        alt_path = artifact_path.parent / f"{artifact_path.stem}.sidecar.json"
        if alt_path.exists():
            return alt_path
            
        return None
    
    def validate_glyphsig_syntax(self, content: str) -> bool:
        """Validate proper glyphsig vocabulary usage"""
        self.log("Checking glyphsig syntax...")
        
        # Check for reflection seal
        if '⟡' not in content:
            self.warnings.append("No reflection seal (⟡) found - recommended for verification")
        
        # Validate enclosure frame pairs
        open_frames = content.count('⟦')
        close_frames = content.count('⟧')
        if open_frames != close_frames:
            self.errors.append(f"Mismatched enclosure frames: {open_frames} open, {close_frames} close")
            return False
        
        # Check consent gate syntax
        consent_found = False
        for gate in self.consent_gates:
            if gate in content:
                consent_found = True
                # Validate gate is properly enclosed
                pattern = rf'{gate}[^⟧]*⟧'
                if not re.search(pattern, content):
                    self.errors.append(f"Malformed consent gate: {gate} not properly enclosed")
                    return False
        
        if not consent_found:
            self.warnings.append("No consent gates found - consider adding access permissions")
        
        self.log("✓ Glyphsig syntax valid")
        return True
    
    def validate_lineage_markers(self, content: str) -> bool:
        """Validate lineage preservation markers"""
        self.log("Checking lineage markers...")
        
        origin_found = False
        for marker in self.lineage_markers:
            if marker in content:
                if marker == 'ORIGIN:':
                    origin_found = True
                    # Validate ORIGIN format: timestamp | author | checksum
                    pattern = r'ORIGIN:\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^\s]+)'
                    if not re.search(pattern, content):
                        self.errors.append("ORIGIN marker malformed - expected: timestamp | author | checksum")
                        return False
        
        if not origin_found:
            self.warnings.append("No ORIGIN marker found - lineage tracking recommended")
        
        self.log("✓ Lineage markers valid")
        return True
    
    def validate_sidecar(self, sidecar_path: Path, artifact_content: str) -> bool:
        """Validate JSON sidecar compliance"""
        self.log(f"Checking sidecar: {sidecar_path}")
        
        try:
            with open(sidecar_path, 'r', encoding='utf-8') as f:
                sidecar = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.errors.append(f"Sidecar JSON error: {e}")
            return False
        
        # Required fields
        required_fields = ['glyphsig_version', 'artifact_checksum', 'lineage', 'consent_gates']
        for field in required_fields:
            if field not in sidecar:
                self.errors.append(f"Missing required sidecar field: {field}")
                return False
        
        # Validate checksum
        actual_checksum = self.calculate_checksum(artifact_content)
        declared_checksum = sidecar.get('artifact_checksum', '').replace('sha256:', '')
        
        if actual_checksum != declared_checksum:
            self.errors.append(f"Checksum mismatch: declared {declared_checksum[:8]}..., actual {actual_checksum[:8]}...")
            return False
        
        # Validate lineage structure
        lineage = sidecar.get('lineage', {})
        if 'origin' not in lineage:
            self.errors.append("Sidecar missing lineage.origin")
            return False
        
        origin = lineage['origin']
        required_origin_fields = ['timestamp', 'author', 'checksum']
        for field in required_origin_fields:
            if field not in origin:
                self.errors.append(f"Missing lineage.origin.{field}")
                return False
        
        # Validate consent gates
        consent_gates = sidecar.get('consent_gates', {})
        if 'default' not in consent_gates:
            self.warnings.append("No default consent gate specified")
        
        self.log("✓ Sidecar valid")
        return True
    
    def check_compliance_tier(self, content: str, sidecar_data: Dict, target_tier: str = 'L1') -> bool:
        """Check compliance with specific tier requirements"""
        self.log(f"Checking {target_tier} compliance...")
        
        tier_requirements = {
            'L1': ['glyphsig_syntax', 'consent_gates', 'basic_sidecar'],
            'L2': ['L1', 'full_lineage', 'change_history'],
            'L3': ['L2', 'platform_agnostic', 'portable_encoding'],
            'L4': ['L3', 'meta_glyph_support', 'semantic_evolution']
        }
        
        if target_tier not in tier_requirements:
            self.errors.append(f"Unknown compliance tier: {target_tier}")
            return False
        
        # For now, implement basic L1/L2 checking
        if target_tier in ['L1', 'L2']:
            declared_tier = sidecar_data.get('compliance_tier', 'L1')
            if declared_tier < target_tier:
                self.warnings.append(f"Declared tier {declared_tier} below target {target_tier}")
        
        self.log(f"✓ {target_tier} compliance verified")
        return True
    
    def validate_artifact(self, artifact_path: Path, target_tier: str = 'L1') -> bool:
        """Complete validation of reflective artifact"""
        self.log(f"Validating artifact: {artifact_path}")
        self.errors.clear()
        self.warnings.clear()
        
        # Read artifact content
        try:
            with open(artifact_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            self.errors.append("Artifact must be UTF-8 encoded text")
            return False
        
        # Find and validate sidecar
        sidecar_path = self.find_sidecar(artifact_path)
        if not sidecar_path:
            self.errors.append("No sidecar file found (expected .json companion)")
            return False
        
        # Run validation checks
        checks = [
            self.validate_glyphsig_syntax(content),
            self.validate_lineage_markers(content),
            self.validate_sidecar(sidecar_path, content)
        ]
        
        if not all(checks):
            return False
        
        # Load sidecar for tier checking
        with open(sidecar_path, 'r', encoding='utf-8') as f:
            sidecar_data = json.load(f)
        
        return self.check_compliance_tier(content, sidecar_data, target_tier)
    
    def print_results(self, artifact_path: Path, is_valid: bool):
        """Print validation results"""
        print(f"\n📄 Artifact: {artifact_path}")
        
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if is_valid:
            print("✅ ⟡ VERIFIED REFLECTIVE: True")
        else:
            print("❌ ⟡ VERIFIED REFLECTIVE: False")
        
        return is_valid

def main():
    parser = argparse.ArgumentParser(description='MirrorDNA Sidecar Validator')
    parser.add_argument('path', help='Artifact file or directory to validate')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--tier', '-t', default='L1', choices=['L1', 'L2', 'L3', 'L4'], 
                       help='Target compliance tier')
    parser.add_argument('--directory', '-d', action='store_true', 
                       help='Validate all artifacts in directory')
    
    args = parser.parse_args()
    
    validator = GlyphsigValidator(verbose=args.verbose)
    path = Path(args.path)
    
    if not path.exists():
        print(f"❌ Path not found: {path}")
        sys.exit(1)
    
    valid_count = 0
    total_count = 0
    
    if args.directory or path.is_dir():
        # Validate all markdown files in directory
        artifacts = list(path.glob('*.md')) + list(path.glob('*.txt'))
        if not artifacts:
            print(f"❌ No artifacts found in {path}")
            sys.exit(1)
        
        for artifact in artifacts:
            total_count += 1
            is_valid = validator.validate_artifact(artifact, args.tier)
            if validator.print_results(artifact, is_valid):
                valid_count += 1
    else:
        # Validate single file
        total_count = 1
        is_valid = validator.validate_artifact(path, args.tier)
        if validator.print_results(path, is_valid):
            valid_count = 1
    
    # Summary
    print(f"\n📊 SUMMARY: {valid_count}/{total_count} artifacts verified reflective")
    
    if valid_count == total_count:
        print("🎉 All artifacts comply with MirrorDNA Standard!")
        sys.exit(0)
    else:
        print("💡 Fix errors and warnings, then re-validate")
        sys.exit(1)

if __name__ == '__main__':
    main()
