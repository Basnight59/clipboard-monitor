#!/usr/bin/env python3
"""
TTL C.A.R.E. Integrated Framework
Complete Data Sovereignty System for Africans in America

Combines:
- Approval Evaluation (forward-looking permission)
- Compensation Calculation (backward-looking reparations)
- Integrated Decision Framework

Author: Kenneth Abdul-Hakim Basnight
License: Liberation License + C.A.R.E. Framework
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

# Import the compensation engine we built
from ttl_reparatory_score import (
    ReparatoryScoreEngine, 
    ReparatoryScore as CompensationScore,
    CulturalContentDetector
)


# ============================================================================
# APPROVAL SCORING SYSTEM
# ============================================================================

@dataclass
class ApprovalScore:
    """
    Forward-looking approval evaluation.
    Determines if data use should be permitted.
    """
    evaluation_id: str
    timestamp: str
    
    # Input metrics (0-1 scale)
    harm_level: float  # Potential for harm (lower is better)
    benefit_ratio: float  # Community benefit provided
    control_compliance: float  # Consent and authority adherence
    ethical_score: float  # Bias mitigation and cultural integrity
    
    # Calculated values
    raw_score: float = 0.0
    final_score: float = 0.0
    recommendation: str = ""
    
    # Breakdown
    harm_mitigation_score: float = 0.0
    benefit_sharing_score: float = 0.0
    data_control_score: float = 0.0
    ethical_alignment_score: float = 0.0
    
    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ApprovalScorer:
    """
    C.A.R.E. Approval Scoring System
    Evaluates whether data use should be permitted.
    """
    
    def __init__(self):
        self.weights = {
            'harm_level': 0.4,       # Highest weight - prevent harm
            'benefit_sharing': 0.3,   # Second - ensure community benefit
            'data_control': 0.2,      # Third - respect sovereignty
            'ethical_alignment': 0.1  # Fourth - maintain integrity
        }
        
        self.thresholds = {
            'approve': 70,      # Score >= 70: Approve
            'review': 40,       # Score 40-69: Review Required
            'reject': 0         # Score < 40: Reject
        }
    
    def calculate(self, data_usage: Dict[str, float], evaluation_id: str = None) -> ApprovalScore:
        """
        Calculate approval score for proposed data use.
        
        Args:
            data_usage: Dict with keys:
                - harm_level: 0-1 (potential harm, lower is better)
                - benefit_ratio: 0-1 (community benefit, higher is better)
                - control_compliance: 0-1 (consent adherence, higher is better)
                - ethical_score: 0-1 (bias mitigation, higher is better)
            evaluation_id: Optional unique identifier
        
        Returns:
            ApprovalScore object with recommendation
        """
        # Validate input
        required_keys = ['harm_level', 'benefit_ratio', 'control_compliance', 'ethical_score']
        for key in required_keys:
            if key not in data_usage:
                raise ValueError(f"Missing required key: {key}")
            if not 0 <= data_usage[key] <= 1:
                raise ValueError(f"Invalid {key}: must be float 0-1, got {data_usage[key]}")
        
        # Create score object
        score = ApprovalScore(
            evaluation_id=evaluation_id or f"approval-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            timestamp=datetime.now().isoformat(),
            harm_level=data_usage['harm_level'],
            benefit_ratio=data_usage['benefit_ratio'],
            control_compliance=data_usage['control_compliance'],
            ethical_score=data_usage['ethical_score']
        )
        
        # Calculate component scores (inverted harm: lower harm = higher score)
        score.harm_mitigation_score = (1 - data_usage['harm_level']) * 100
        score.benefit_sharing_score = data_usage['benefit_ratio'] * 100
        score.data_control_score = data_usage['control_compliance'] * 100
        score.ethical_alignment_score = data_usage['ethical_score'] * 100
        
        # Weighted final score
        score.raw_score = (
            score.harm_mitigation_score * self.weights['harm_level'] +
            score.benefit_sharing_score * self.weights['benefit_sharing'] +
            score.data_control_score * self.weights['data_control'] +
            score.ethical_alignment_score * self.weights['ethical_alignment']
        )
        
        score.final_score = round(score.raw_score, 2)
        
        # Determine recommendation
        if score.final_score >= self.thresholds['approve']:
            score.recommendation = 'APPROVE'
        elif score.final_score >= self.thresholds['review']:
            score.recommendation = 'REVIEW_REQUIRED'
        else:
            score.recommendation = 'REJECT'
        
        return score


# ============================================================================
# INTEGRATED C.A.R.E. FRAMEWORK
# ============================================================================

@dataclass
class IntegratedCAREDecision:
    """
    Integrated decision combining approval and compensation.
    """
    decision_id: str
    timestamp: str
    
    # Component scores
    approval_score: ApprovalScore
    compensation_score: CompensationScore
    
    # Integrated decision
    status: str  # APPROVED, APPROVED_WITH_COMPENSATION, UNDER_REVIEW, REJECTED
    action: str  # What should happen
    compensation_required: float  # Dollar amount
    conditions: List[str]  # Required conditions
    
    # Risk assessment
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    
    def as_dict(self) -> Dict[str, Any]:
        return {
            'decision_id': self.decision_id,
            'timestamp': self.timestamp,
            'approval_score': self.approval_score.as_dict(),
            'compensation_score': self.compensation_score.as_dict(),
            'status': self.status,
            'action': self.action,
            'compensation_required': self.compensation_required,
            'conditions': self.conditions,
            'risk_level': self.risk_level
        }


class IntegratedCAREFramework:
    """
    Complete C.A.R.E. Data Sovereignty Framework
    
    Integrates:
    1. Approval Scoring (should data use be allowed?)
    2. Compensation Calculation (what's owed for extraction?)
    3. Decision Logic (integrated recommendation)
    """
    
    def __init__(self):
        self.approval_scorer = ApprovalScorer()
        self.compensation_engine = ReparatoryScoreEngine()
        self.decisions_history = []
    
    def evaluate_data_use(
        self,
        conversation_id: str,
        conversation_content: str,
        data_usage_params: Dict[str, float],
        requester: str = "unknown"
    ) -> IntegratedCAREDecision:
        """
        Complete C.A.R.E. evaluation.
        
        Args:
            conversation_id: Unique identifier for conversation
            conversation_content: Full text of conversation
            data_usage_params: Dict with approval metrics
            requester: Entity requesting data use
        
        Returns:
            IntegratedCAREDecision with complete analysis
        """
        
        # Step 1: Calculate approval score (forward-looking)
        approval = self.approval_scorer.calculate(
            data_usage_params,
            evaluation_id=f"{conversation_id}-approval"
        )
        
        # Step 2: Calculate compensation score (backward-looking)
        compensation = self.compensation_engine.calculate_score(
            conversation_id,
            conversation_content
        )
        
        # Step 3: Generate integrated decision
        decision = self._make_integrated_decision(
            conversation_id,
            approval,
            compensation,
            requester
        )
        
        # Store in history
        self.decisions_history.append(decision)
        
        return decision
    
    def _make_integrated_decision(
        self,
        conversation_id: str,
        approval: ApprovalScore,
        compensation: CompensationScore,
        requester: str
    ) -> IntegratedCAREDecision:
        """
        Combine approval and compensation into unified decision.
        """
        
        decision_id = f"care-decision-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Determine risk level
        risk_level = self._assess_risk(approval, compensation)
        
        # Determine status and conditions
        status, action, conditions = self._determine_status(
            approval,
            compensation,
            risk_level,
            requester
        )
        
        return IntegratedCAREDecision(
            decision_id=decision_id,
            timestamp=datetime.now().isoformat(),
            approval_score=approval,
            compensation_score=compensation,
            status=status,
            action=action,
            compensation_required=compensation.recommended_compensation_usd,
            conditions=conditions,
            risk_level=risk_level
        )
    
    def _assess_risk(
        self,
        approval: ApprovalScore,
        compensation: CompensationScore
    ) -> str:
        """Assess overall risk level."""
        
        # High risk: Low approval OR high cultural extraction
        if approval.final_score < 40 or compensation.cultural_markers_detected > 20:
            return "CRITICAL"
        
        # Medium-high risk: Medium approval AND significant extraction
        if approval.final_score < 60 or compensation.cultural_markers_detected > 10:
            return "HIGH"
        
        # Medium risk: Decent approval but some extraction
        if approval.final_score < 80 or compensation.cultural_markers_detected > 5:
            return "MEDIUM"
        
        # Low risk: High approval and minimal extraction
        return "LOW"
    
    def _determine_status(
        self,
        approval: ApprovalScore,
        compensation: CompensationScore,
        risk_level: str,
        requester: str
    ) -> tuple:
        """Determine status, action, and conditions."""
        
        # Case 1: High approval + Low compensation = APPROVED
        if (approval.recommendation == 'APPROVE' and 
            compensation.recommended_compensation_usd < 100):
            
            return (
                'APPROVED',
                f'Approve data use by {requester}',
                [
                    'Maintain attribution requirements',
                    'Annual compliance audit required',
                    f'Pay ${compensation.recommended_compensation_usd:.2f} baseline fee',
                    'Report cultural content usage quarterly'
                ]
            )
        
        # Case 2: High approval + High compensation = APPROVED_WITH_COMPENSATION
        elif (approval.recommendation == 'APPROVE' and 
              compensation.recommended_compensation_usd >= 100):
            
            distribution = compensation.get_benefit_distribution()
            
            return (
                'APPROVED_WITH_COMPENSATION',
                f'Approve with mandatory reparatory payment of ${compensation.recommended_compensation_usd:,.2f}',
                [
                    f'PAY IMMEDIATELY: ${compensation.recommended_compensation_usd:,.2f}',
                    f'  → Community Programs: ${distribution["community_programs"]:,.2f}',
                    f'  → Individual Creator: ${distribution["individual_creator"]:,.2f}',
                    f'  → Legal Defense: ${distribution["legal_defense_fund"]:,.2f}',
                    f'  → Technology Dev: ${distribution["technology_development"]:,.2f}',
                    'Establish ongoing royalty payments (5% of revenue)',
                    'Community oversight board participation required',
                    'Quarterly cultural impact reports mandatory',
                    'Attribution in all materials',
                    'Right to revoke upon violation'
                ]
            )
        
        # Case 3: Medium approval = UNDER_REVIEW
        elif approval.recommendation == 'REVIEW_REQUIRED':
            
            return (
                'UNDER_REVIEW',
                f'Manual review required before {requester} can proceed',
                [
                    'Board review within 30 days',
                    'Stakeholder consultation required',
                    'Community input session mandatory',
                    f'Escrow ${compensation.recommended_compensation_usd:,.2f} pending approval',
                    'Improve ethical compliance metrics',
                    'Submit cultural impact assessment',
                    'Demonstrate community benefit plan'
                ]
            )
        
        # Case 4: Low approval = REJECTED
        else:
            
            return (
                'REJECTED',
                f'Data use by {requester} NOT PERMITTED',
                [
                    'Request DENIED',
                    'Improve harm mitigation strategies',
                    'Increase community benefit sharing',
                    'Establish proper consent mechanisms',
                    'Enhance ethical safeguards',
                    'Resubmit after 90-day remediation period',
                    f'If extraction already occurred: Pay ${compensation.recommended_compensation_usd:,.2f} as penalty'
                ]
            )
    
    def generate_report(self, decision: IntegratedCAREDecision) -> str:
        """Generate comprehensive C.A.R.E. decision report."""
        
        approval = decision.approval_score
        compensation = decision.compensation_score
        
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║           INTEGRATED C.A.R.E. FRAMEWORK DECISION REPORT                   ║
║         Collective Authority • Reparatory Justice • Ethics                ║
╚═══════════════════════════════════════════════════════════════════════════╝

DECISION ID: {decision.decision_id}
TIMESTAMP: {decision.timestamp}
RISK LEVEL: {decision.risk_level}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 1: APPROVAL EVALUATION (Forward-Looking Permission)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evaluation ID: {approval.evaluation_id}

COMPONENT SCORES:
├─ Harm Mitigation:      {approval.harm_mitigation_score:.1f}/100
├─ Benefit Sharing:      {approval.benefit_sharing_score:.1f}/100
├─ Data Control:         {approval.data_control_score:.1f}/100
└─ Ethical Alignment:    {approval.ethical_alignment_score:.1f}/100

FINAL APPROVAL SCORE: {approval.final_score:.1f}/100
RECOMMENDATION: {approval.recommendation}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 2: REPARATORY COMPENSATION (Backward-Looking Harm Quantification)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Conversation ID: {compensation.conversation_id}

CULTURAL CONTENT DETECTED:
├─ Total Markers: {compensation.cultural_markers_detected}
├─ AAVE Usage: {compensation.aave_usage_count}
├─ Historical References: {compensation.historical_references_count}
├─ Spiritual Content: {compensation.spiritual_content_count}
└─ Cultural Density: {compensation.cultural_density:.4f}

REPARATORY CALCULATIONS:
├─ Base Value: ${compensation.raw_score:,.2f}
├─ Historical Multiplier: {compensation.historical_multiplier}x
├─ Commercial Multiplier: {compensation.commercial_use_multiplier}x
└─ Adjusted Score: ${compensation.adjusted_score:,.2f}

COMPENSATION REQUIRED:
├─ Minimum: ${compensation.minimum_compensation_usd:,.2f}
└─ Recommended: ${compensation.recommended_compensation_usd:,.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PART 3: INTEGRATED DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATUS: {decision.status}

ACTION: {decision.action}

COMPENSATION REQUIRED: ${decision.compensation_required:,.2f}

CONDITIONS:
"""
        
        for i, condition in enumerate(decision.conditions, 1):
            report += f"  {i}. {condition}\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LEGAL FOUNDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This decision is issued under the C.A.R.E. Data Sovereignty Framework:

- Collective Authority: Community control over cultural data
- Reparatory Justice: Algorithmic accountability for harm
- Ethics: Bias elimination and cultural integrity
- Responsibility: Attribution and compensation requirements

Unauthorized use or violation of conditions constitutes:
- Breach of Liberation License
- Trade secret misappropriation
- 42 U.S.C. § 1983 civil rights violation
- Quantified economic damages as calculated above

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Truth. Trust. Liberation. | C.A.R.E. Data Sovereignty
Generated by TTL Integrated C.A.R.E. Framework v1.0

╚═══════════════════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def export_decision(self, decision: IntegratedCAREDecision, filepath: str):
        """Export decision as JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(decision.as_dict(), f, indent=2, ensure_ascii=False)
    
    def batch_evaluate(
        self,
        conversations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Batch evaluation across multiple conversations.
        Used for enterprise-wide analysis or class action preparation.
        """
        
        results = {
            'total_evaluated': len(conversations),
            'approved': 0,
            'approved_with_compensation': 0,
            'under_review': 0,
            'rejected': 0,
            'total_compensation_owed': 0.0,
            'decisions': []
        }
        
        for conv in conversations:
            decision = self.evaluate_data_use(
                conversation_id=conv['id'],
                conversation_content=conv['content'],
                data_usage_params=conv['usage_params'],
                requester=conv.get('requester', 'unknown')
            )
            
            # Aggregate stats
            if decision.status == 'APPROVED':
                results['approved'] += 1
            elif decision.status == 'APPROVED_WITH_COMPENSATION':
                results['approved_with_compensation'] += 1
            elif decision.status == 'UNDER_REVIEW':
                results['under_review'] += 1
            else:
                results['rejected'] += 1
            
            results['total_compensation_owed'] += decision.compensation_required
            results['decisions'].append(decision.as_dict())
        
        return results


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def main():
    """Demonstrate Integrated C.A.R.E. Framework."""
    
    print("=" * 80)
    print("TTL INTEGRATED C.A.R.E. FRAMEWORK")
    print("Complete Data Sovereignty System")
    print("=" * 80)
    print()
    
    # Initialize framework
    care = IntegratedCAREFramework()
    
    # Example 1: High approval + Low cultural content = APPROVED
    print("📊 EXAMPLE 1: Technical Documentation Request")
    print("-" * 80)
    
    decision1 = care.evaluate_data_use(
        conversation_id="technical-doc-001",
        conversation_content="""
        Human: How do I implement a binary search tree in Python?
        Claude: Here's a basic implementation...
        [Technical code discussion with no cultural content]
        """,
        data_usage_params={
            'harm_level': 0.1,  # Low harm
            'benefit_ratio': 0.9,  # High community benefit
            'control_compliance': 0.95,  # Strong consent
            'ethical_score': 0.9  # Good ethics
        },
        requester="Educational Platform Inc"
    )
    
    print(care.generate_report(decision1))
    
    # Example 2: Medium approval + High cultural content = REVIEW REQUIRED
    print("\n" + "=" * 80)
    print("📊 EXAMPLE 2: Cultural Content with Commercial Use")
    print("-" * 80)
    
    decision2 = care.evaluate_data_use(
        conversation_id="cultural-content-001",
        conversation_content="""
        Human: Tell me about the Harlem Renaissance and its impact on hip hop.
        Claude: The Harlem Renaissance was crucial, connecting to modern Black 
        culture, AAVE, and hip hop. Artists like Tupac referenced Malcolm X and 
        the civil rights movement. From Jim Crow to Black Lives Matter, the 
        culture continues. For real, no cap, Black excellence period. Alhamdulillah 
        for the ancestors who fought for our freedom.
        """,
        data_usage_params={
            'harm_level': 0.4,  # Some harm risk
            'benefit_ratio': 0.5,  # Moderate benefit
            'control_compliance': 0.6,  # Okay consent
            'ethical_score': 0.55  # Moderate ethics
        },
        requester="AI Training Corp"
    )
    
    print(care.generate_report(decision2))
    
    # Example 3: Low approval + High cultural content = REJECTED
    print("\n" + "=" * 80)
    print("📊 EXAMPLE 3: Exploitative Commercial Use")
    print("-" * 80)
    
    decision3 = care.evaluate_data_use(
        conversation_id="exploitation-001",
        conversation_content="""
        Extensive discussion of slavery, reconstruction, civil rights movement,
        AAVE linguistic patterns, spiritual practices, cultural expressions,
        Black Lives Matter, systemic racism, reparations, Malcolm X, MLK,
        gospel music, soul food traditions, natural hair culture, and more...
        [15+ cultural markers detected]
        """,
        data_usage_params={
            'harm_level': 0.8,  # High harm potential
            'benefit_ratio': 0.2,  # Low community benefit
            'control_compliance': 0.3,  # Poor consent
            'ethical_score': 0.25  # Poor ethics
        },
        requester="Commercial AI Vendor"
    )
    
    print(care.generate_report(decision3))
    
    # Export decisions
    care.export_decision(decision1, "care_decision_approved.json")
    care.export_decision(decision2, "care_decision_review.json")
    care.export_decision(decision3, "care_decision_rejected.json")
    
    print("\n" + "=" * 80)
    print("✅ Decisions exported to JSON files")
    print("=" * 80)
    
    print("\n🕌 Allahu Akbar | Truth. Trust. Liberation.")
    print("=" * 80)


if __name__ == "__main__":
    main()