FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN  apk add binutils gdal-dev geos-dev

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]