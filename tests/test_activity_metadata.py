from uvprov_api.uv.activity_metadata import activity_get_output, ActivityGraph
import unittest
from mock import patch


class WorkflowGraphTest(unittest.TestCase):
    """Test for Activity Response from API."""

    def setUp(self):
        """Set up test fixtures."""
        # self.data = WorkflowGraph()
        # self.workflow_graph = self.data.workflow('2017-01-17T14:14:14Z')

    def tearDown(self):
        """Tear down test fixtures."""
        pass

    @patch('uvprov_api.uv.activity_metadata.connect_DB')
    @patch('uvprov_api.uv.activity_metadata.empty_activities_DB')
    @patch.object(ActivityGraph, 'activity')
    def test_activity_get_output(self, mock, empty_DB, db_mock):
        """Test Activity processing."""
        activity_get_output()
        self.assertTrue(mock.called)


if __name__ == "__main__":
    unittest.main()
