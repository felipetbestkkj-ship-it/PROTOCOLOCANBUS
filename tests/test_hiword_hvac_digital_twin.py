import unittest
from scripts.hiworld_hvac_digital_twin import (
    STATES, StateMachine, FakeCanbox, Builder, Request,
    hvac_tx, decode31, encode31, infer, valid
)

class FrameTests(unittest.TestCase):
    def test_static_vectors(self):
        vectors={(1,1):"5a a5 02 3b 01 01 3e",(2,1):"5a a5 02 3b 02 01 3f",(5,1):"5a a5 02 3b 05 01 42",(6,1):"5a a5 02 3b 06 01 43",(11,1):"5a a5 02 3b 0b 01 48",(12,1):"5a a5 02 3b 0c 01 49",(13,1):"5a a5 02 3b 0d 01 4a",(15,1):"5a a5 02 3b 0f 01 4c",(16,1):"5a a5 02 3b 10 01 4d"}
        for key,expected in vectors.items():
            frame=hvac_tx(*key); self.assertEqual(expected,frame.hex(" ")); self.assertTrue(valid(frame))
    def test_31_roundtrip(self):
        for state in STATES:self.assertEqual(state,decode31(encode31(state)))

class BuilderTests(unittest.TestCase):
    def setUp(self):self.s=STATES[0];self.b=Builder(self.s)
    def test_power(self):
        self.assertEqual([],self.b.build(Request(16385,8,1)))
        self.assertEqual([hvac_tx(1,0)],self.b.build(Request(16385,8,0)))
    def test_recirc(self):
        self.assertEqual([],self.b.build(Request(16394,-2147483648,1)))
        self.assertEqual([hvac_tx(7,1)],self.b.build(Request(16394,-2147483648,0)))
    def test_fan_absolute(self):
        self.assertEqual([hvac_tx(11,1)]*3,self.b.build(Request(16389,-2147483648,7)))
        self.assertEqual([hvac_tx(11,2)]*2,self.b.build(Request(16389,-2147483648,2)))
    def test_airflow_changed_bits_only(self):
        self.assertEqual([hvac_tx(9,0),hvac_tx(8,1),hvac_tx(10,1)],self.b.build(Request(16391,-2147483648,5)))
    def test_temperature_step_count(self):
        self.assertEqual([hvac_tx(12,1)]*2,self.b.build(Request(16387,1,22.0)))
        self.assertEqual([hvac_tx(12,1)],Builder(self.s,1).build(Request(16387,1,22.0)))

class GrammarTests(unittest.TestCase):
    def test_replay(self):self.assertEqual(STATES,StateMachine().replay())
    def test_actions(self):
        got=[infer(a,b).action for a,b in zip(STATES,STATES[1:])]
        self.assertEqual(["FRONT_DEFROST_ON","REAR_DEFROST_ON","FRONT_DEFROST_OFF","REAR_DEFROST_OFF","RECIRCULATION_ON","HVAC_POWER_OFF","HVAC_POWER_ON"],got)
    def test_high_confidence_single_field(self):
        self.assertGreaterEqual(infer(STATES[1],STATES[2]).confidence,.99)
        self.assertGreaterEqual(infer(STATES[3],STATES[4]).confidence,.99)
        self.assertGreaterEqual(infer(STATES[4],STATES[5]).confidence,.99)
    def test_fake_rear_defrost(self):
        r=FakeCanbox(STATES[1]).receive(hvac_tx(6,1))
        self.assertEqual(STATES[2],r.state);self.assertEqual(encode31(STATES[2]),r.response)

if __name__=="__main__":unittest.main()
