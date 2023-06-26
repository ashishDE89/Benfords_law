import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect, url_for, flash,session
from flask_cors import CORS
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

def validate_file_extension(filename):
    
    #Validates if the uploaded file has a valid CSV extension.
    
    allowed_extensions = ['.csv']
    return any(filename.lower().endswith(ext) for ext in allowed_extensions)

def calculate_benford_distribution(data):
    digit_counts = [0] * 9

    for row in data:
        value = str(row)  
        first_digit = int(value[0])

        if first_digit != 0:
            digit_counts[first_digit - 1] += 1

    total_counts = sum(digit_counts)
    benford_distribution = [count / total_counts * 100 for count in digit_counts]

    return benford_distribution

def validate_benford_law(data):
    observed_distribution = calculate_benford_distribution(data)
    expected_distribution = [np.log10(1 + 1 / d) * 100 for d in range(1, 10)]

    return observed_distribution, expected_distribution

def process_file(file_path):
    """
    Processes the uploaded file and extracts the values from the target column.
    Returns a list of cleaned numeric values and the expected distribution based on Benfords law.
    """
    try:
        # Read the file using pandas
        file_path = os.path.join('uploads', 'census_2009b.csv')
        with open(file_path) as file:
                dialect = csv.Sniffer().sniff(file.read(1024))
                delimiter = dialect.delimiter
        # Load the CSV file with the inferred delimiter
        df = pd.read_csv(file_path,delimiter=delimiter)
        # Check if the target column exists
        if '7_2009' not in df.columns:
            print("targetcolumn empty")
            flash("Target column '7_2009' not found in the file.")
            return None, None

        # Extract values from the target column
        values = df['7_2009'].dropna().astype(float).tolist()
        # Calculate the expected distribution based on Benford's law
        total_count = len(values)
        observed_values,expected_counts=validate_benford_law(values)

        return observed_values, expected_counts
    except Exception as e:
        flash(f"Error processing file: {str(e)}")
        return None, None


def plot_distribution(observed_data, expected_counts):
    """
    Plots the observed distribution of numbers and the expected distribution based on Benford's law.
    """
    observed_counts = [observed_data.count(i) for i in range(1, 10)]

    # Plotting the bar chart
    plt.bar(range(1, 10), observed_counts, label='Observed', alpha=0.7)
    plt.plot(range(1, 10), expected_counts, 'ro-', label='Expected')
    plt.xlabel('Leading Digit')
    plt.ylabel('Count')
    plt.title("Benford's Law Distribution")
    plt.legend()
    plt.xticks(range(1, 10))
    plt.grid(True)
    plt.savefig('static/distribution.png')
    print("plot save")
    plt.close()


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file uploaded.')
            return render_template('error.html',error_message='No file uploaded.')

        file = request.files['file']

        # Validate file extension
        if not validate_file_extension(file.filename):
            flash('Invalid file extension. Only CSV files are allowed.')
            return render_template('error.html',error_message='Invalid file extension. Only CSV files are allowed.')

        # Save the file
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Process the file
        values, expected_counts = process_file(file_path)
        if values is None or expected_counts is None:
            return render_template('error.html',error_message='Error in processing the file')

        # Plot the distribution
        plot_distribution(values, expected_counts)

        return render_template('result.html', expected_counts=expected_counts,observed_counts=values)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

        