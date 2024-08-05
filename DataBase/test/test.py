import sys
import os
from unittest.mock import patch, mock_open
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.main import DataBase

class TestDataBase(unittest.TestCase):

    def setUp(self):
        self.db = DataBase()

    @patch('builtins.open', new_callable=mock_open, read_data='index,col1,col2\n0,1,2\n1,2,3')
    def test_upload_from_csv(self, mock_file):
        self.db.upload_from_csv('test/students.csv', 'index', ['col1', 'col2'])
        self.assertEqual(self.db.get_length(), 2)
        self.assertEqual(self.db.get_width(), 2)
        self.assertEqual(self.db.index_col, 'index')
        self.assertEqual(self.db.columns, ['col1', 'col2'])

    def test_get_length(self):
        self.assertEqual(self.db.get_length(), 0)

    def test_get_width(self):
        self.assertEqual(self.db.get_width(), 0)

    @patch('builtins.open', new_callable=mock_open, read_data='index,col1,col2\n0,1,2\n1,2,3')
    def test_get_data_by_index(self, mock_file):
        self.db.upload_from_csv('test/students.csv', 'index', ['col1', 'col2'])
        data = self.db.get_data_by_index(0)
        self.assertEqual(data, (0, {'col1': 1, 'col2': 2}))  # 确保索引为整数

    @patch('builtins.open', new_callable=mock_open, read_data='index,col1,col2\n0,1,2\n1,2,3')
    def test_select_by_judgement(self, mock_file):
        self.db.upload_from_csv('test/students.csv', 'index', ['col1', 'col2'])
        result = self.db.select_by_judgement({'col1': '$>1'})
        expected = [[1, {'col1': 2, 'col2': 3}]]
        self.assertEqual(result, expected)
    def test_add_data(self):
        self.db.add_data(data={'col1': '4', 'col2': '5'}, header='2')
        self.db.commit()
        self.assertEqual(self.db.get_length(), 1)

    @patch('builtins.open', new_callable=mock_open, read_data='index,col1,col2\n0,1,2\n1,2,3')
    def test_delete_element(self, mock_file):
        self.db.upload_from_csv('test/students.csv', 'index', ['col1', 'col2'])
        self.db.delete_element(0)
        self.db.commit()  # 确保更改被提交
        self.assertEqual(self.db.get_length(), 1)

if __name__ == '__main__':
    unittest.main()