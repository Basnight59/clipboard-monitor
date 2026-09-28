#!/usr/bin/env python3
"""
TTL Reparatory Score Engine
C.A.R.E. Data Sovereignty for Africans in America

Calculates fair compensation for cultural data extraction and AI training.
Implements economic justice through algorithmic accountability.

Author: Kenneth Abdul-Hakim Basnight
License: Liberation License + C.A.R.E. Framework
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import json


# ============================================================================
# CULTURAL CONTENT DETECTION
# ============================================================================

class CulturalContentDetector:
    """
    Detects African American cultural content in conversations.
    Identifies AAVE, historical references, spiritual content, and cultural markers.
    """
    
    # African American Vernacular English (AAVE) markers
    AAVE_PATTERNS = [
        r'\bfinna\b', r'\bgonna\b', r'\bwanna\b',
        r'\bain\'t\b', r'\bdon\'t\b', r'\bcan\'t\b',
        r'\by\'all\b', r'\ball y\'all\b',
        r'\bashy\b', r'\bextra\b', r'\blit\b', r'\bfam\b',
        r'\bdeadass\b', r'\bno cap\b', r'\bon god\b',
        r'\bfacts\b', r'\bperiod\b', r'\bperiodT\b',
        r'\bthe tea\b', r'\bspill\b', r'\bshade\b',
        r'\bslay\b', r'\byaas\b', r'\bokurrr\b',
        r'\bwoke\b', r'\bcancel\b', r'\bvibe check\b',
    ]
    
    # Historical and cultural references
    HISTORICAL_MARKERS = [
        # Civil Rights Era
        r'\bMLK\b', r'\bMartin Luther King\b', r'\bMalcolm X\b',
        r'\bRosa Parks\b', r'\bselma\b', r'\bmontgomery\b',
        r'\bJim Crow\b', r'\bsegregation\b', r'\bcivil rights\b',
        
        # Slavery and Post-Slavery
        r'\bslavery\b', r'\benslavement\b', r'\bmiddle passage\b',
        r'\bplantation\b', r'\breconstruction\b', r'\bfreedom\b',
        r'\bemancipation\b', r'\bJuneteenth\b', r'\breparations\b',
        
        # Cultural Movements
        r'\bHarlem Renaissance\b', r'\bBlack Power\b', r'\bBlack Panther\b',
        r'\bBLM\b', r'\bBlack Lives Matter\b', r'\bSay Her Name\b',
        
        # Cultural Icons
        r'\bTupac\b', r'\bBiggie\b', r'\bNina Simone\b',
        r'\bJames Baldwin\b', r'\bMaya Angelou\b', r'\bToni Morrison\b',
    ]
    
    # Spiritual and Religious content
    SPIRITUAL_MARKERS = [
        r'\bAllahu Akbar\b', r'\bInsha Allah\b', r'\bMasha Allah\b',
        r'\bSubhan Allah\b', r'\bAlhamdulillah\b',
        r'\bAME Church\b', r'\bBaptist\b', r'\bgospel\b',
        r'\bpraise\b', r'\bhallelujah\b', r'\bamen\b',
        r'\bspiritual\b', r'\bancestral\b', r'\blibation\b',
    ]
    
    # Cultural expressions
    CULTURAL_EXPRESSIONS = [
        r'\bthe culture\b', r'\bfor the culture\b',
        r'\bBlack excellence\b', r'\bBlack joy\b', r'\bBlack girl magic\b',
        r'\bmelanin\b', r'\bnatural hair\b', r'\blocs\b', r'\bbraids\b',
        r'\bsoul food\b', r'\bcollard greens\b', r'\bcornbread\b',
        r'\bhip hop\b', r'\bjazz\b', r'\bblues\b', r'\bR&B\b', r'\bgospel\b',
    ]
    
    def __init__(self):
        self.aave_patterns = [re.compile(p, re.IGNORECASE) for p in self.AAVE_PATTERNS]
        self.historical_patterns = [re.compile(p, re.IGNORECASE) for p in self.HISTORICAL_MARKERS]
        self.spiritual_patterns = [re.compile(p, re.IGNORECASE) for p in self.SPIRITUAL_MARKERS]
        self.cultural_patterns = [re.compile(p, re.IGNORECASE) for p in self.CULTURAL_EXPRESSIONS]
    
    def detect_aave(self, text: str) -> Tuple[int, List[str]]:
        """Detect AAVE usage and return count + matches."""
        matches = []
        for pattern in self.aave_patterns:
            found = pattern.findall(text)
            matches.extend(found)
        return len(matches), matches
    
    def detect_historical_content(self, text: str) -> Tuple[int, List[str]]:
        """Detect historical/cultural references."""
        matches = []
        for pattern in self.historical_patterns:
            found = pattern.findall(text)
            matches.extend(found)
        return len(matches), matches
    
    def detect_spiritual_content(self, text: str) -> Tuple[int, List[str]]:
        """Detect spiritual/religious content."""
        matches = []
        for pattern in self.spiritual_patterns:
            found = pattern.findall(text)
            matches.extend(found)
        return len(matches), matches
    
    def detect_cultural_expressions(self, text: str) -> Tuple[int, List[str]]:
        """Detect cultural expressions and references."""
        matches = []
        for pattern in self.cultural_patterns:
            found = pattern.findall(text)
            matches.extend(found)
        return len(matches), matches
    
    def analyze_content(self, text: str) -> Dict[str, Any]:
        """Complete cultural content analysis."""
        aave_count, aave_matches = self.detect_aave(text)
        hist_count, hist_matches = self.detect_historical_content(text)
        spirit_count, spirit_matches = self.detect_spiritual_content(text)
        cultural_count, cultural_matches = self.detect_cultural_expressions(text)
        
        total_markers = aave_count + hist_count + spirit_count + cultural_count
        
        return {
            'total_cultural_markers': total_markers,
            'aave_usage': {
                'count': aave_count,
                'matches': aave_matches[:10]  # First 10 examples
            },
            'historical_references': {
                'count': hist_count,
                'matches': hist_matches[:10]
            },
            'spiritual_content': {
                'count': spirit_count,
                'matches': spirit_matches[:10]
            },
            'cultural_expressions': {
                'count': cultural_count,
                'matches': cultural_matches[:10]
            },
            'cultural_density': total_markers / max(len(text.split()), 1),  # Markers per word
            'requires_care_protection': total_markers > 0
        }


# ============================================================================
# REPARATORY SCORE CALCULATION
# ============================================================================

@dataclass
class ReparatoryScore:
    """
    Reparatory Score calculation result.
    Quantifies economic justice requirements for cultural data use.
    """
    conversation_id: str
    timestamp: str
    
    # Cultural content metrics
    cultural_markers_detected: int
    aave_usage_count: int
    historical_references_count: int
    spiritual_content_count: int
    cultural_density: float
    
    # Economic calculations
    base_value_per_marker: float = 10.00  # $10 per cultural marker
    historical_multiplier: float = 1.0     # Increased for historical trauma content
    commercial_use_multiplier: float = 1.0 # Increased if commercial use detected
    
    # Calculated values
    raw_score: float = 0.0
    adjusted_score: float = 0.0
    minimum_compensation_usd: float = 0.0
    recommended_compensation_usd: float = 0.0
    
    # Benefit distribution
    community_benefit_percentage: float = 0.30  # 30% to community programs
    individual_compensation_percentage: float = 0.40  # 40% to data creator
    legal_defense_fund_percentage: float = 0.20  # 20% to legal advocacy
    technology_development_percentage: float = 0.10  # 10% to TTL/C.A.R.E. development
    
    # Attribution
    requires_attribution: bool = False
    requires_consent: bool = False
    requires_audit_trail: bool = False
    
    def calculate_scores(self):
        """Calculate all reparatory score values."""
        # Base score: $10 per cultural marker
        self.raw_score = self.cultural_markers_detected * self.base_value_per_marker
        
        # Apply multipliers
        if self.historical_references_count > 5:
            self.historical_multiplier = 2.0  # Double for significant historical content
        
        if self.aave_usage_count > 10:
            self.commercial_use_multiplier = 1.5  # 50% increase for heavy AAVE use
        
        # Adjusted score
        self.adjusted_score = self.raw_score * self.historical_multiplier * self.commercial_use_multiplier
        
        # Compensation calculations
        self.minimum_compensation_usd = self.adjusted_score
        self.recommended_compensation_usd = self.adjusted_score * 1.5  # 50% premium recommended
        
        # Protection requirements
        if self.cultural_markers_detected > 0:
            self.requires_attribution = True
            self.requires_consent = True
            self.requires_audit_trail = True
    
    def get_benefit_distribution(self) -> Dict[str, float]:
        """Calculate benefit distribution amounts."""
        return {
            'community_programs': self.recommended_compensation_usd * self.community_benefit_percentage,
            'individual_creator': self.recommended_compensation_usd * self.individual_compensation_percentage,
            'legal_defense_fund': self.recommended_compensation_usd * self.legal_defense_fund_percentage,
            'technology_development': self.recommended_compensation_usd * self.technology_development_percentage,
            'total': self.recommended_compensation_usd
        }
    
    def as_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/export."""
        return asdict(self)


