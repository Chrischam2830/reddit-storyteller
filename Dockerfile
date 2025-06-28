FROM python:3.11

WORKDIR /app

# Copy your project files into the container
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install all your normal requirements EXCEPT moviepy
RUN pip install --no-cache-dir -r requirements.txt

# Remove any old/corrupt moviepy installs (including broken upper/lowercase variants)
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy* && \
    rm -rf /usr/local/lib/python3.11/site-packages/MoviePy*

# Now install the official MoviePy release from PyPI
RUN pip install --force-reinstall --no-cache-dir moviepy

# Show the files so you can confirm editor.py exists
RUN ls -l /usr/local/lib/python3.11/site-packages/moviepy

# (Optional) Debug: Run a test import to check for import errors
RUN python -c "from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip; print('MoviePy Editor import OK!')"

# (Continue with your normal commands)
CMD ["python", "main.py"]
