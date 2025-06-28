FROM python:3.11

WORKDIR /app
COPY . /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        imagemagick fonts-dejavu-core fonts-freefont-ttf fontconfig wget && \
    rm -rf /var/lib/apt/lists/*

# Fix ImageMagick policy.xml for large images
RUN mkdir -p /etc/ImageMagick-6 && \
    printf '%s\n' '<policymap>
  <policy domain="resource" name="memory" value="4GiB"/>
  <policy domain="resource" name="map" value="8GiB"/>
  <policy domain="resource" name="width" value="32KP"/>
  <policy domain="resource" name="height" value="32KP"/>
  <policy domain="resource" name="area" value="256MP"/>
  <policy domain="resource" name="disk" value="20GiB"/>
  <policy domain="coder" rights="read|write" pattern="*"/>
  <policy domain="path" rights="read|write" pattern="@*"/>
</policymap>' > /etc/ImageMagick-6/policy.xml

RUN pip install --upgrade pip

# Install Python requirements and MoviePy fixes
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --force-reinstall --no-cache-dir moviepy==1.0.3 pillow==9.5.0

# Download subway.mp4 from Google Drive using bash script
ADD download_gdrive.sh /app/download_gdrive.sh
RUN chmod +x /app/download_gdrive.sh && \
    /app/download_gdrive.sh "1IBRp3tl-dc1sJQlB0md5OZMmt4WCwMrF" "/app/subway.mp4"

# Test MoviePy import (optional, for debugging)
RUN python -c "from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip; print('MoviePy Editor import OK!')"

CMD ["python", "main.py"]
