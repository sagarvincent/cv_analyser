FROM python:3.12-slim

RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data at build time into a known directory
RUN python -m nltk.downloader -d /app/nltk_data stopwords punkt

COPY . .

RUN chown -R app:app /app
USER app

ENV NLTK_DATA=/app/nltk_data

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
