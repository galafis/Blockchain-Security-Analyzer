import pytest
from src.app import app, analyze_solidity_contract


def test_comments_and_strings_are_not_findings():
    code = '// block.timestamp\n/* x += 1; gas: 2300 */\nstring x = "block.timestamp";'
    assert analyze_solidity_contract(code) == []


def test_offsets_and_each_occurrence():
    code = "// example\nblock.timestamp;\n  block.timestamp;"
    findings = analyze_solidity_contract(code)
    assert [(f["line"], f["column"]) for f in findings] == [(2, 1), (3, 3)]
    for finding in findings:
        assert code[finding["start"] : finding["end"]] == finding["evidence"]
        assert finding["classification"] == "review_required"


@pytest.mark.parametrize(
    "code",
    [17, True, ["code"], "   ", "x" * 100001],
    ids=["number", "boolean", "array", "blank", "oversized"],
)
def test_invalid_source_returns_client_error(code):
    assert (
        app.test_client().post("/api/analyze", json={"code": code}).status_code == 400
    )


def test_modern_arithmetic_is_explained_as_contextual_review():
    finding = analyze_solidity_contract("pragma solidity ^0.8.20; uint x; x += 1;")[0]
    assert "by default" in finding["description_en"]
