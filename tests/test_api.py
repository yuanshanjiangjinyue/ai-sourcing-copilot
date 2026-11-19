import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
import app.main as module

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        module.DB=Path(self.tmp.name)/"rfq.sqlite3"
        self.client=TestClient(module.app)
    def tearDown(self):
        self.client.close()
        self.tmp.cleanup()
    def test_health_and_catalog(self):
        self.assertTrue(self.client.get("/api/health").json()["ok"])
        self.assertEqual(len(self.client.get("/api/products").json()["items"]),16)
        self.assertEqual(self.client.get("/").status_code,200)
    def test_rfq(self):
        payload={"sku":"DEMO-CAM-001","requirements":{},"qty":20,"destination":"Germany"}
        resp=self.client.post("/api/rfqs",json=payload)
        self.assertEqual(resp.status_code,201)
        self.assertEqual(resp.json()["status"],"draft-only")
        self.assertEqual(len(self.client.get("/api/rfqs").json()["items"]),1)
    def test_bad_sku(self):
        payload={"sku":"NOT-REAL","requirements":{},"qty":1,"destination":"Germany"}
        self.assertEqual(self.client.post("/api/rfqs",json=payload).status_code,422)
if __name__=="__main__":unittest.main()
