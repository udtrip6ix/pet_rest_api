FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
ENV PIP_PROGRESS_BAR=on
RUN pip install --no-cache-dir --index-url https://pypi.org/simple -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]