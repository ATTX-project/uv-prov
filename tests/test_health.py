import falcon
import unittest
import httpretty
from falcon import testing
from uvprov_api.app import init_api


class appHealthTest(testing.TestCase):
    """Testing GM prov function and initialize it for that purpose."""

    def setUp(self):
        """Setting the app up."""
        self.app = init_api()

    def tearDown(self):
        """Tearing down the app up."""
        pass


class TestProv(appHealthTest):
    """Testing if there is a health endoint available."""

    def test_create(self):
        """Test GET health message."""
        self.app
        pass

    @httpretty.activate
    def test_health_ok(self):
        """Test GET health is ok."""
        httpretty.register_uri(httpretty.GET, "http://localhost:4301/health", status=200)
        result = self.simulate_get('/health')
        assert(result.status == falcon.HTTP_200)
        httpretty.disable()
        httpretty.reset()


if __name__ == "__main__":
    unittest.main()
