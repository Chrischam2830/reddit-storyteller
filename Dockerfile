FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install system dependencies: ImageMagick and fonts
RUN apt-get update && \
    apt-get install -y --no-install-recommends imagemagick fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

# UNLOCK ImageMagick security policies for MoviePy text support
RUN for pattern in PDF PS EPI XPS SVG MSL MVG MNG TXT; do \
      sed -i "s/rights=\"none\" pattern=\"$pattern\"/rights=\"read|write\" pattern=\"$pattern\"/g" /etc/ImageMagick-6/policy.xml || true; \
    done

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies from your requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Force reinstall MoviePy 1.0.3 (and its dependencies) to avoid conflicts
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy* && \
    rm -rf /usr/local/lib/python3.11/site-packages/MoviePy* && \
    pip install --force-reinstall --no-cache-dir moviepy==1.0.3

# Force reinstall Pillow 9.5.0 to ensure compatibility
RUN pip install --force-reinstall --no-cache-dir pillow==9.5.0

# (Optional) Test the MoviePy + ImageMagick install (remove if not needed)
RUN python -c "from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip; print('MoviePy Editor import OK!')"

# Set the default command (change this if your entrypoint is different)
CMD ["python", "main.py"]
