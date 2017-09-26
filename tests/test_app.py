# import falcon
import unittest
import httpretty
# import requests
from falcon import testing
from uvprov_api.app import init_api
# from wf_api.app import api_version
# from datetime import datetime
# from wf_api.utils.db import connect_DB


class appTest(testing.TestCase):
    """Testing GM map function and initialize it for that purpose."""

    def setUp(self):
        """Setting the app up."""
        # self.conn = connect_DB()
        self.app = init_api()

    def tearDown(self):
        """Tearing down the app up."""
        pass


class TestApp(appTest):
    """Test app is ok."""

    @httpretty.activate
    def test_main(self):
        """Test the server is up and running."""
        httpretty.register_uri(httpretty.GET, "http://localhost:4301/", status=404)
        response = self.simulate_get('/')
        assert(response.status_code == 404)

    # @httpretty.activate
    # def test_activity_ok(self):
    #     """Test GET map response is OK."""
    #     httpretty.register_uri(httpretty.GET, "http://localhost:4301/0.1/activity?modifiedSince=2017-02-03T08%3A14%3A14Z", status=304)
    #     params = {"modifiedSince": str(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))}
    #     result = self.simulate_get('/{0}/activity'.format(api_version), params=params)
    #     assert(result.status == falcon.HTTP_304)


if __name__ == "__main__":
    unittest.main()