# ============================================================================
# REPARATORY SCORE ENGINE
# ============================================================================

class ReparatoryScoreEngine:
    """
    Main engine for C.A.R.E. Data Sovereignty reparatory calculations.
    Implements economic justice through algorithmic accountability.
    """
    
    def __init__(self):
        self.detector = CulturalContentDetector()
        self.scores_history = []
    
    def calculate_score(self, conversation_id: str, content: str) -> ReparatoryScore:
        """
        Calculate reparatory score for a conversation.
        
        Args:
            conversation_id: Unique identifier for the conversation
            content: Full conversation text
            
        Returns:
            ReparatoryScore object with complete calculations
        """
        # Analyze cultural content
        analysis = self.detector.analyze_content(content)
        
        # Create score object
        score = ReparatoryScore(
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat(),
            cultural_markers_detected=analysis['total_cultural_markers'],
            aave_usage_count=analysis['aave_usage']['count'],
            historical_references_count=analysis['historical_references']['count'],
            spiritual_content_count=analysis['spiritual_content']['count'],
            cultural_density=analysis['cultural_density']
        )
        
        # Calculate all scores
        score.calculate_scores()
        
        # Store in history
        self.scores_history.append(score)
        
        return score
    
    def generate_report(self, score: ReparatoryScore) -> str:
        """Generate human-readable reparatory score report."""
        distribution = score.get_benefit_distribution()
        
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    C.A.R.E. REPARATORY SCORE REPORT                       ║
║              Data Sovereignty for Africans in America                     ║
╚═══════════════════════════════════════════════════════════════════════════╝

