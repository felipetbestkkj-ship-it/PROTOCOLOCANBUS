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

    def test_generic_contract_passes_validator(self):
        result = mod.validate_contract(self.data)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(18, result["summary"]["generic_protocol_operations"])
        self.assertEqual("contracts/hvac_target_profile.json", result["summary"]["target_profile"])

    def test_recirculation_observed_transition_is_single_field(self):
        s = [mod.decode31(mod.parse_hex(x)) for x in mod.OBSERVED_SEQUENCE]
        self.assertEqual({"recirculation"}, mod.logical_diff(s[4], s[5]))

    def test_generic_rear_defrost_bit_is_preserved_as_protocol_evidence_only(self):
        s = [mod.decode31(mod.parse_hex(x)) for x in mod.OBSERVED_SEQUENCE]
        self.assertEqual({"rear_defrost"}, mod.logical_diff(s[1], s[2]))
        self.assertEqual({"rear_defrost"}, mod.logical_diff(s[3], s[4]))
        # Target applicability is intentionally NOT asserted here.
        # It lives in contracts/hvac_target_profile.json.

    def test_every_generic_control_has_rx_mapping(self):
        for f in self.data["functions"]:
            self.assertIn(f["rx"], self.data["rx_layout"])


if __name__ == "__main__":
    unittest.main()
