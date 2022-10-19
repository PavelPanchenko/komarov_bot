FROM python:3.10.4

WORKDIR app

COPY requirements.txt .

RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

COPY . .