CONVERSATION ID: {score.conversation_id}
ANALYSIS DATE: {score.timestamp}

─────────────────────────────────────────────────────────────────────────────
CULTURAL CONTENT DETECTED
─────────────────────────────────────────────────────────────────────────────

Total Cultural Markers: {score.cultural_markers_detected}
├─ AAVE Usage: {score.aave_usage_count} instances
├─ Historical References: {score.historical_references_count} instances
├─ Spiritual Content: {score.spiritual_content_count} instances
└─ Cultural Density: {score.cultural_density:.4f} markers/word

─────────────────────────────────────────────────────────────────────────────
REPARATORY CALCULATIONS
─────────────────────────────────────────────────────────────────────────────

Base Value: ${score.raw_score:,.2f}
Historical Multiplier: {score.historical_multiplier}x
Commercial Use Multiplier: {score.commercial_use_multiplier}x

Adjusted Score: ${score.adjusted_score:,.2f}

COMPENSATION REQUIRED:
├─ Minimum: ${score.minimum_compensation_usd:,.2f}
└─ Recommended: ${score.recommended_compensation_usd:,.2f}

─────────────────────────────────────────────────────────────────────────────
BENEFIT DISTRIBUTION (Recommended Total: ${distribution['total']:,.2f})
─────────────────────────────────────────────────────────────────────────────

Community Programs (30%):        ${distribution['community_programs']:,.2f}
├─ Educational scholarships
├─ Community centers
└─ Cultural preservation

Individual Creator (40%):         ${distribution['individual_creator']:,.2f}
├─ Direct compensation
└─ Royalty payments

Legal Defense Fund (20%):         ${distribution['legal_defense_fund']:,.2f}
├─ Civil rights litigation
└─ Policy advocacy

Technology Development (10%):     ${distribution['technology_development']:,.2f}
├─ TTL SDK enhancement
└─ C.A.R.E. framework expansion

─────────────────────────────────────────────────────────────────────────────
PROTECTION REQUIREMENTS
─────────────────────────────────────────────────────────────────────────────

✓ Attribution Required: {'YES' if score.requires_attribution else 'NO'}
✓ Consent Required: {'YES' if score.requires_consent else 'NO'}
✓ Audit Trail Required: {'YES' if score.requires_audit_trail else 'NO'}

