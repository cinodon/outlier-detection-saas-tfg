from unittest.mock import patch
import unittest
import sys
import os
import pandas as pd

# add dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.data_processing import save_to_csv

class TestSaveCSV(unittest.TestCase):

    def setUp(self):
        # Simulated DataFrame to be saved
        data = {
            'workappid': [339125453961521899744304000625562202634],
            'workappcategoryid': [9],
            'userid': [269060504179808300657734787876250564146],
            'usermanagerid': [-1],
            'usertypeofworkid': [11.0],
            'userroleid': [3],
            'permissionlevelid': [-1],
            'permissionlevelisprivileged': [-1],
            'usersgroupids': ['{NULL}']
        }
        self.df = pd.DataFrame(data)

    @patch('modules.data_processing.pd.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        # Mocking csv_file to not overwritten file
        output_path = "test_output.csv"

        # Call function
        save_to_csv(self.df, output_path)

        # Assert that is called with right arguments
        mock_to_csv.assert_called_once_with(output_path, header=True, index=False)

        # Print message?

if __name__ == '__main__':
    unittest.main()


