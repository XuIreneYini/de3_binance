FROM python:3.11-slim

RUN pip install fastapi uvicorn pandas matplotlib python-binance pydantic
ADD api.py /app/api.py
EXPOSE 8000
WORKDIR /app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
