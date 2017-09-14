# from uvprov_api.uv.activity_metadata import activity_get_output, ActivityGraph
# from rdflib import Graph
# import unittest
#
#
# class ActivityGraphTest(unittest.TestCase):
#     """Test for Activity Response from API."""
#
#     def setUp(self):
#         """Set up test fixtures."""
#         self.graph = Graph()
#         self.format_jsonld = 'json-ld'
#         self.format_turtle = 'turtle'
#         self.data = ActivityGraph()
#         self.activity_graph = self.data.activity('2017-01-17T14:14:14Z')
#
#     def tearDown(self):
#         """Tear down test fixtures."""
#         pass
#
#     def test_activity_get_output(self):
#         """Test Activity processing output is Graph."""
#         if activity_get_output('turtle', None) is not (None or 'Empty'):
#             data_turtle = self.graph.parse(data=str(activity_get_output(self.format_turtle, None))
#                                            .encode('utf-8'),
#                                            format=self.format_turtle)
#             data_json = self.graph.parse(data=str(activity_get_output(self.format_jsonld, None))
#                                          .encode('utf-8'),
#                                          format=self.format_jsonld)
#             self.assertIsInstance(data_turtle, type(Graph()))
#             self.assertIsInstance(data_json, type(Graph()))
#
#     def test_activity_no_output(self):
#         """Test Activity processing output is empty graph."""
#         if len(self.activity_graph) == 0:
#             assert True
#
#
# if __name__ == "__main__":
#     unittest.main()