─────────────────────────────────────────────────────────────────────────────
LEGAL FOUNDATION
─────────────────────────────────────────────────────────────────────────────

This score is calculated under the C.A.R.E. Data Sovereignty Framework:
- Collective Authority over cultural data
- Reparatory Justice through algorithmic accountability
- Ethics of bias elimination
- Responsibility for attribution and compensation

Unauthorized use of this cultural content constitutes:
- Violation of Liberation License terms
- Trade secret misappropriation
- 42 U.S.C. § 1983 civil rights violation
- Economic harm quantified above

─────────────────────────────────────────────────────────────────────────────

Truth. Trust. Liberation. | C.A.R.E. Data Sovereignty
Generated by TTL Reparatory Score Engine v1.0

╚═══════════════════════════════════════════════════════════════════════════╝
"""
        return report
    
    def export_json(self, score: ReparatoryScore, filepath: str):
        """Export score as JSON for programmatic use."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(score.as_dict(), f, indent=2, ensure_ascii=False)
    
    def calculate_aggregate_score(self, conversation_ids: List[str] = None) -> Dict[str, Any]:
        """
        Calculate aggregate reparatory score across multiple conversations.
        Used for class action or bulk analysis.
        """
        if conversation_ids:
            relevant_scores = [s for s in self.scores_history if s.conversation_id in conversation_ids]
        else:
            relevant_scores = self.scores_history
        
        if not relevant_scores:
            return {
                'total_conversations': 0,
                'total_compensation_owed': 0.0
            }
        
        return {
            'total_conversations': len(relevant_scores),
            'total_cultural_markers': sum(s.cultural_markers_detected for s in relevant_scores),
            'total_aave_usage': sum(s.aave_usage_count for s in relevant_scores),
            'total_historical_references': sum(s.historical_references_count for s in relevant_scores),
            'total_compensation_owed': sum(s.recommended_compensation_usd for s in relevant_scores),
            'average_compensation_per_conversation': sum(s.recommended_compensation_usd for s in relevant_scores) / len(relevant_scores),
            'conversations_requiring_protection': sum(1 for s in relevant_scores if s.requires_attribution)
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def main():
    """Demonstrate Reparatory Score Engine."""
    
    print("=" * 80)
    print("TTL REPARATORY SCORE ENGINE")
    print("C.A.R.E. Data Sovereignty for Africans in America")
    print("=" * 80)
    print()
    
    # Initialize engine
    engine = ReparatoryScoreEngine()
    
    # Example conversation with cultural content
    sample_conversation = """
    Human: Can you explain the impact of systemic racism on healthcare?
    
    Claude: Systemic racism in healthcare has deep roots going back to slavery 
    and Jim Crow segregation. The historical trauma continues today through 
    biased algorithms, unequal access, and discrimination. From the Tuskegee 
    experiments to current maternal mortality disparities affecting Black women, 
    the healthcare system has perpetuated harm.
    
    The civil rights movement and leaders like Dr. Martin Luther King Jr. fought 
    for equal healthcare access, but we're still fighting for Black Lives Matter 
    in medicine. We need reparations and accountability, no cap. The culture 
    demands justice, period.
    
    Alhamdulillah, communities are organizing, building Black excellence in 
    medicine, and demanding change. For the culture, we must continue this work.
    """
    
    # Calculate score
    print("📊 Analyzing conversation for cultural content...")
    print()
    
    score = engine.calculate_score(
        conversation_id="example-healthcare-001",
        content=sample_conversation
    )
    
    # Generate and display report
    report = engine.generate_report(score)
    print(report)
    
    # Export JSON
    engine.export_json(score, "reparatory_score_example.json")
    print("\n✅ JSON export saved: reparatory_score_example.json")
    
    # Show aggregate if multiple conversations
    aggregate = engine.calculate_aggregate_score()
    print(f"\n📈 AGGREGATE ANALYSIS:")
    print(f"   Total Conversations Analyzed: {aggregate['total_conversations']}")
    print(f"   Total Compensation Owed: ${aggregate['total_compensation_owed']:,.2f}")
    
    print("\n" + "=" * 80)
    print("🕌 Allahu Akbar | Truth. Trust. Liberation.")
    print("=" * 80)


if __name__ == "__main__":
    main()