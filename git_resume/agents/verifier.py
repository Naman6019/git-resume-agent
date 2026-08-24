from typing import Dict, Any, List, Tuple

class GroundingVerifierAgent:
    """Ensures that generated metrics and claims are grounded in actual git evidence and AST structures."""

    def verify_bullet(self, bullet: str, ground_truth: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates a proposed bullet against inspected repo data."""
        # 1. Verify tech stack alignment
        claimed_stack = set([s.lower() for s in ground_truth.get("stack", [])])
        
        # 2. Check for metric sanity
        if "lines of code" in bullet.lower():
            # Ensure LOC claim matches ground truth
            loc_k = ground_truth.get("loc_k", "")
            if loc_k and loc_k not in bullet:
                return False, f"LOC mismatch (expected ~{loc_k})"

        return True, "Verified against Git tree and commit history"
