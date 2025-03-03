# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy Flask app
COPY app.py .

# Install Flask
RUN pip install flask

# Expose the port
EXPOSE 9080

# Run the application
CMD ["python", "app.py"]
