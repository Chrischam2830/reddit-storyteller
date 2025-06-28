# Use official Python image
FROM python:3.11

# Set work directory
WORKDIR /app

# Copy everything
COPY . /app

# Install ImageMagick and DejaVu font (needed for MoviePy TextClip)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        imagemagick \
        fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

# FIX ImageMagick security policy for 'TXT' files (needed for MoviePy caption)
RUN sed -i 's/rights="none" pattern="TXT"/rights="read|write" pattern="TXT"/g' /etc/ImageMagick-6/policy.xml || true

# Upgrade pip
RUN pip install --upgrade pip

# Install regular requirements
RUN pip install --no-cache-dir -r requirements.txt

# Remove any pre-existing MoviePy (in case)
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy* && \
    rm -rf /usr/local/lib/python3.11/site-packages/MoviePy*

# Reinstall MoviePy (1.0.3 is the most stable for Render + Docker)
RUN pip install --force-reinstall --no-cache-dir moviepy==1.0.3

# (Optional) Force Pillow version, if you know it’s needed for your code
RUN pip install --force-reinstall --no-cache-dir pillow==9.5.0

# (Optional, but recommended) Test that MoviePy works
RUN python -c "from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip; print('MoviePy Editor import OK!')"

# Set the default command (replace with your actual start command)
CMD ["python", "main.py"]
