FROM python:3.11

WORKDIR /app
COPY . /app

# Install ImageMagick and fonts
RUN apt-get update && \
    apt-get install -y --no-install-recommends imagemagick fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

# Overwrite the security policy
RUN cat > /etc/ImageMagick-6/policy.xml <<EOF
<policymap>
  <policy domain="coder" rights="read|write" pattern="*" />
</policymap>
EOF

# Upgrade pip, install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Clean and force install MoviePy and Pillow versions
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy* && \
    rm -rf /usr/local/lib/python3.11/site-packages/MoviePy* && \
    pip install --force-reinstall --no-cache-dir moviepy==1.0.3
RUN pip install --force-reinstall --no-cache-dir pillow==9.5.0

# (Optional) Test the MoviePy install
RUN python -c "from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip; print('MoviePy Editor import OK!')"

CMD ["python", "main.py"]
