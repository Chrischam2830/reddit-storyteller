FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

# Install all Python dependencies except moviepy
RUN pip install --no-cache-dir -r requirements.txt

# !!! NEW: Remove any previous moviepy installs/zombie folders
RUN rm -rf /usr/local/lib/python3.11/site-packages/moviepy*

# Now install moviepy directly from GitHub
RUN pip install --no-cache-dir git+https://github.com/Zulko/moviepy.git

RUN python debug.py

CMD ["python", "main.py"]
