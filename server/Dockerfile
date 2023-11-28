# Use the official Python image as the base image
FROM python:3.8.2

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# Install netcat for database health check
RUN apt-get update \
    && apt-get install -y netcat

# Set the working directory in the container
ENV APP=/app
WORKDIR $APP

# Copy the requirements file to the working directory
COPY requirements.txt $APP/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
# Copy the application code to the container
COPY . $APP/

# Expose port 8000
EXPOSE 8000

# Make entrypoint.sh executable
RUN chmod +x $APP/entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["/bin/bash", "$APP/entrypoint.sh"]

# Default command to run the application using Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]