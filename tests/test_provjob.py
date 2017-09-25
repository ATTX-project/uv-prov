import falcon
import unittest
import httpretty
from falcon import testing
from uvprov_api.app import create
from mock import patch
# import testing.mysqld

# Generate Mysqld class which shares the generated database
# Mysqld = testing.mysqld.Mysqld(copy_data_from='tests/resources')


class appProvjobTest(testing.TestCase):
    """Testing GM prov function and initialize it for that purpose."""

    def setUp(self):
        """Setting the app up."""
        self.app = create()

    def tearDown(self):
        """Tearing down the app up."""
        # Mysqld.clear_cache()
        # self.mysqld.stop()


class TestProv(appProvjobTest):
    """Testing if there is a provjob endoint available."""

    def test_create(self):
        """Test GET provjob message."""
        self.app
        # self.mysqld = Mysqld()
        pass

    @httpretty.activate
    @patch('uvprov_api.api.healthcheck.prov_job')
    def test_provjob_ok(self, mock):
        """Test GET provjob is ok."""
        httpretty.register_uri(httpretty.GET, "http://localhost:4301/provjob", status=202)
        result = self.simulate_get('/provjob')
        assert(result.status == falcon.HTTP_202)


if __name__ == "__main__":
    unittest.main()
