FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

ENV PATH="/opt/venv/bin:$PATH"
CMD ["python", "app.py"] 