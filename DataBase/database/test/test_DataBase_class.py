import unittest
import os
from datetime import datetime
from database.main import DataBase 

class TestDataBase(unittest.TestCase):

    def setUp(self):
        self.db = DataBase()
        self.test_data_path = 'test_data.csv'
        self.index_col = 'id'
        self.columns = ['name', 'age']
        # create test data
        with open(self.test_data_path, 'w') as f:
            f.write('id,name,age\n')
            f.write('1,Alice,25\n')
            f.write('2,Bob,30\n')

    def tearDown(self):
        # delete test data
        os.remove(self.test_data_path)

    def test_upload_from_csv(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        self.assertEqual(self.db.length, 2)
        self.assertEqual(self.db.width, 2)
        self.assertEqual(self.db.index_col, self.index_col)
        self.assertEqual(self.db.columns, self.columns)

    def test_get_length(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        self.assertEqual(self.db.get_length(), 2)

    def test_get_width(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        self.assertEqual(self.db.get_width(), 2)

    def test_get_data_by_index(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        data = self.db.get_data_by_index(0)
        expected = (1, {'age': 25, 'name': 'Alice'})
        self.assertEqual(data, expected)

    def test_get_data_by_header(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        data = self.db.get_data_by_header(1)
        self.assertEqual(data, {'name': 'Alice', 'age': 25})

    def test_select_by_judgement(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        judgement = {'age': '$*2<=60'}
        results = self.db.select_by_judgement(judgement)
        self.assertEqual(len(results), 2)

    def test_add_data(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        data = {'name': 'Charlie', 'age': '35'}
        self.db.add_data(data=data, header='3')
        self.db.commit()
        self.assertEqual(self.db.get_data_by_index(2), ('3', {'name': 'Charlie', 'age': '35'}))

    def test_delete_element(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        self.db.delete_element(0)
        self.db.commit()
        self.assertEqual(self.db.get_length(), 1)

    def test_update_data(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        data = {'name': 'Charlie', 'age': '35'}
        self.db.update_data(0,message="Update: Alice", data=data)
        self.db.commit()
        self.assertEqual(self.db.get_data_by_index(0), (1, {'name': 'Charlie', 'age': '35'}))

    def test_get_average_data(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        average_age = self.db.get_average_data('age')
        self.assertEqual(average_age, 27.5)

    def test_sort_data_reverse_True(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        self.db.sort_data('age', reverse=True)
        self.assertEqual(self.db.get_data_by_index(0), (1, {'age': 25, 'name': 'Alice'}))

    def test_sort_data_reverse_False(self):
        self.db.upload_from_csv(self.test_data_path, self.index_col, self.columns)
        self.db.sort_data('age', reverse=False)
        self.assertEqual(self.db.get_data_by_index(0), (1, {'name': 'Alice', 'age': 25}))

if __name__ == '__main__':
    unittest.main()
