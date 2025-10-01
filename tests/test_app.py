
import unittest
import json
from src.app import app, analyze_solidity_contract

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))
        self.assertIn("project", data)
        self.assertEqual(data["project"], "Blockchain-Security-Analyzer")

    def test_status_route(self):
        response = self.app.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))
        self.assertIn("status", data)
        self.assertEqual(data["status"], "running")

    def test_analyze_solidity_contract_reentrancy(self):
        contract_code = """
        function vulnerable() public payable {
            (bool success, ) = msg.sender.call{value: msg.value}("");
            require(success);
        }
        """
        findings = analyze_solidity_contract(contract_code)
        self.assertTrue(any(f["vulnerability"] == "Potencial Reentrancy" for f in findings))

    def test_analyze_solidity_contract_integer_overflow(self):
        contract_code = """
        uint256 public balance;
        function add(uint256 _value) public {
            balance += _value;
        }
        """
        findings = analyze_solidity_contract(contract_code)
        self.assertTrue(any(f["vulnerability"] == "Potencial Integer Overflow/Underflow" for f in findings))

    def test_analyze_solidity_contract_timestamp_dependency(self):
        contract_code = """
        function checkTime() public view returns (uint256) {
            return block.timestamp;
        }
        """
        findings = analyze_solidity_contract(contract_code)
        self.assertTrue(any(f["vulnerability"] == "Potencial Dependência de Timestamp" for f in findings))

    def test_analyze_solidity_contract_hardcoded_gas_limit(self):
        contract_code = """
        function callExternal() public {
            (bool success, ) = address(0x123).call{gas: 2300}("");
            require(success);
        }
        """
        findings = analyze_solidity_contract(contract_code)
        self.assertTrue(any(f["vulnerability"] == "Potencial Limite de Gás Hardcoded" for f in findings))

    def test_analyze_solidity_contract_no_vulnerabilities(self):
        contract_code = """
        function safeFunction() public pure returns (uint256) {
            return 1 + 1;
        }
        """
        findings = analyze_solidity_contract(contract_code)
        self.assertEqual(len(findings), 0)

    def test_analyze_api_endpoint(self):
        contract_code = "function test() public {}"
        response = self.app.post("/api/analyze", data=json.dumps({"code": contract_code}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))
        self.assertIn("analysis_results", data)
        self.assertIsInstance(data["analysis_results"], list)

    def test_analyze_api_endpoint_no_code(self):
        response = self.app.post("/api/analyze", data=json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode("utf-8"))
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Nenhum código de contrato fornecido")

if __name__ == "__main__":
    unittest.main()

