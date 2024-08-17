from unittest.mock import Mock
import unittest
import sys
import os

# add dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.data_processing import transform_data


class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        # Query Results
        self.query_results = [
            ('ff212fc9-8777-4551-928e-c8c569a1b20a', 9, '4fc5737a-8624-4549-b594-412196860fb7',
             'ca808231-fab0-4f64-9bbb-52caddc97396', 5, 1, None, None, '{NULL}')
        ]

        # Query Columns
        self.columns = ['workappid','workappcategoryid','userid',
                        'usermanagerid', 'usertypeofworkid','userroleid',
                        'permissionlevelid','permissionlevelisprivileged','usersgroupids']


    def test_transform_data(self):
        # Cursor mock
        cursor = Mock()
        cursor.description = [(col,) for col in self.columns]

        transformed_df = transform_data(self.query_results, cursor)

        # Transform UUID to int
        self.assertEqual(transformed_df['workappid'].iloc[0],
                         339125453961521899744304000625562202634)

        self.assertEqual(transformed_df['userid'].iloc[0],
                         106034236332594801533119361560923738039)

        self.assertEqual(transformed_df['usermanagerid'].iloc[0],
                         269171309819458300501565234849742680982)

        # Null to -1 expected
        self.assertEqual(transformed_df['permissionlevelid'].iloc[0], -1)
        self.assertEqual(transformed_df['permissionlevelisprivileged'].iloc[0], -1)

        # Ignore Groups


if __name__ == '__main__':
    unittest.main()