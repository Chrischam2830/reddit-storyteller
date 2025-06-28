# Use official python base image
FROM python:3.11

WORKDIR /app

COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install all requirements
RUN pip install -r requirements.txt

# Force-reinstall moviepy just in case (critical fix for your problem)
RUN pip install --force-reinstall --no-cache-dir moviepy

# (Optional) Output installed files for debug
RUN python debug.py

# Start your main app (adjust as needed)
CMD ["python", "main.py"]
