FROM python:3.11

WORKDIR /app
COPY . /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends imagemagick fonts-dejavu-core fonts-freefont-ttf fontconfig wget && \
    rm -rf /var/lib/apt/lists/*

# Fix ImageMagick policy
RUN cat > /etc/ImageMagick-6/policy.xml <<EOF
<policymap>
  <policy domain="resource" name="memory" value="2GiB"/>
  <policy domain="resource" name="map" value="4GiB"/>
  <policy domain="resource" name="width" value="16KP"/>
  <policy domain="resource" name="height" value="16KP"/>
  <policy domain="resource" name="area" value="128MP"/>
  <policy domain="resource" name="disk" value="10GiB"/>
  <policy domain="coder" rights="read|write" pattern="*" />
  <policy domain="path" rights="read|write" pattern="@*" />
</policymap>
EOF

RUN pip install --upgrade pip

# Install requirements and moviepy fixes
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy* && \
    rm -rf /usr/local/lib/python3.11/site-packages/MoviePy* && \
    pip install --force-reinstall --no-cache-dir moviepy==1.0.3
RUN pip install --force-reinstall --no-cache-dir pillow==9.5.0

# Download subway.mp4 from Google Drive using bash script
ADD download_gdrive.sh /app/download_gdrive.sh
RUN chmod +x /app/download_gdrive.sh && \
    /app/download_gdrive.sh "1IBRp3tl-dc1sJQlB0md5OZMmt4WCwMrF" "/app/subway.mp4"

# Test MoviePy import
RUN python -c "from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip; print('MoviePy Editor import OK!')"

CMD ["python", "main.py"]
