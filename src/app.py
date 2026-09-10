#!/usr/bin/env python3
"""
Blockchain-Security-Analyzer
Blockchain security analyzer with smart contract auditing
Built by Gabriel Demetrios Lafis
"""

from flask import Flask, jsonify, request
import json
from datetime import datetime
import re

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 500000


def mask_comments_and_strings(source):
    """Preserve character offsets and newlines while masking non-code tokens."""
    token = re.compile(
        r"""//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'"""
    )
    return token.sub(
        lambda match: "".join("\n" if char == "\n" else " " for char in match.group()),
        source,
    )


def analyze_solidity_contract(contract_code):
    if (
        not isinstance(contract_code, str)
        or not contract_code.strip()
        or len(contract_code) > 100000
    ):
        raise ValueError(
            "Source must contain 1–100000 characters / fonte deve conter 1–100000 caracteres"
        )
    code = mask_comments_and_strings(contract_code)
    rules = [
        (
            "external-value-call",
            r"\.call\s*\{[^}]*\bvalue\s*:[^}]*\}\s*\(",
            "Potencial Reentrancy",
            "High",
            "External value call: inspect ordering and reentrancy guards; this pattern is not proof of a vulnerability.",
            "Chamada externa com valor: revisar ordem e proteção contra reentrância; o padrão não comprova uma vulnerabilidade.",
        ),
        (
            "arithmetic-review",
            r"\b\w+\s*(?:\+\+|--|\+=|-=|\*=|/=)",
            "Potencial Integer Overflow/Underflow",
            "Medium",
            "Review arithmetic in its compiler and unchecked-block context. Solidity 0.8+ checks ordinary arithmetic by default.",
            "Revisar aritmética no contexto do compilador e de blocos unchecked. Solidity 0.8+ verifica a aritmética comum por padrão.",
        ),
        (
            "timestamp-review",
            r"\bblock\s*\.\s*timestamp\b",
            "Potencial Dependência de Timestamp",
            "Low",
            "Review time-dependent business rules and boundary conditions.",
            "Revisar regras de negócio dependentes de tempo e suas condições de limite.",
        ),
        (
            "fixed-gas-review",
            r"\bgas\s*:\s*\d+",
            "Potencial Limite de Gás Hardcoded",
            "Medium",
            "A fixed gas allowance may become insufficient when execution costs change.",
            "Uma quantidade fixa de gás pode se tornar insuficiente quando os custos de execução mudam.",
        ),
    ]
    findings = []
    for rule_id, pattern, title, severity, english, portuguese in rules:
        for match in re.finditer(pattern, code):
            findings.append(
                {
                    "rule_id": rule_id,
                    "vulnerability": title,
                    "severity": severity,
                    "classification": "review_required",
                    "description": portuguese,
                    "description_en": english,
                    "description_pt": portuguese,
                    "line": contract_code.count("\n", 0, match.start()) + 1,
                    "column": match.start()
                    - contract_code.rfind("\n", 0, match.start()),
                    "start": match.start(),
                    "end": match.end(),
                    "evidence": contract_code[match.start() : match.end()],
                }
            )
    return sorted(findings, key=lambda finding: (finding["start"], finding["rule_id"]))


@app.route("/")
def index():
    return jsonify(
        {
            "project": "Blockchain-Security-Analyzer",
            "description": "Solidity source review / revisão de código Solidity",
            "scope": "Heuristic review prompts; no proof of safety / revisão heurística, sem comprovação de segurança",
            "author": "Gabriel Demetrios Lafis",
            "status": "active",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "/": "Informações gerais do projeto",
                "/api/status": "Status da API",
                "/api/analyze": "Analisar contrato Solidity (POST com 'code' no corpo da requisição)",
            },
        }
    )


@app.route("/api/status")
def status():
    return jsonify({"status": "running", "version": "1.0.0"})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=False, silent=False)
        if data is None:
            return jsonify({"error": "Requisição JSON inválida"}), 400
        contract_code = data.get("code")
    except Exception:
        return jsonify({"error": "Requisição JSON inválida"}), 400

    if not contract_code:
        return jsonify({"error": "Nenhum código de contrato fornecido"}), 400

    try:
        findings = analyze_solidity_contract(contract_code)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(
        {"analysis_results": findings, "contract_code_length": len(contract_code)}
    )


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
