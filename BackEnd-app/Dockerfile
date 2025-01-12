# Use Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the backend port (8001)
EXPOSE 8001

# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--reload"]
