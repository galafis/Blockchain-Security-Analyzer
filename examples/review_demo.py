from pathlib import Path
from src.app import analyze_solidity_contract


def run():
    source = Path(__file__).with_name("review.sol").read_text(encoding="utf-8")
    findings = analyze_solidity_contract(source)
    assert any(item["rule_id"] == "timestamp-review" for item in findings)
    return {
        "synthetic": True,
        "classification": "review_required",
        "findings": findings,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), ensure_ascii=False, indent=2, allow_nan=False))
