FROM python:3.9

WORKDIR /app
COPY powerplant.py .
COPY wrapper.py .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "wrapper.py"]
