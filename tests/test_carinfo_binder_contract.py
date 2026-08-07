import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CarInfoBinderContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "contracts" / "carinfo_hvac_binder_contract.json").read_text(encoding="utf-8"))

    def test_service_component_is_frozen(self):
        self.assertEqual("com.can.activity/com.can.ui.CanPopWind", self.data["service"]["component"])
        self.assertIn("autoai.intent.action.CANBUS_SERVICE", self.data["service"]["intent_actions"])
        self.assertTrue(self.data["service"]["runtime_service_resolver_seen"])

    def test_core_hvac_transactions_are_frozen(self):
        bus = self.data["interfaces"]["ICanBus"]["transactions"]
        self.assertEqual(1, bus["registerListener"])
        self.assertEqual(7, bus["setHvacProperty"])
        self.assertEqual(13, bus["getHvacInfo"])
        self.assertEqual(26, bus["getPropertyList"])

    def test_callback_transaction_is_frozen(self):
        listener = self.data["interfaces"]["ICanBusListener"]["transactions"]
        self.assertEqual(1, listener["onHvacInfoChanged"])

    def test_external_binding_remains_unproven(self):
        self.assertNotEqual("PROVEN_EXTERNAL_BIND", self.data["status"])
        self.assertIn("External APK binding", self.data["security_observation"]["caveat"])

if __name__ == "__main__":
    unittest.main()
