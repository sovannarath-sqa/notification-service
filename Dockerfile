# Step 1: Use the official Python 3.11 slim image as the base image
FROM python:3.11-slim

# Step 2: Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Step 5: Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the Django project files into the container
COPY . /app/

# Step 7: Collect static files (optional, but recommended for production)
#RUN python manage.py collectstatic --noinput

# Expose port 8000 for the application
EXPOSE 8000

# Step 8: Set the default command to run the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "notifications.wsgi:application"]
