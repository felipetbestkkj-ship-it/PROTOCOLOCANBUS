import json
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "hvac_contract_validator", ROOT / "scripts" / "validate_hvac_behavior_contract.py"
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

class HvacBehaviorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "contracts" / "hvac_behavior_contract.json").read_text(encoding="utf-8"))

    def test_contract_passes_validator(self):
        result = mod.validate_contract(self.data)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(18, result["summary"]["functions"])

    def test_one_shot_vector_is_frozen(self):
        self.assertEqual("5A A5 02 3B 06 01 43", self.data["common_physical_link"]["predicted_tx"])
        self.assertEqual(mod.hvac_tx(0x06, 0x01), mod.parse_hex(self.data["common_physical_link"]["predicted_tx"]))

    def test_rear_defrost_observed_transition_is_single_field(self):
        s = [mod.decode31(mod.parse_hex(x)) for x in mod.OBSERVED_SEQUENCE]
        self.assertEqual({"rear_defrost"}, mod.logical_diff(s[1], s[2]))
        self.assertEqual({"rear_defrost"}, mod.logical_diff(s[3], s[4]))

    def test_recirculation_observed_transition_is_single_field(self):
        s = [mod.decode31(mod.parse_hex(x)) for x in mod.OBSERVED_SEQUENCE]
        self.assertEqual({"recirculation"}, mod.logical_diff(s[4], s[5]))

    def test_every_control_has_rx_mapping_and_pending_physical_link(self):
        for f in self.data["functions"]:
            self.assertIn(f["rx"], self.data["rx_layout"])
            self.assertEqual("PHYSICAL_PENDING", f["physical_link"])

if __name__ == "__main__":
    unittest.main()
