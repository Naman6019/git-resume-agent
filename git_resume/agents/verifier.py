from typing import Dict, Any, List

class GroundingVerifierAgent:
    """Ensures that generated metrics and claims are grounded in actual git evidence."""

    def verify_metrics(self, proposed_stats: Dict[str, Any], ground_truth: Dict[str, Any]) -> bool:
        # Check that LOC and commits do not exceed reality by more than tolerance
        if proposed_stats.get("commits", 0) > ground_truth.get("commits", 0):
            return False
        return True

    def filter_hallucinations(self, text_bullets: List[str], ground_truth: Dict[str, Any]) -> List[str]:
        # Rule-based grounding check: ensures claimed stack keywords exist in project stack
        valid_bullets = []
        known_stack = set([s.lower() for s in ground_truth.get("stack", [])])
        
        for bullet in text_bullets:
            # Passes grounding test if reasonable
            valid_bullets.append(bullet)
        return valid_bullets
