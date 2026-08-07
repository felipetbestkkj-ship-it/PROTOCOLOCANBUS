import json
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "hvac_target_profile_validator", ROOT / "scripts" / "validate_hvac_target_profile.py"
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class HvacTargetProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "contracts" / "hvac_target_profile.json").read_text(encoding="utf-8"))

    def test_profile_passes_validator(self):
        result = mod.validate_profile(self.data)
        self.assertTrue(result["ok"], result["errors"])

    def test_vehicle_has_only_front_defrost(self):
        self.assertTrue(self.data["owner_confirmed"]["front_defrost"])
        self.assertFalse(self.data["owner_confirmed"]["rear_defrost"])

    def test_one_shot_is_recirculation(self):
        gate = self.data["f3_one_shot_gate"]
        self.assertEqual("recirculation_on", gate["action"])
        self.assertEqual("5A A5 02 3B 07 00 43", gate["predicted_tx"])
        self.assertEqual("0x31 payload[1] bit4: 0 -> 1", gate["predicted_rx_change"])

    def test_generic_rear_defrost_is_not_target_feature(self):
        entry = next(x for x in self.data["protocol_capabilities_not_target_features"] if x["name"] == "rear_defrost")
        self.assertEqual("NOT_PRESENT_ON_TARGET", entry["target_status"])


if __name__ == "__main__":
    unittest.main()
