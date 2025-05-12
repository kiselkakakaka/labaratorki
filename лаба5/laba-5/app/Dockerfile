FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir email-validator python-multipart


ARG DATABASE_URL
ARG SECRET_KEY
ARG ALGORITHM
ARG ACCESS_TOKEN_EXPIRE_MINUTES


ENV DATABASE_URL=${DATABASE_URL}
ENV SECRET_KEY=${SECRET_KEY}
ENV ALGORITHM=${ALGORITHM}
ENV ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]