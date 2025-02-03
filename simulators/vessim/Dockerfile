# Use a lightweight Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY storage.py .
COPY wrapper.py .

# Install dependencies
RUN pip install --no-cache-dir flask loguru

# Expose the API port
EXPOSE 5000

# Run the Flask app
CMD ["python", "wrapper.py"]
