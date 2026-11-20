FROM mcr.microsoft.com/playwright/python:v1.49.1-noble

WORKDIR /tests
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["pytest"]
