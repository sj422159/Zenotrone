# Use Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all files to the container
COPY . .

# Install dependencies (including uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask/Uvicorn runs on
EXPOSE 5000

# Run the application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
