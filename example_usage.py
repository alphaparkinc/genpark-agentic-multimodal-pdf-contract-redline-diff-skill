from client import AgenticContractRedlineDiffSentinel

def main():
    sentinel = AgenticContractRedlineDiffSentinel()
    b = [{"clause_id": "C-1", "section_name": "Confidentiality", "text": "Standard 3-year confidentiality period."}]
    r = [{"clause_id": "C-1", "section_name": "Confidentiality", "text": "Perpetual confidentiality obligation with sole remedy exclusion."}]
    res = sentinel.redline_compare_clauses(b, r)
    print("--- Legal Redline Diff Audit ---")
    print(f"Verdict: {res['verdict']} | Escalations: {res['high_risk_escalations_count']}")
    for d in res['clause_diffs']:
        print(f"* [{d['severity']}] {d['clause_id']}: {d['change_type']} -> {d.get('flagged_risks')}")

if __name__ == "__main__":
    main()
