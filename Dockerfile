# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

COPY . .

# Install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

# Define the command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

 


