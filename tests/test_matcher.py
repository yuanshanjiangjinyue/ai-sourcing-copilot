import unittest
from app.matcher import parse_requirements, match, CATALOG

class MatcherTests(unittest.TestCase):
    def test_catalog(self):
        self.assertEqual(len(CATALOG),16)
    def test_parse(self):
        x=parse_requirements("Linux ARM64 USB3 全局快门 ≥2MP ≥120fps 预算 $320 采购 20 台")
        self.assertEqual(x["os"],"Linux")
        self.assertEqual(x["arch"],"arm64")
        self.assertEqual(x["min_fps"],120)
        self.assertEqual(x["max_price"],320)
        self.assertEqual(x["qty"],20)
    def test_camera(self):
        x=match(dict(interface="USB3",shutter="global",os="Linux",arch="arm64",min_mp=2,min_fps=120,max_price=320,qty=20))
        self.assertIn("DEMO-CAM-001",[p["sku"] for p in x["eligible"]])
        self.assertEqual(x["stats"]["total"],16)
        self.assertGreaterEqual(x["stats"]["review"],1)
    def test_conflict(self):
        self.assertEqual(match({"interface":"conflict"})["stats"]["eligible"],0)
    def test_no_match(self):
        self.assertEqual(match(dict(min_mp=100,min_fps=10000,max_price=1))["stats"]["eligible"],0)
if __name__=="__main__":unittest.main()
