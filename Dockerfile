# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY app.py .
COPY templates templates
COPY static static
COPY  uploads uploads
# Expose the port the application runs on
EXPOSE 5000

# Start the application
#CMD ["python", "app.py"]
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
