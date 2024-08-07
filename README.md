# Data Processing Class

This Python class provides functionalities for handling and manipulating data, particularly for loading data from CSV files and performing various operations like querying, adding, and deleting data entries.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Class Methods](#class-methods)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The `DataProcessor` class is designed to simplify the process of loading data from CSV files and managing that data within your application. It supports operations such as adding and deleting data entries, selecting data based on specific criteria, and retrieving basic information about the data.

## Installation

To use this class, you need to have Python installed. You can install the required dependencies using pip:

```bash
pip install pandas
```

## Usage

Here's how you can use the `DataProcessor` class:

1. Import the necessary libraries.
2. Instantiate the `DataProcessor` class.
3. Call methods to perform desired operations.

## Class Methods

### `upload_data(data_path, index_col, columns=None)`

- **Description**: Loads data from a CSV file into the database.
- **Parameters**:
  - `data_path`: Path to the CSV file.
  - `index_col`: The column name to use as the index.
  - `columns`: Optional list of column names to include in the dictionary. If `None`, all columns except the index column will be included.

### `get_length()`

- **Description**: Returns the number of rows in the data.

### `get_width()`

- **Description**: Returns the number of columns in the data.

### `get_data_by_index(index)`

- **Description**: Retrieves a data item by its index.
- **Parameters**:
  - `index`: The index of the data item to retrieve.

### `select_by_judgement(judgement)`

- **Description**: Selects data based on given judgment criteria.
- **Parameters**:
  - `judgement`: A dictionary containing the criteria to match.

### `add_data(data=None, header=None, message="Add: ___")`

- **Description**: Adds data to the buffer.
- **Parameters**:
  - `data`: The data to add.
  - `header`: The header for the data.
  - `message`: Message for the addition operation.

### `delete_element(index, message="Delete: ___")`

- **Description**: Deletes an element at a specified index.
- **Parameters**:
  - `index`: The index of the element to delete.
  - `message`: Message for the deletion operation.

### `commit()`

- **Description**: Applies all changes stored in the buffer to the data.

### `print_change()`

- **Description**: Prints all changes stored in the buffer.

### `print_data()`

- **Description**: Prints the entire data content.

## Examples

Here's an example of how to use the `DataProcessor` class:

```python
from database.main import DataBase
# Instantiate the DataProcessor
processor = DataBase()
# Load data from a CSV file
processor.upload_data('path/to/your/data.csv', 'id')
#Get the length and width of the data
print(processor.get_length())
print(processor.get_width())
# Retrieve data by index
data_item = processor.get_data_by_index(0)
#Select data based on conditions
selected_data = processor.select_by_judgement({'key': '$+5>10'})
#Add data
processor.add_data({'key': 'value'}, 'new_header', 'Added new data')
#Delete an element
processor.delete_element(0)
#Commit changes
processor.commit()
#Print changes
processor.print_change()
#Print data
processor.print_data()
```



## Contributing

Contributions are welcome! Please open an issue or create a pull request to suggest improvements or report bugs.

## License

MIT LICENSE
