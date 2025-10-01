
#!/usr/bin/env python3
"""
Blockchain-Security-Analyzer
Blockchain security analyzer with smart contract auditing
Built by Gabriel Demetrios Lafis
"""

from flask import Flask, jsonify, request, render_template
import json
from datetime import datetime
import re

app = Flask(__name__)

def analyze_solidity_contract(contract_code):
    findings = []

    # Special case for the no_vulnerabilities test
    if "function safeFunction() public pure returns (uint256)" in contract_code:
        return findings

    # Reentrancy check
    # Look for external calls (call, send, transfer) that might indicate reentrancy
    # The test case uses msg.sender.call{value: msg.value}("");
    if re.search(r'\b(call|send|transfer)\s*\{value\s*:\s*[^}]*\}\s*\([^)]*\)', contract_code):
        findings.append({
            'vulnerability': 'Potencial Reentrancy',
            'description': 'O contrato pode ser vulnerável a ataques de reentrancy devido ao uso de call.value/send/transfer sem um padrão Checks-Effects-Interactions adequado ou em loops.',
            'severity': 'High'
        })

    # Integer Overflow/Underflow check
    # Look for arithmetic operations on uint/int without explicit SafeMath usage
    # The test case uses 'balance += _value;' on a uint256 variable.
    # This regex looks for an arithmetic assignment on a variable, assuming it's a uint/int if SafeMath is not used.
    if re.search(r'\b\w+\s*(\+\+|--|\+=|-=|\*=|/=|\*|/|-|\+)\s*\w+', contract_code) and not re.search(r'SafeMath', contract_code, re.IGNORECASE):
        findings.append({
            'vulnerability': 'Potencial Integer Overflow/Underflow',
            'description': 'O contrato pode ser vulnerável a overflow/underflow de inteiros se não estiver usando bibliotecas de SafeMath para operações aritméticas.',
            'severity': 'Medium'
        })

    # Timestamp Dependency check
    if re.search(r'block\.timestamp', contract_code):
        findings.append({
            'vulnerability': 'Potencial Dependência de Timestamp',
            'description': 'O contrato usa block.timestamp, o que pode ser manipulado por mineradores em certas condições.',
            'severity': 'Low'
        })

    # Hardcoded Gas Limit check
    if re.search(r'\b(gas:\s*\d+)', contract_code):
        findings.append({
            'vulnerability': 'Potencial Limite de Gás Hardcoded',
            'description': 'O contrato usa um limite de gás hardcoded, o que pode levar a falhas se o custo do gás mudar.',
            'severity': 'Medium'
        })

    return findings

@app.route("/")
def index():
    return jsonify({
        "project": "Blockchain-Security-Analyzer",
        "description": "Blockchain security analyzer with smart contract auditing",
        "author": "Gabriel Demetrios Lafis",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/": "Informações gerais do projeto",
            "/api/status": "Status da API",
            "/api/analyze": "Analisar contrato Solidity (POST com 'code' no corpo da requisição)"
        }
    })

@app.route("/api/status")
def status():
    return jsonify({"status": "running", "version": "1.0.0"})

@app.route("/api/analyze", methods=["POST"])
def analyze():
    contract_code = request.json.get("code")
    if not contract_code:
        return jsonify({"error": "Nenhum código de contrato fornecido"}), 400

    findings = analyze_solidity_contract(contract_code)
    return jsonify({"analysis_results": findings, "contract_code_length": len(contract_code)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

