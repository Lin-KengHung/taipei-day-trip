# Start with a Python base image
FROM python:3.10.11

# Set the working directory to /app
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt requirements.txt
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]