#!/usr/bin/env python3
"""
MirrorDNA Meta-Cognition System

VaultID: AMOS://MirrorDNA-Standard/Tools/MetaCognition/v1.0
GlyphSig: ⟡⟦META⟧ · ⟡⟦WISDOM⟧ · ⟡⟦ETHICS⟧
Predecessor: None (Initial Release)
Successor: TBD

CONSTITUTIONAL STATUS:
Enforceability: RECOMMENDED
Verifiability: MANUAL + HYBRID
Adoption: EXTENDED
Truth-State: [Fact - Governance Framework]

Meta-Cognitive Assessment Framework
====================================

Provides cross-domain insights, ethical assessment, and wisdom gates
for MirrorDNA constitutional development.

Wisdom Gates:
- Legal implications assessment
- Philosophical ambiguity detection
- Implementation feasibility analysis
- Ethical impact evaluation
- Cross-domain coherence checking

Use when:
- Defining new constitutional principles
- Evaluating implementation proposals
- Assessing philosophical implications
- Making architectural decisions
"""

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass


class WisdomGate(Enum):
    """Wisdom gate categories"""
    LEGAL = "legal"
    PHILOSOPHICAL = "philosophical"
    TECHNICAL = "technical"
    ETHICAL = "ethical"
    SOCIAL = "social"


class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Decision(Enum):
    """Wisdom gate decisions"""
    APPROVE = "approve"
    APPROVE_WITH_CONDITIONS = "approve_with_conditions"
    REVIEW_REQUIRED = "review_required"
    REJECT = "reject"


@dataclass
class WisdomGateAssessment:
    """Assessment result from a wisdom gate"""
    gate: WisdomGate
    risk_level: RiskLevel
    decision: Decision
    findings: List[str]
    recommendations: List[str]
    reasoning: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'gate': self.gate.value,
            'risk_level': self.risk_level.value,
            'decision': self.decision.value,
            'findings': self.findings,
            'recommendations': self.recommendations,
            'reasoning': self.reasoning
        }


