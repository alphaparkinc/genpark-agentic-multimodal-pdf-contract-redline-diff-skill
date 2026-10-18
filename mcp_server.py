#!/usr/bin/env python3
import json
import sys
from client import AgenticContractRedlineDiffSentinel

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sentinel = AgenticContractRedlineDiffSentinel()
        base = [
            {"clause_id": "SEC-1", "section_name": "Liability", "text": "Each party liability shall be capped at 12 months fees paid."},
            {"clause_id": "SEC-2", "section_name": "IP", "text": "Customer retains all background IP."}
        ]
        rev = [
            {"clause_id": "SEC-1", "section_name": "Liability", "text": "Customer shall provide unlimited liability and indemnify provider."},
            {"clause_id": "SEC-2", "section_name": "IP", "text": "Customer retains all background IP."}
        ]
        res = sentinel.redline_compare_clauses(base, rev)
        assert res["high_risk_escalations_count"] >= 1
        assert res["verdict"] == "CONTRACT_FLAGGED_RISK_ESCALATIONS"
        print(f"[TEST PASS] Contract Redline Diff Flagged: {res['high_risk_escalations_count']} escalations")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-contract-redline", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "redline_compare_clauses", "description": "Compare contract clause revisions and detect liability risks"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                sentinel = AgenticContractRedlineDiffSentinel()
                out = sentinel.redline_compare_clauses(args.get("baseline_clauses", []), args.get("revised_clauses", []))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
