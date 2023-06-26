# Benford's Law Analysis Web Application

This is a Python-based web application that performs Benford's Law analysis on user-submitted flat files.

Steps taken to handle the data formatting issues:
File Validation: The code assumes that the uploaded file is a CSV file. It checks if the file has a valid CSV extension and reads the file using the csv module. If the file format is incorrect, an error message is displayed to the user.

Column Validation: The code specifically looks for the '7_2009' column in the uploaded file. If the column is not found, an error message is displayed to the user, indicating that the required column is missing.

Data Cleaning: The code processes each row of the file and extracts the values from the '7_2009' column. It attempts to convert the values to float type using try-except blocks. If a value cannot be converted to float or is missing, it is skipped. This approach handles non-numeric values and missing values in the '7_2009' column.

Error Handling: The code utilizes try-except blocks to catch and handle potential errors. If any error occurs during file processing or data analysis, an error message is displayed to the user, indicating the nature of the error.

## Prerequisites

- Python 3.9 or later
- Docker (optional)

## Installation

1. Clone the repository

2. Install the Python dependencies:
pip install -r requirements.txt


## Usage

1. Run the application:
python app.py

2. Access the application in your web browser at `http://localhost:5000`.

3. Upload a flat file for analysis. The application will validate Benford's assertion based on the target column and display a graph of the observed distribution compared to the expected distribution.

4. Perform another analysis by clicking the "Perform another analysis" link.

## Docker Support

To run the application in a Docker container, follow these steps:

1. Build the Docker image:
docker build -t benfords-law-app .


2. Run the Docker container:
docker run -p 5000:5000 benfords-law-app

3. Access the application in your web browser at `http://localhost:5000`.

## License

This project is licensed under the [MIT License](LICENSE).




