FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

# Debug: what's there before anything is installed?
RUN ls -l /usr/local/lib/python3.11/site-packages/ || true

RUN pip install --no-cache-dir -r requirements.txt

# Remove all moviepy ghosts
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy* \
 && rm -rf /usr/local/lib/python3.11/site-packages/MoviePy*

# Debug: after nuke
RUN ls -l /usr/local/lib/python3.11/site-packages/ || true

# Install MoviePy directly, forcibly, with no cache
RUN pip install --force-reinstall --no-cache-dir git+https://github.com/Zulko/moviepy.git

# Debug: what's in the moviepy directory now?
RUN ls -l /usr/local/lib/python3.11/site-packages/moviepy

RUN python debug.py

CMD ["python", "main.py"]
