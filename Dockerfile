FROM python:3.11.4-slim as base 

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
COPY . .

EXPOSE 8000
CMD python main.py 