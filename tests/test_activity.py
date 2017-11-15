import unittest
from mock import patch
import httpretty
import falcon
# import json
from falcon import testing
from uvprov_api.app import init_api


class ActivityGetTest(testing.TestCase):
    """Testing Graph Store and initialize the app for that.."""

    def setUp(self):
        """Setting the app up."""
        self.api = "http://localhost:4031/"
        self.version = "0.2"
        self.app = init_api()

    def tearDown(self):
        """Tearing down the app up."""
        pass


class ActivityTestCase(ActivityGetTest):
    """Test for Graph Store operations."""

    def test_create(self):
        """Test create API."""
        self.app
        pass

    @httpretty.activate
    @patch('uvprov_api.api.activity.activity_get_output')
    def test_api_activity(self, mock):
        """Test activity API."""
        with open('tests/resources/data_activity.json') as datafile:
            prov_data = datafile.read()
        mock.return_value = prov_data
        httpretty.register_uri(httpretty.GET, "{0}/{1}/activity".format(self.api, self.version), prov_data, status=200)
        result = self.simulate_get('/{0}/activity'.format(self.version), body=prov_data)
        assert(result.status == falcon.HTTP_200)
        httpretty.disable()
        httpretty.reset()


if __name__ == "__main__":
    unittest.main()
