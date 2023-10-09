import unittest
import requests
from crud_db import create_workflow, create_protocol, create_step, create_parameter


BASE_URL = "http://127.0.0.1:5000"

class TestIntegration(unittest.TestCase):

    def setUp(self):
        # Protocol for integration test
        create_workflow("PCR Workflow")

        create_protocol(1, "PCR version 1", "Amplify template using annealing temp of 60°C over 30 cycles")

        create_step(1, 1, "In PCR tubes of 200 μl", 1)
        create_step(1, 1, "Add 38 μl sterile water", 2)
        create_step(1, 1, "Add 2 μl of forward primer (10 μM)", 3)
        create_step(1, 1, "Add 2 μl of reverse primer (10 μM)", 4)
        create_step(1, 1, "Add 1 μl of dNTPs (50 μM)", 5)
        create_step(1, 1, "Add 5 μl of reaction buffer containing MgCl2 (10X)", 6)
        create_step(1, 1, "Add 1 μl of DNA template (100 ng/μl)", 7)
        create_step(1, 1, "Add 1 μl of DNA polymerase (0.5 U/μl)", 8)

        create_step(1, 9, "Pipette gently the reaction mixture to allow good homogenization", 9)

        create_step(1, 10, "Spin 10 seconds at 1000 RPM", 10)

        create_step(1, 11, "Transfer to thermocycler and run the following program", 11)
        create_step(1, 11, "An initial step of DNA denaturation at 98°C for 5 min", 12)
        create_step(1, 11, "Cycle through 30 rounds of", 13)
        create_step(1, 13, "Denaturation: 98°C for 30 seconds", 14)
        create_step(1, 13, "Annealing: 60°C for 30 seconds", 15)
        create_step(1, 13, "Extension: 68°C for 2 min", 16)
        create_step(1, 11, "Final extension: 72°C for 10 min", 17)

        create_step(1, 18, "Store at 4°C", 18)

        # parameters
        create_parameter(2, "Water Quantity", "numeric", "38")
        create_parameter(3, "forward primer (10 μM)", "numeric", "2")
        create_parameter(4, "Reverse Primer", "numeric", "2")
        create_parameter(5, "dNTPs (50 μM)", "numeric", "1")
        create_parameter(6, "reaction buffer containing MgCl2 (10X)", "numeric", "5")
        create_parameter(7, "DNA template (100 ng/μl)", "numeric", "1")
        create_parameter(8, "DNA polymerase (0.5 U/μl)", "numeric", "1")

        create_parameter(10, "spin time (s)", "numeric", "10")
        create_parameter(10, "spin speed (RPM)", "numeric", "1000")

        create_parameter(11, "cycle", "numeric", "30")
        create_parameter(12, "temperature (°C)", "numeric", "98")
        create_parameter(11, "time (seconds)", "numeric", "30")
        create_parameter(12, "temperature (°C)", "numeric", "60")
        create_parameter(11, "time (seconds)", "numeric", "30")
        create_parameter(12, "temperature (°C)", "numeric", "68")
        create_parameter(11, "time (seconds)", "numeric", "120")
        create_parameter(12, "temperature (°C)", "numeric", "72")
        create_parameter(11, "time (seconds)", "numeric", "600")

    def tearDown(self):
        # Delete all entries using the API
        self._api_delete("/workflows")
        self._api_delete("/protocols")
        self._api_delete("/steps")
        self._api_delete("/parameters")

    def test_pcr_workflow_retrieval(self):
        response = self._api_get("/workflows")
        workflows = response.json()
        self.assertIn("PCR Workflow", [wf["name"] for wf in workflows])

    def test_pcr_protocol_retrieval(self):
        response = self._api_get("/protocols")
        protocols = response.json()
        self.assertIn("PCR version 1", [protocol["name"] for protocol in protocols])

    def test_steps_retrieval(self):
        response = self._api_get("/steps/protocol_id/1")
        steps = response.json()
        expected_steps = [
            "In PCR tubes of 200 μl",
            "Add 38 μl sterile water",
            "Add 2 μl of forward primer (10 μM)",
            "Add 2 μl of reverse primer (10 μM)",
            "Add 1 μl of dNTPs (50 μM)",
            "Add 5 μl of reaction buffer containing MgCl2 (10X)",
            "Add 1 μl of DNA template (100 ng/μl)",
            "Add 1 μl of DNA polymerase (0.5 U/μl)",
            "Pipette gently the reaction mixture to allow good homogenization",
            "Spin 10 seconds at 1000 RPM",
            "Transfer to thermocycler and run the following program",
            "An initial step of DNA denaturation at 98°C for 5 min",
            "Cycle through 30 rounds of",
            "Denaturation: 98°C for 30 seconds",
            "Annealing: 60°C for 30 seconds",
            "Extension: 68°C for 2 min",
            "Final extension: 72°C for 10 min",
            "Store at 4°C"
        ]
        self.assertListEqual([step["description"] for step in steps], expected_steps)

    def test_parameters_retrieval(self):
        response = self._api_get("/parameters")
        parameters = response.json()
        expected_parameters = [
            ('Water Quantity', 'numeric', '38'),
            ('forward primer (10 μM)', 'numeric', '2'),
            ('Reverse Primer', 'numeric', '2'),
            ('dNTPs (50 μM)', 'numeric', '1'),
            ('reaction buffer containing MgCl2 (10X)', 'numeric', '5'),
            ('DNA template (100 ng/μl)', 'numeric', '1'),
            ('DNA polymerase (0.5 U/μl)', 'numeric', '1'),
            ('spin time (s)', 'numeric', '10'),
            ('spin speed (RPM)', 'numeric', '1000'),
            ('cycle', 'numeric', '30'),
            ('temperature (°C)', 'numeric', '98'),
            ('time (seconds)', 'numeric', '30'),
            ('temperature (°C)', 'numeric', '60'),
            ('time (seconds)', 'numeric', '30'),
            ('temperature (°C)', 'numeric', '68'),
            ('time (seconds)', 'numeric', '120'),
            ('temperature (°C)', 'numeric', '72'),
            ('time (seconds)', 'numeric', '600')
        ]
        params_result = [(param["name"], param["value_type"], param["value"]) for param in parameters]
        self.assertListEqual(params_result, expected_parameters)

    # Helper methods for API interaction
    def _api_post(self, endpoint, data):
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        response.raise_for_status()

    def _api_get(self, endpoint):
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        return response

    def _api_delete(self, endpoint):
        response = requests.delete(f"{BASE_URL}{endpoint}")
        response.raise_for_status()

if __name__ == '__main__':
    unittest.main()
