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
    @patch('uvprov_api.api.workflow.workflow_get_output')
    def test_api_workflow(self, mock):
        """Test activity API."""
        with open('tests/resources/data_workflow.json') as datafile:
            prov_data = datafile.read()
        mock.return_value = prov_data
        httpretty.register_uri(httpretty.GET, "{0}/{1}/workflow".format(self.api, self.version), prov_data, status=200)
        result = self.simulate_get('/{0}/workflow'.format(self.version), body=prov_data)
        assert(result.status == falcon.HTTP_200)


if __name__ == "__main__":
    unittest.main()
