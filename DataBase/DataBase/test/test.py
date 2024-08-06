import unittest
from DataBase.database.main import DataBase

class TestDataBase(unittest.TestCase):

    def setUp(self):
        self.db = DataBase()

    def test_upload_from_csv_valid_path(self):
        data_path = "./students.csv"  # Replace with a valid CSV file path
        index_col = "name"  # Replace with the index column name
        columns = ["score", "place"]  # Replace with actual column names
        self.db.upload_from_csv(data_path, index_col, columns)
        self.assertGreater(self.db.length, 0, "Database length should be greater than 0 after upload.")
        self.assertEqual(self.db.index_col, index_col, "Index column should match the provided index column.")
        self.assertEqual(self.db.columns, columns, "Columns should match the provided columns.")

    def test_upload_from_csv_invalid_path(self):
        data_path = None
        index_col = "id"
        columns = ["column1", "column2"]
        with self.assertRaises(ValueError):
            self.db.upload_from_csv(data_path, index_col, columns)

    def test_upload_from_csv_nonexistent_file(self):
        data_path = "nonexistent_file.csv"  # Replace with a path that does not exist
        index_col = "id"
        columns = ["column1", "column2"]
        with self.assertRaises(FileNotFoundError):
            self.db.upload_from_csv(data_path, index_col, columns)

    def test_get_length(self):
        # Assuming that upload_from_csv has been called previously
        length = self.db.get_length()
        self.assertIsInstance(length, int, "Length should be an integer.")
        self.assertGreaterEqual(length, 0, "Length should be greater than or equal to 0.")

    def test_get_width(self):
        # Assuming that upload_from_csv has been called previously
        width = self.db.get_width()
        self.assertIsInstance(width, int, "Width should be an integer.")
        self.assertGreaterEqual(width, 0, "Width should be greater than or equal to 0.")

    def test_get_data_by_index_valid(self):
        # Assuming that upload_from_csv has been called previously
        index = 0  # Replace with a valid index
        data = self.db.get_data_by_index(index)
        self.assertIsNotNone(data, "Data should not be None for a valid index.")

    def test_get_data_by_index_invalid(self):
        index = -1  # Replace with an invalid index
        with self.assertRaises(IndexError):
            self.db.get_data_by_index(index)

    def test_get_data_by_header_valid(self):
        # Assuming that upload_from_csv has been called previously
        header_name = "student1"  # Replace with a valid header name
        data = self.db.get_data_by_header(header_name)
        self.assertIsNotNone(data, "Data should not be None for a valid header name.")

    def test_get_data_by_header_invalid(self):
        header_name = "invalid_header"  # Replace with an invalid header name
        with self.assertRaises(ValueError):
            self.db.get_data_by_header(header_name)

    # Add more tests for other methods of the DataBase class as needed

if __name__ == '__main__':
    unittest.main()
