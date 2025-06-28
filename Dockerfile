FROM python:3.11

WORKDIR /app

# Copy code into container
COPY . /app

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Install your main dependencies (except moviepy)
RUN pip install --no-cache-dir -r requirements.txt

# Remove any broken or cached moviepy installs (important!)
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy* && \
    rm -rf /usr/local/lib/python3.11/site-packages/MoviePy*

# Install a working, stable version of moviepy (this will include editor.py!)
RUN pip install --force-reinstall --no-cache-dir moviepy==1.0.3

# Confirm that editor.py is present (this is a debug line, keep it until it works)
RUN ls -l /usr/local/lib/python3.11/site-packages/moviepy

# Debug: try to import from moviepy.editor (will fail the build if broken)
RUN python -c "from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip; print('MoviePy Editor import OK!')"

# Start your app (change this if your entrypoint is different)
CMD ["python", "main.py"]
