import unittest
import pymysql as mysql
from uvprov_api.utils.db import connect_DB


class DBTestCase(unittest.TestCase):
    """Test for DB connection."""

    def setUp(self):
        """Set up test fixtures."""

    def test_connection(self):
        """Test connection."""
        cursor = connect_DB()
        if isinstance(cursor, mysql.cursors.DictCursor):
            self.assertRaises(Exception)
        else:
            pass
