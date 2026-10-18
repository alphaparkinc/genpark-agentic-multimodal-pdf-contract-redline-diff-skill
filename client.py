"""
AI Multimodal Contract Redline Diff Sentinel (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import re
from typing import Dict, Any, List, Optional

class AgenticContractRedlineDiffSentinel:
    HIGH_RISK_KEYWORDS = {
        "indemnify": "HIGH_LIABILITY_INDEMNIFICATION",
        "unlimited liability": "CRITICAL_UNLIMITED_EXPOSURE",
        "sole remedy": "REMEDY_EXCLUSION_RISK",
        "perpetual": "PERPETUAL_COMMITMENT_RISK",
        "assign all rights": "IP_FORFEITURE_RISK"
    }

    def __init__(self, sentinel_name: str = "GenPark-Legal-Redline-Core"):
        self.sentinel_name = sentinel_name

    def redline_compare_clauses(self, baseline_clauses: List[Dict[str, Any]], revised_clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        base_map = {c.get("clause_id", f"C-{i}"): c for i, c in enumerate(baseline_clauses)}
        rev_map = {c.get("clause_id", f"C-{i}"): c for i, c in enumerate(revised_clauses)}
        
        diffs = []
        high_risk_escalations = 0
        
        all_ids = sorted(list(set(base_map.keys()) | set(rev_map.keys())))
        for cid in all_ids:
            b_clause = base_map.get(cid)
            r_clause = rev_map.get(cid)
            
            if not b_clause:
                diffs.append({"clause_id": cid, "change_type": "NEW_UNILATERAL_CLAUSE", "section": r_clause.get("section_name", "General"), "severity": "MEDIUM"})
            elif not r_clause:
                diffs.append({"clause_id": cid, "change_type": "DELETED_PROTECTIVE_CLAUSE", "section": b_clause.get("section_name", "General"), "severity": "HIGH"})
                high_risk_escalations += 1
            else:
                b_text = b_clause.get("text", "")
                r_text = r_clause.get("text", "")
                if b_text != r_text:
                    r_low = r_text.lower()
                    flagged_risks = [desc for kw, desc in self.HIGH_RISK_KEYWORDS.items() if kw in r_low and kw not in b_text.lower()]
                    sev = "HIGH" if flagged_risks else "LOW"
                    if sev == "HIGH":
                        high_risk_escalations += 1
                    diffs.append({
                        "clause_id": cid,
                        "section": r_clause.get("section_name", "General"),
                        "change_type": "MODIFIED_CLAUSE",
                        "severity": sev,
                        "flagged_risks": flagged_risks
                    })
                    
        verdict = "CONTRACT_FLAGGED_RISK_ESCALATIONS" if high_risk_escalations > 0 else "CONTRACT_REVISION_ACCEPTABLE"
        return {
            "sentinel": self.sentinel_name,
            "total_clauses_reviewed": len(all_ids),
            "discrepancy_count": len(diffs),
            "high_risk_escalations_count": high_risk_escalations,
            "clause_diffs": diffs,
            "verdict": verdict
        }
