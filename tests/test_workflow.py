# from uvprov_api.api.workflow import workflow_get, workflow_post
# import unittest
# from uvprov_api.app import api_version, wfm_app
# from rdflib import Graph
# from flask import Response
#
#
# class WorkflowResponseTest(unittest.TestCase):
#     """Test for Workflow Response from API."""
#
#     def setUp(self):
#         """Set up test fixtures."""
#         self.app = wfm_app.app.test_client()
#         # propagate the exceptions to the test client
#         self.app.testing = True
#
#         self.graph = Graph()
#
#     def tearDown(self):
#         """Tear down test fixtures."""
#         pass
#
#     def test_workflow_post_response(self):
#         """Test Workflow POST Endpoint responds with a status code."""
#         result = self.app.post('/{0}/workflow'.format(api_version))
#
#         # assert the status code of the response
#         assert(result.status_code == 405)
#
#     def test_workflow_get_response(self):
#         """Test Workflow GET Endpoint responds with a status code."""
#         result = self.app.get('/{0}/workflow'.format(api_version))
#
#         # assert the status code of the response
#         self.assertIn(result.status_code, [200, 204, 304, 405])
#
#     def test_workflow_post_data(self):
#         """Test Workflow POST Endpoint data response."""
#         result = self.app.post('/{0}/workflow'.format(api_version))
#
#         assert(str(result.data).encode('utf-8') == """Operation Not Allowed.""")
#
#     def test_workflow_get_jsondata(self):
#         """Test Workflow GET Endpoint JSON-LD data response."""
#         result = self.app.get('/{0}/workflow?format=json-ld'.format(api_version))
#
#         if result.status_code == 200:
#             data = self.graph.parse(data=str(result.data).encode('utf-8'),
#                                     format='json-ld')
#             self.assertIsInstance(data, type(Graph()))
#         elif result.status_code == 204:
#             assert(result.data == '')
#         elif result.status_code == 304:
#             assert(result.data is None)
#
#     def test_workflow_get_modified(self):
#         """Test Workflow GET Endpoint JSON-LD data response."""
#         parameters = '?modifiedSince=2017-01-03T08%3A14%3A14Z'
#         result = self.app.get('/v{0}/workflow{1}'.format(api_version, parameters))
#
#         if result.status_code == 200:
#             data = self.graph.parse(data=str(result.data).encode('utf-8'),
#                                     format='turtle')
#             self.assertIsInstance(data, type(Graph()))
#         elif result.status_code == 204:
#             assert(result.data == '')
#         elif result.status_code == 304:
#             assert(result.data is None)
#
#     def test_workflow_get_json_and_date(self):
#         """Test Workflow GET Endpoint JSON-LD + modifiedSince data response."""
#         parameters = '?modifiedSince=2017-01-03T08%3A14%3A14Z&format=json-ld'
#         result = self.app.get('/{0}/workflow{1}'.format(api_version, parameters))
#
#         if result.status_code == 200:
#             data = self.graph.parse(data=str(result.data).encode('utf-8'),
#                                     format='json-ld')
#             self.assertIsInstance(data, type(Graph()))
#         elif result.status_code == 204:
#             assert(result.data == '')
#         elif result.status_code == 304:
#             assert(result.data is None)
#
#     def test_workflow_get_data(self):
#         """Test Workflow GET Endpoint data response."""
#         result = self.app.get('/{0}/workflow'.format(api_version))
#
#         if result.status_code == 200:
#             data = self.graph.parse(data=str(result.data).encode('utf-8'),
#                                     format='turtle')
#             self.assertIsInstance(data, type(Graph()))
#         elif result.status_code == 204:
#             assert(result.data == '')
#         elif result.status_code == 304:
#             assert(result.data is None)
#
#     def test_workflow_get_badformat(self):
#         """Test Workflow GET Endpoint bad format data response."""
#         result = self.app.get('/{0}/workflow?format=trig'.format(api_version))
#         assert(result.status_code == 405)
#
#     def test_workflow_get(self):
#         """Test Workflow GET provides a proper Response type."""
#         self.assertIsInstance(workflow_get(), type(Response()))
#
#     def test_workflow_post(self):
#         """Test Workflow POST provides a proper Response type."""
#         self.assertIsInstance(workflow_post(), type(Response()))
#
#
# if __name__ == "__main__":
#     unittest.main()