class MetaCognitionEngine:
    """
    Meta-cognitive assessment engine for constitutional development.

    Provides multi-domain analysis and wisdom gates for:
    - New standard proposals
    - Implementation designs
    - Architectural decisions
    - Principle definitions
    """

    def __init__(self, strict_mode: bool = False):
        """
        Initialize Meta-Cognition Engine.

        Args:
            strict_mode: If True, apply stricter assessment criteria
        """
        self.strict_mode = strict_mode
        self.assessments: List[WisdomGateAssessment] = []

    def assess_proposal(
        self,
        proposal: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess a proposal through all wisdom gates.

        Args:
            proposal: Proposal dict with keys:
                - title: Proposal title
                - description: Full description
                - impact_areas: List of impacted areas
                - implementation: Implementation details
                - rationale: Reasoning

        Returns:
            Complete assessment report
        """
        self.assessments = []

        # Run all wisdom gates
        self._legal_wisdom_gate(proposal)
        self._philosophical_wisdom_gate(proposal)
        self._technical_wisdom_gate(proposal)
        self._ethical_wisdom_gate(proposal)
        self._social_wisdom_gate(proposal)

        return self._generate_assessment_report(proposal)

    def _legal_wisdom_gate(self, proposal: Dict[str, Any]) -> None:
        """
        Legal implications assessment.

        Checks:
        - Regulatory compliance
        - Intellectual property concerns
        - Liability implications
        - Terms of service impacts
        """
        findings = []
        recommendations = []
        risk_level = RiskLevel.LOW

        description = proposal.get('description', '').lower()

        # Check for legal keywords
        legal_risk_keywords = [
            'patent', 'copyright', 'trademark', 'liability', 'legal',
            'regulation', 'compliance', 'gdpr', 'privacy law',
            'data protection', 'license', 'intellectual property'
        ]

        legal_mentions = sum(
            1 for keyword in legal_risk_keywords
            if keyword in description
        )

        if legal_mentions > 0:
            findings.append(f"Legal-related terms found ({legal_mentions} mentions)")
            risk_level = RiskLevel.MEDIUM

        if legal_mentions > 3:
            risk_level = RiskLevel.HIGH
            recommendations.append("Consult legal counsel before implementation")

        # Check for data handling
        if any(term in description for term in ['personal data', 'user data', 'privacy']):
            findings.append("Proposal involves data handling")
            recommendations.append("Review GDPR and privacy compliance requirements")
            risk_level = RiskLevel.MEDIUM

        # Check for terms of service changes
        if 'terms' in description or 'service agreement' in description:
            findings.append("May require ToS updates")
            recommendations.append("Review and update terms of service")

        # Determine decision
        if risk_level == RiskLevel.CRITICAL or risk_level == RiskLevel.HIGH:
            decision = Decision.REVIEW_REQUIRED
        elif risk_level == RiskLevel.MEDIUM:
            decision = Decision.APPROVE_WITH_CONDITIONS
        else:
            decision = Decision.APPROVE

        reasoning = (
            f"Legal assessment completed. Risk level: {risk_level.value}. "
            f"Found {legal_mentions} legal-related mentions."
        )

        assessment = WisdomGateAssessment(
            gate=WisdomGate.LEGAL,
            risk_level=risk_level,
            decision=decision,
            findings=findings or ["No significant legal concerns identified"],
            recommendations=recommendations or ["Proceed with standard legal review"],
            reasoning=reasoning
        )

        self.assessments.append(assessment)

    def _philosophical_wisdom_gate(self, proposal: Dict[str, Any]) -> None:
        """
        Philosophical coherence assessment.

        Checks:
        - Alignment with core principles
        - Conceptual clarity
        - Philosophical consistency
        - Ontological soundness
        """
        findings = []
        recommendations = []
        risk_level = RiskLevel.LOW

        description = proposal.get('description', '')

        # Check principle alignment
        principles = [
            'reflection over prediction',
            'presence over productivity',
            'symbolic continuity',
            'trust by design',
            'explicit uncertainty'
        ]

        mentioned_principles = [
            p for p in principles
            if p in description.lower()
        ]

        if mentioned_principles:
            findings.append(
                f"Aligns with principles: {', '.join(mentioned_principles)}"
            )
        else:
            findings.append("No explicit principle alignment stated")
            recommendations.append(
                "Clarify alignment with MirrorDNA core principles"
            )
            risk_level = RiskLevel.MEDIUM

        # Check for philosophical ambiguity
        ambiguity_markers = [
            'might be', 'could be', 'possibly', 'unclear',
            'ambiguous', 'vague', 'uncertain about'
        ]

        has_ambiguity = any(
            marker in description.lower()
            for marker in ambiguity_markers
        )

        if has_ambiguity:
            findings.append("Philosophical ambiguity detected")
            recommendations.append(
                "Clarify philosophical intent and resolve ambiguities"
            )
            risk_level = RiskLevel.MEDIUM

        # Check for sovereignty implications
        if 'sovereignty' in description.lower() or 'vault ownership' in description.lower():
            findings.append("Impacts user sovereignty")
            recommendations.append(
                "Ensure sovereignty principles are maintained"
            )

        # Determine decision
        if risk_level == RiskLevel.HIGH:
            decision = Decision.REVIEW_REQUIRED
        elif risk_level == RiskLevel.MEDIUM:
            decision = Decision.APPROVE_WITH_CONDITIONS
        else:
            decision = Decision.APPROVE

        reasoning = (
            f"Philosophical assessment completed. "
            f"Principles mentioned: {len(mentioned_principles)}. "
            f"Ambiguity detected: {has_ambiguity}."
        )

        assessment = WisdomGateAssessment(
            gate=WisdomGate.PHILOSOPHICAL,
            risk_level=risk_level,
            decision=decision,
            findings=findings,
            recommendations=recommendations or ["Philosophical foundation is sound"],
            reasoning=reasoning
        )

        self.assessments.append(assessment)

    def _technical_wisdom_gate(self, proposal: Dict[str, Any]) -> None:
        """
        Technical feasibility assessment.

        Checks:
        - Implementation complexity
        - Technical dependencies
        - Performance implications
        - Scalability concerns
        """
        findings = []
        recommendations = []
        risk_level = RiskLevel.LOW

        implementation = proposal.get('implementation', '')

        # Check for complexity markers
        complexity_markers = [
            'complex', 'difficult', 'challenging', 'advanced',
            'sophisticated', 'intricate'
        ]

        complexity_score = sum(
            1 for marker in complexity_markers
            if marker in implementation.lower()
        )

        if complexity_score > 2:
            findings.append(f"High implementation complexity (score: {complexity_score})")
            risk_level = RiskLevel.MEDIUM
            recommendations.append("Break down into smaller, manageable components")

        # Check for dependencies
        dependency_markers = [
            'depends on', 'requires', 'needs', 'relies on',
            'prerequisite', 'dependency'
        ]

        has_dependencies = any(
            marker in implementation.lower()
            for marker in dependency_markers
        )

        if has_dependencies:
            findings.append("External dependencies identified")
            recommendations.append("Document all dependencies and verify availability")

        # Check for performance concerns
        performance_markers = [
            'performance', 'speed', 'latency', 'throughput',
            'scalability', 'efficiency'
        ]

        has_performance_concerns = any(
            marker in implementation.lower()
            for marker in performance_markers
        )

        if has_performance_concerns:
            findings.append("Performance implications noted")
            recommendations.append("Conduct performance testing and benchmarking")

        # Check for testing mentions
        has_testing = 'test' in implementation.lower()

        if not has_testing and len(implementation) > 100:
            findings.append("No testing strategy mentioned")
            recommendations.append("Define comprehensive testing strategy")
            risk_level = RiskLevel.MEDIUM

        # Determine decision
        if complexity_score > 4:
            decision = Decision.REVIEW_REQUIRED
            risk_level = RiskLevel.HIGH
        elif risk_level == RiskLevel.MEDIUM:
            decision = Decision.APPROVE_WITH_CONDITIONS
        else:
            decision = Decision.APPROVE

        reasoning = (
            f"Technical feasibility assessed. Complexity score: {complexity_score}. "
            f"Dependencies: {has_dependencies}. Testing: {has_testing}."
        )

        assessment = WisdomGateAssessment(
            gate=WisdomGate.TECHNICAL,
            risk_level=risk_level,
            decision=decision,
            findings=findings or ["Implementation appears technically feasible"],
            recommendations=recommendations or ["Proceed with standard development practices"],
            reasoning=reasoning
        )

        self.assessments.append(assessment)

    def _ethical_wisdom_gate(self, proposal: Dict[str, Any]) -> None:
        """
        Ethical impact assessment.

        Checks:
        - User autonomy impact
        - Privacy implications
        - Bias and fairness
        - Transparency
        - Potential for harm
        """
        findings = []
        recommendations = []
        risk_level = RiskLevel.LOW

        description = proposal.get('description', '').lower()

        # Check for privacy impact
        privacy_keywords = [
            'data collection', 'personal information', 'tracking',
            'surveillance', 'monitoring', 'privacy'
        ]

        privacy_mentions = sum(
            1 for keyword in privacy_keywords
            if keyword in description
        )

        if privacy_mentions > 0:
            findings.append("Privacy implications identified")
            recommendations.append("Conduct privacy impact assessment")
            risk_level = RiskLevel.MEDIUM

        # Check for autonomy impact
        if any(term in description for term in ['require', 'mandatory', 'forced', 'must use']):
            findings.append("May impact user autonomy")
            recommendations.append("Ensure user choice and consent mechanisms")
            risk_level = RiskLevel.MEDIUM

        # Check for bias concerns
        bias_keywords = ['bias', 'fairness', 'discrimination', 'equity']
        if any(keyword in description for keyword in bias_keywords):
            findings.append("Fairness and bias considerations noted")
            recommendations.append("Review for potential bias and ensure fairness")

        # Check for transparency
        if 'transparent' in description or 'open' in description:
            findings.append("Promotes transparency (positive)")

        # Check for harm potential
        harm_keywords = ['harm', 'damage', 'risk', 'danger', 'vulnerable']
        harm_mentions = sum(1 for keyword in harm_keywords if keyword in description)

        if harm_mentions > 1:
            findings.append("Potential for harm identified")
            recommendations.append("Implement safeguards and harm mitigation strategies")
            risk_level = RiskLevel.HIGH

        # Determine decision
        if risk_level == RiskLevel.HIGH:
            decision = Decision.REVIEW_REQUIRED
        elif risk_level == RiskLevel.MEDIUM:
            decision = Decision.APPROVE_WITH_CONDITIONS
        else:
            decision = Decision.APPROVE

        reasoning = (
            f"Ethical assessment completed. Privacy mentions: {privacy_mentions}. "
            f"Harm potential: {harm_mentions}. Risk level: {risk_level.value}."
        )

        assessment = WisdomGateAssessment(
            gate=WisdomGate.ETHICAL,
            risk_level=risk_level,
            decision=decision,
            findings=findings or ["No significant ethical concerns identified"],
            recommendations=recommendations or ["Ethical foundation appears sound"],
            reasoning=reasoning
        )

        self.assessments.append(assessment)

    def _social_wisdom_gate(self, proposal: Dict[str, Any]) -> None:
        """
        Social impact assessment.

        Checks:
        - Community impact
        - Accessibility
        - Inclusivity
        - Cultural sensitivity
        - Adoption barriers
        """
        findings = []
        recommendations = []
        risk_level = RiskLevel.LOW

        description = proposal.get('description', '').lower()
        impact_areas = proposal.get('impact_areas', [])

        # Check for accessibility
        if 'accessibility' in description or 'accessible' in description:
            findings.append("Accessibility considerations included (positive)")
        else:
            recommendations.append("Consider accessibility requirements")

        # Check for inclusivity
        inclusivity_keywords = ['inclusive', 'diversity', 'all users', 'everyone']
        if any(keyword in description for keyword in inclusivity_keywords):
            findings.append("Inclusivity considerations noted (positive)")

        # Check for adoption barriers
        barrier_keywords = [
            'requires expertise', 'technical knowledge', 'complex setup',
            'difficult to use', 'learning curve'
        ]

        has_barriers = any(keyword in description for keyword in barrier_keywords)

        if has_barriers:
            findings.append("Adoption barriers identified")
            recommendations.append("Develop onboarding and documentation to lower barriers")
            risk_level = RiskLevel.MEDIUM

        # Check community impact
        if impact_areas and len(impact_areas) > 3:
            findings.append(f"Wide community impact ({len(impact_areas)} areas)")
            recommendations.append("Gather community feedback before implementation")

        # Check for breaking changes
        if 'breaking change' in description or 'incompatible' in description:
            findings.append("Breaking changes proposed")
            recommendations.append("Provide migration path and clear communication")
            risk_level = RiskLevel.MEDIUM

        # Determine decision
        if risk_level == RiskLevel.HIGH:
            decision = Decision.REVIEW_REQUIRED
        elif risk_level == RiskLevel.MEDIUM:
            decision = Decision.APPROVE_WITH_CONDITIONS
        else:
            decision = Decision.APPROVE

        reasoning = (
            f"Social impact assessed. Adoption barriers: {has_barriers}. "
            f"Impact areas: {len(impact_areas)}."
        )

        assessment = WisdomGateAssessment(
            gate=WisdomGate.SOCIAL,
            risk_level=risk_level,
            decision=decision,
            findings=findings or ["Positive social impact expected"],
            recommendations=recommendations or ["Proceed with community engagement"],
            reasoning=reasoning
        )

        self.assessments.append(assessment)

    def _generate_assessment_report(
        self,
        proposal: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive assessment report."""

        # Calculate overall decision
        decisions = [a.decision for a in self.assessments]

        if Decision.REJECT in decisions:
            overall_decision = Decision.REJECT
        elif Decision.REVIEW_REQUIRED in decisions:
            overall_decision = Decision.REVIEW_REQUIRED
        elif Decision.APPROVE_WITH_CONDITIONS in decisions:
            overall_decision = Decision.APPROVE_WITH_CONDITIONS
        else:
            overall_decision = Decision.APPROVE

        # Calculate overall risk
        risk_scores = {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4
        }

        max_risk_score = max(risk_scores[a.risk_level] for a in self.assessments)
        overall_risk = [r for r, s in risk_scores.items() if s == max_risk_score][0]

        return {
            'proposal_title': proposal.get('title', 'Untitled'),
            'overall_decision': overall_decision.value,
            'overall_risk': overall_risk.value,
            'wisdom_gates': [a.to_dict() for a in self.assessments],
            'summary': {
                'total_findings': sum(len(a.findings) for a in self.assessments),
                'total_recommendations': sum(len(a.recommendations) for a in self.assessments),
                'gates_passed': sum(1 for a in self.assessments if a.decision == Decision.APPROVE),
                'gates_conditional': sum(1 for a in self.assessments if a.decision == Decision.APPROVE_WITH_CONDITIONS),
                'gates_review_required': sum(1 for a in self.assessments if a.decision == Decision.REVIEW_REQUIRED),
            }
        }


def assess_standard_proposal(
    title: str,
    description: str,
    implementation: str = "",
    impact_areas: List[str] = None,
    rationale: str = ""
) -> Dict[str, Any]:
    """
    Convenience function to assess a standard proposal.

    Args:
        title: Proposal title
        description: Full description
        implementation: Implementation details
        impact_areas: List of impacted areas
        rationale: Reasoning for proposal

    Returns:
        Assessment report
    """
    proposal = {
        'title': title,
        'description': description,
        'implementation': implementation,
        'impact_areas': impact_areas or [],
        'rationale': rationale
    }

    engine = MetaCognitionEngine()
    return engine.assess_proposal(proposal)


if __name__ == "__main__":
    import sys
    import json
    import argparse

    parser = argparse.ArgumentParser(description="MirrorDNA Meta-Cognition System")
    parser.add_argument('--title', required=True, help='Proposal title')
    parser.add_argument('--description', required=True, help='Proposal description')
    parser.add_argument('--implementation', default='', help='Implementation details')
    parser.add_argument('--impact', nargs='*', default=[], help='Impact areas')
    parser.add_argument('--rationale', default='', help='Rationale')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    report = assess_standard_proposal(
        title=args.title,
        description=args.description,
        implementation=args.implementation,
        impact_areas=args.impact,
        rationale=args.rationale
    )

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n⟡⟦META-COGNITIVE ASSESSMENT⟧\n")
        print(f"Proposal: {report['proposal_title']}")
        print(f"Overall Decision: {report['overall_decision'].upper()}")
        print(f"Overall Risk: {report['overall_risk'].upper()}")
        print(f"\nSummary:")
        print(f"  Total findings: {report['summary']['total_findings']}")
        print(f"  Total recommendations: {report['summary']['total_recommendations']}")
        print(f"  Gates passed: {report['summary']['gates_passed']}")
        print(f"  Gates conditional: {report['summary']['gates_conditional']}")
        print(f"  Gates requiring review: {report['summary']['gates_review_required']}")

        print(f"\nWisdom Gate Results:")
        for gate in report['wisdom_gates']:
            print(f"\n  {gate['gate'].upper()}")
            print(f"    Decision: {gate['decision']}")
            print(f"    Risk: {gate['risk_level']}")
            print(f"    Findings: {len(gate['findings'])}")
            for finding in gate['findings']:
                print(f"      - {finding}")
            if gate['recommendations']:
                print(f"    Recommendations:")
                for rec in gate['recommendations']:
                    print(f"      → {rec}")
