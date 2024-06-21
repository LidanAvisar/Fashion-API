FROM python:3.11-slim

# Update the package list and install libgl1-mesa-glx and libglib2.0-0 for OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# we first copying only the requirements.txt file to leverage Docker's cache
COPY requirements.txt ./
RUN pip install --no-cache-dir --default-timeout=480 --retries=5 torch==2.2.0
RUN pip install --no-cache-dir --default-timeout=240 --retries=5 -r requirements.txt

COPY . .

EXPOSE 8000

# the directory where app.py is located
WORKDIR /app/similar_recommendation

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
