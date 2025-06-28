FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

# Install all Python dependencies except moviepy
RUN pip install --no-cache-dir -r requirements.txt

# Now install moviepy directly from the official GitHub source
RUN pip install git+https://github.com/Zulko/moviepy.git

# (Optional) Run your debug to verify
RUN python debug.py

CMD ["python", "main.py"]
