FROM python:3.11

WORKDIR /app
COPY . /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends imagemagick fonts-dejavu-core fonts-freefont-ttf fontconfig wget && \
    rm -rf /var/lib/apt/lists/*

# Fix ImageMagick policy.xml (use echo with line breaks and >)
RUN mkdir -p /etc/ImageMagick-6 && \
    echo '<policymap>'                                      > /etc/ImageMagick-6/policy.xml && \
    echo '  <policy domain="resource" name="memory" value="4GiB"/>'    >> /etc/ImageMagick-6/policy.xml && \
    echo '  <policy domain="resource" name="map" value="8GiB"/>'       >> /etc/ImageMagick-6/policy.xml && \
    echo '  <policy domain="resource" name="width" value="32KP"/>'     >> /etc/ImageMagick-6/policy.xml && \
    echo '  <policy domain="resource" name="height" value="32KP"/>'    >> /etc/ImageMagick-6/policy.xml && \
    echo '  <policy domain="resource" name="area" value="256MP"/>'     >> /etc/ImageMagick-6/policy.xml && \
    echo '  <policy domain="resource" name="disk" value="20GiB"/>'     >> /etc/ImageMagick-6/policy.xml && \
    echo '  <policy domain="coder" rights="read|write" pattern="*"/>'  >> /etc/ImageMagick-6/policy.xml && \
    echo '  <policy domain="path" rights="read|write" pattern="@*"/>'  >> /etc/ImageMagick-6/policy.xml && \
    echo '</policymap>'                                    >> /etc/ImageMagick-6/policy.xml

RUN pip install --upgrade pip

# Install Python requirements and MoviePy fixes
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
