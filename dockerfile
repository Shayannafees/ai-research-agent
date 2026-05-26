FROM python:3.12-slim
WORKDIR /app
COPY requirement.txt .
RUN pip install -r requirement.txt
COPY . .
CMD ["uvicorn", "phase4.main:app", "--host", "0.0.0.0", "--port", "8000"]
