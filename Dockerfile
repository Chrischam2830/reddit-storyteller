FROM python:3.11

WORKDIR /app
COPY . /app

# Install ImageMagick and a basic font (required for TextClip)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        imagemagick \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Fix ImageMagick security policy to allow writing/reading files (for TextClip)
RUN sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/g' /etc/ImageMagick-6/policy.xml || true \
 && sed -i 's/rights="none" pattern="PS"/rights="read|write" pattern="PS"/g' /etc/ImageMagick-6/policy.xml || true \
 && sed -i 's/rights="none" pattern="EPI"/rights="read|write" pattern="EPI"/g' /etc/ImageMagick-6/policy.xml || true \
 && sed -i 's/rights="none" pattern="XPS"/rights="read|write" pattern="XPS"/g' /etc/ImageMagick-6/policy.xml || true \
 && sed -i 's/rights="none" pattern="SVG"/rights="read|write" pattern="SVG"/g' /etc/ImageMagick-6/policy.xml || true \
 && sed -i 's/rights="none" pattern="MSL"/rights="read|write" pattern="MSL"/g' /etc/ImageMagick-6/policy.xml || true \
 && sed -i 's/rights="none" pattern="MVG"/rights="read|write" pattern="MVG"/g' /etc/ImageMagick-6/policy.xml || true \
 && sed -i 's/rights="none" pattern="MNG"/rights="read|write" pattern="MNG"/g' /etc/ImageMagick-6/policy.xml || true \
 && sed -i 's/rights="none" pattern="TXT"/rights="read|write" pattern="TXT"/g' /etc/ImageMagick-6/policy.xml || true

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Remove MoviePy (if present) and force correct install order
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy* && \
    rm -rf /usr/local/lib/python3.11/site-packages/MoviePy*

RUN pip install --force-reinstall --no-cache-dir moviepy==1.0.3
RUN pip install --force-reinstall --no-cache-dir pillow==9.5.0

# (Optional sanity check)
RUN python -c "from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip; print('MoviePy Editor import OK!')"

CMD ["python", "main.py"]
