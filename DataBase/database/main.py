import pandas
import time
class DataBase:
    def __init__(self, name=None):
        self.data = {}
        self.length = 0
        self.buffer = {}  # flush area
        self.time = 0  # the change times
        self.width = 0
        self.index_col = None
        self.columns = None
        self.data_path = None

    def upload_from_csv(self, data_path, index_col, columns):
        import os
        import pandas as pd
        self.data_path = data_path
        if data_path is None:
            raise ValueError("Invalid path")

        """
               Uploads data from a CSV file into the database.

               Parameters:
               - data_path: Path to the CSV file.
               - index_col: The column name to use as the index.
               - columns: Optional list of column names to include in the dictionary.
                          If None, all columns except the index column will be included.
               """
        if data_path is None:
            raise ValueError("Invalid path")

        if not os.path.exists(data_path):
            raise FileNotFoundError(f"The file '{data_path}' does not exist.")

        df = pd.read_csv(data_path)

        # Set the index column
        df.set_index(index_col, inplace=True)

        # Select only the specified columns if provided
        if columns is not None:
            df = df[columns]

        # Convert DataFrame to dictionary
        self.data = df.to_dict(orient='index')
        self.width = len(df.columns)
        self.length = len(self.data)
        self.index_col=index_col
        self.columns=columns

        # write the data into history/history.txt
        try:
            localtime = time.localtime(time.time())
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", localtime)

            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "history", "history.txt")
            with open(file_path, mode="a") as history_file:
                history_file.write(f"{formatted_time}\n")
                history_file.write(f"{self.data_path}\n")
                history_file.write(f"{self.index_col}, {self.columns}\n")
                history_file.write(f"{self.length}\n")
                history_file.write(f"{self.time}\n")
                history_file.write(f"{self.data}\n")
                history_file.write("=====================\n")
        except Exception as e:
            print(f"Error writing to history file: {e}")

    def get_length(self):
        # get the length
        return self.length

    def get_width(self):
        # get the length
        return self.width

    def get_data_by_index(self, index):
        if not isinstance(index, int):
            raise IndexError("Index must be integer.")

        if index < 0 or index >= self.length:
            raise IndexError(f"Index must be from 0 to {self.length - 1}")

        return list(self.data.items())[index]

    def get_data_by_header(self, header):
        # get the data by the header.
        if not header in self._get_headers():
            raise ValueError(f"{header} not in the columns")

        return self.data[header]
    
    def _get_headers(self):
        return [header for header in self.data]

    def _get_columns(self):
        return [col_name for col_name in self.columns+[self.index_col]]

    def select_by_judgement(self, judgement: dict):
        """
        Selects data based on the given judgement criteria.

        Parameters:
        - judgement: A dictionary containing the criteria to match.
                     Example: {"key": "$+5>10", "col1": "$*2<=100"}.

        Returns:
        - A list of dictionaries, where each dictionary represents a data entry that matches the criteria.
        """

        if not isinstance(judgement, dict):
            raise ValueError("Judgement must be dict")

        if not judgement:  # Handle empty dictionary
            return []

        # Check if the keys in judgement are valid
        if not set(judgement.keys()).issubset(self.columns + [self.index_col]):
            raise ValueError("Not match key.")

        # Parse conditions and evaluate
        results = []
        for key, value in self.data.items():
            if all(self._evaluate_condition(value, k, v) for k, v in judgement.items()):
                results.append([key,value])

        return results

    def _evaluate_condition(self, data_entry, key, condition):
        """
        Evaluates whether the given condition is satisfied by the data entry.

        Parameters:
        - data_entry: A dictionary representing a single data entry.
        - key: The key in the data_entry to use for evaluation.
        - condition: The string condition to evaluate.

        Returns:
        - True if the condition is satisfied, False otherwise.
        """

        # Replace '$' with the actual value from the data entry
        value = data_entry.get(key)

        # Handle None values
        if value is None:
            return False

        # Check if the value is a string and we need to compare the first character
        if isinstance(value, str) and condition.startswith("'$[0]=="):
            condition = f"'{value[0]}' == {condition[5:-1]}"  # Extract the comparison value and create a new condition
        else:
            safe_condition = condition.replace("$", str(value))

        # Define a safe context for evaluation
        safe_dict = {'__builtins__': None}

        try:
            # Evaluate the condition safely
            return eval(safe_condition, safe_dict)
        except Exception as e:
            print(f"Error evaluating condition '{condition}': {e}")
            return False

    def add_data(self, data=None, header=None, message="Add: ___"):
        # add the data to the buffer.
        self.buffer[self.time] = {
            "time": self.time + 1,
            "To do": "Add",
            "Message": message,
            "Position": self.length,
            "header":header,
            "data": data,
            "local time": time.perf_counter()
        }
        self.time += 1

    def delete_element(self, index, message="Delete: ___"):
        if not isinstance(index, int):
            raise IndexError("Index must be integer.")

        if index < 0 or index >= self.length:
            raise IndexError(f"Index must be from 0 to {self.length - 1}")

        self.buffer[self.time] = {
            "time": self.time + 1,
            "To do": "Delete",
            "Message": message,
            "Position": index,  # Fixed: Use the correct variable name
            "data": list(self.data.values())[index],
            "local time": time.perf_counter()
        }
        self.time += 1

    def update_data(self, index, message="Update: ___", data=None):
        if not isinstance(index, int):
            raise IndexError("Index must be integer.")

        if data is None:
            raise ValueError("Data must be provided.")

        if index < 0 or index >= self.length:
            raise IndexError(f"Index must be from 0 to {self.length - 1}")

        self.buffer[self.time] = {
            "time": self.time + 1,
            "To do": "Update",
            "Message": message,
            "Position": index,  # Fixed: Use the correct variable name
            "header": list(self.data.keys())[index],
            "data": data,
            "local time": time.perf_counter()
        }

        self.time += 1
    def commit(self):
        for change in self.buffer.values():
            if change["To do"] == "Add":
                self._add_data(change)
            elif change["To do"] == "Delete":
                self._delete_data(change)
            elif change["To do"] == "Update":
                self._update_data(change)
            elif change["To do"] == "Merge":
                self._merge_data(change)
        # Clear buffer after applying changes
        try:
            import os
            localtime = time.localtime(time.time())
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "history", "history.txt")
            with open(file_path, mode="a") as history_file:
                history_file.write(f"{formatted_time}\n")
                history_file.write(f"{self.data_path}\n")
                history_file.write(f"{self.index_col}, {self.columns}\n")
                history_file.write(f"{self.length}\n")
                history_file.write(f"{self.time}\n")
                history_file.write(f"{self.data}\n")
                history_file.write("=====================\n")
        except Exception as e:
            print(f"Error writing to history file: {e}")
        self.buffer.clear()

    def _add_data(self, change):
        if not isinstance(change["data"], dict):
            raise ValueError("Data should be a dictionary with keys matching the columns.")

        # Add the data to the internal storage
        self.data[change["header"]] = change["data"]
        self.length += 1

    def _delete_data(self, change):
        del self.data[list(self.data.keys())[change["Position"]]]
        self.length -= 1

    def _update_data(self, change):
        if not isinstance(change["data"], dict):
            raise ValueError("Data should be a dictionary with keys matching the columns.")

        if not set(change["data"]).issubset(self.columns+[self.index_col]):
            raise ValueError(f"Wrong match keys: { change['data'].keys() }")

        self.data[change["header"]] = change["data"]

    def get_index_by_header(self, header):
        if not header in self._get_headers():
            raise ValueError(f"Wrong Header Name {header}")

        index = 0
        for di in self.data:
            if di == header:
                return index
            index += 1

    def merge_data(self, DataBase_object, message="Merge___"):
        self.buffer[self.time] = {
            "time": self.time + 1,
            "To do": "Merge",
            "Message": message,
            "Position": self.length,  # Fixed: Use the correct variable name
            "data": DataBase_object,
            "local time": time.perf_counter()
        }
        self.time += 1

    def _merge_data(self, change):
        if not isinstance(change["data"], DataBase):
            raise ValueError("Data should be a DataBase object.")

        # if not (change["data"].index_col == self.index_col and change["data"].columns == self.columns):
        #     raise ValueError("DataBase object should have the same index_col and columns as the current DataBase.")

        for di in change["data"].data:
            self.data[di] = change["data"].data[di]

        self.length += change["data"].length

    def print_change(self):
        for change in self.buffer.values():
            print(change)

    def print_data(self):
        for d in self.data:
            print(f"{d} : {self.data[d]}")
