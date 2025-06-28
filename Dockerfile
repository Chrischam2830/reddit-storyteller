# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy everything to /app in the container
COPY . /app

# Upgrade pip first
RUN pip install --upgrade pip

# Install your app's dependencies (pins Pillow 9.5.0 here, but we'll force again at end)
RUN pip install --no-cache-dir -r requirements.txt

# Remove any possibly pre-installed MoviePy versions, just in case
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy* && \
    rm -rf /usr/local/lib/python3.11/site-packages/MoviePy*

# Install the working MoviePy version (1.0.3)
RUN pip install --force-reinstall --no-cache-dir moviepy==1.0.3

# **CRITICAL STEP**: Force reinstall Pillow 9.5.0 *after* MoviePy, to fix the ANTIALIAS bug
RUN pip install --force-reinstall --no-cache-dir pillow==9.5.0

# (Optional) Sanity check: list MoviePy files
RUN ls -l /usr/local/lib/python3.11/site-packages/moviepy

# (Optional) Test MoviePy import to make sure it works!
RUN python -c "from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip; print('MoviePy Editor import OK!')"

# Default command (adjust as needed)
CMD ["python", "main.py"]
